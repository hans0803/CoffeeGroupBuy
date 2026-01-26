#!/usr/bin/env python3
"""
咖啡團購系統 - Flask 應用程式
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

from .models import (
    init_db, save_products, get_all_products, get_product_by_id,
    get_products_by_ids, get_categories, create_order, get_all_orders,
    get_order_statistics, mark_order_submitted, export_orders_to_xlsx,
    get_orders_by_customer, get_all_customer_names, delete_order, update_order_item,
    get_common_prices, get_product_facets, ROAST_GROUPS, update_sales_statistics,
    get_current_sales_statistics
)
from .scraper import scrape_all_products, CATEGORY_NAMES
from .google_integration import submit_order_to_google

# 設定 template 和 static 路徑指向專案根目錄
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-2026')


# ========================================
# 頁面路由
# ========================================

def load_site_config():
    """讀取網站設定檔"""
    default_config = {
        "hero": {
            "title": "咖啡團購",
            "description": "各位又到了團購咖啡的時間啦",
            "deadline_info": "本次團購即將截止收單"
        },
        "info": {
            "how_to_buy": ["瀏覽產品並加入購物車", "前往購物車確認商品", "輸入您的姓名並送出訂單"],
            "notes": ["更改數量或商品請至我的訂單查詢", "確認購買數量請參考本期訂單統計", "收單前要記得送出訂單"]
        }
    }
    try:
        config_path = os.path.join(BASE_DIR, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
    return default_config

@app.route('/')
def index():
    """首頁 - 顯示分類"""
    categories = get_categories()
    site_config = load_site_config()
    
    # 讀取銷售統計
    stats = {}
    try:
        json_path = os.path.join(BASE_DIR, 'data', 'statistics.json')
        print(f"Loading stats from: {json_path}")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            print(f"Loaded stats with {len(stats.get('top_products', []))} top products")
        else:
            print(f"statistics.json not found at {json_path}")
    except Exception as e:
        print(f"Error loading statistics.json: {e}")
    
    # 如果沒有產品，提示重新爬取
    if not categories:
        flash('尚未載入產品資料，請點擊下方按鈕同步產品。', 'warning')
    
    return render_template('index.html', categories=categories, stats=stats, config=site_config)


@app.route('/products/<category>')
def products(category):
    """產品列表頁"""
    # 取得篩選參數
    try:
        min_price = int(request.args.get('min', 0)) if request.args.get('min') else None
        max_price = int(request.args.get('max', 0)) if request.args.get('max') else None
    except ValueError:
        min_price = None
        max_price = None

    roast = request.args.get('roast')
    processing = request.args.get('processing')

    # 取得產品與統計
    product_list = get_all_products(category, min_price, max_price, roast, processing)
    common_prices = get_common_prices(category)
    facets = get_product_facets(category)
    category_name = CATEGORY_NAMES.get(category, category)
    
    return render_template('products.html', 
                          products=product_list, 
                          category=category,
                          category_name=category_name,
                          common_prices=common_prices,
                          facets=facets,
                          roast_groups=ROAST_GROUPS,
                          current_min=request.args.get('min', ''),
                          current_max=request.args.get('max', ''),
                          current_roast=roast,
                          current_processing=processing)


@app.route('/cart')
def cart():
    """購物車頁面"""
    cart_data = session.get('cart', {})
    
    # 取得購物車中的產品資訊
    product_ids = list(cart_data.keys())
    products_info = get_products_by_ids(product_ids)
    
    # 合併購物車數量
    cart_items = []
    total = 0
    for product in products_info:
        quantity = cart_data.get(product['id'], {}).get('quantity', 0)
        if quantity > 0:
            item = {**product, 'quantity': quantity}
            cart_items.append(item)
            total += product['price'] * quantity
    
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout')
def checkout():
    """結帳確認頁"""
    cart_data = session.get('cart', {})
    
    if not cart_data:
        flash('購物車是空的', 'warning')
        return redirect(url_for('cart'))
    
    # 取得購物車資訊
    product_ids = list(cart_data.keys())
    products_info = get_products_by_ids(product_ids)
    
    cart_items = []
    total = 0
    for product in products_info:
        quantity = cart_data.get(product['id'], {}).get('quantity', 0)
        if quantity > 0:
            item = {**product, 'quantity': quantity}
            cart_items.append(item)
            total += product['price'] * quantity
    
    return render_template('checkout.html', cart_items=cart_items, total=total)


@app.route('/submit-order', methods=['POST'])
def submit_order():
    """提交訂單"""
    customer_name = request.form.get('customer_name', '').strip()
    
    if not customer_name:
        flash('請輸入您的姓名', 'error')
        return redirect(url_for('checkout'))
    
    cart_data = session.get('cart', {})
    if not cart_data:
        flash('購物車是空的', 'warning')
        return redirect(url_for('cart'))
    
    # 取得產品資訊
    product_ids = list(cart_data.keys())
    products_info = get_products_by_ids(product_ids)
    
    # 準備訂單項目
    items = []
    total = 0
    for product in products_info:
        quantity = cart_data.get(product['id'], {}).get('quantity', 0)
        if quantity > 0:
            items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            })
            total += product['price'] * quantity
    
    # 儲存訂單到資料庫
    order_id = create_order(customer_name, items, total)
    
    # 嘗試提交到 Google 表單
    success, message = submit_order_to_google(customer_name, items, total)
    if success:
        mark_order_submitted(order_id)
    
    # 清空購物車
    session.pop('cart', None)
    
    flash(f'訂單已送出！感謝 {customer_name} 的訂購。', 'success')
    return redirect(url_for('index'))


@app.route('/orders')
def orders_page():
    """訂單統計頁面"""
    orders = get_all_orders()
    stats = get_order_statistics()
    
    # 取得本期訂單的即時銷售統計 (Hot Items, Roast/Price Charts)
    sales_stats = get_current_sales_statistics()
    
    return render_template('orders.html', orders=orders, stats=stats, sales_stats=sales_stats)


# ========================================
# API 路由
# ========================================

@app.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    """加入購物車 API"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'success': False, 'message': '缺少產品 ID'})
    
    # 取得或初始化購物車
    cart = session.get('cart', {})
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'quantity': quantity,
            'name': data.get('name', ''),
            'price': data.get('price', 0)
        }
    
    session['cart'] = cart
    
    return jsonify({
        'success': True,
        'cart_count': len(cart),
        'message': '已加入購物車'
    })


@app.route('/api/cart/update', methods=['POST'])
def api_update_cart():
    """更新購物車數量 API"""
    data = request.get_json()
    product_id = data.get('product_id')
    delta = data.get('delta', 0)
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        cart[product_id]['quantity'] += delta
        
        if cart[product_id]['quantity'] <= 0:
            del cart[product_id]
    
    session['cart'] = cart
    
    return jsonify({'success': True, 'cart_count': len(cart)})


@app.route('/api/cart/remove', methods=['POST'])
def api_remove_from_cart():
    """移除購物車商品 API"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]
    
    session['cart'] = cart
    
    return jsonify({'success': True, 'cart_count': len(cart)})


@app.route('/api/sync-products', methods=['POST'])
def api_sync_products():
    """同步產品資料 API"""
    try:
        products = scrape_all_products()
        products_dict = [p.to_dict() for p in products]
        save_products(products_dict)
        
        return jsonify({
            'success': True,
            'message': f'成功同步 {len(products)} 個產品',
            'count': len(products)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'同步失敗: {str(e)}'
        })


# ========================================
# 初始化
# ========================================

@app.route('/api/export-orders', methods=['POST'])
def api_export_orders():
    """匯出訂單到 Excel API"""
    try:
        output_path = export_orders_to_xlsx()
        return jsonify({
            'success': True,
            'message': '訂單已匯出',
            'path': output_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'匯出失敗: {str(e)}'
        })


@app.route('/my-orders')
def my_orders():
    """我的訂單頁面"""
    name = request.args.get('name', '').strip()
    orders = []
    
    if name:
        orders = get_orders_by_customer(name)
        
    # 取得所有已下單的姓名供下拉選單使用
    all_names = get_all_customer_names()
    
    return render_template('my_orders.html', 
                          orders=orders, 
                          search_name=name,
                          all_names=all_names)


@app.route('/api/orders/delete', methods=['POST'])
def api_delete_order():
    """刪除訂單 API"""
    data = request.get_json()
    order_id = data.get('order_id')
    
    if not order_id:
        return jsonify({'success': False, 'message': '缺少訂單 ID'})
        
    success = delete_order(order_id)
    
    if success:
        return jsonify({'success': True, 'message': '訂單已刪除'})
    else:
        return jsonify({'success': False, 'message': '刪除失敗或訂單不存在'})


@app.route('/api/orders/update-item', methods=['POST'])
def api_update_order_item():
    """更新訂單項目數量 API"""
    data = request.get_json()
    order_id = data.get('order_id')
    product_name = data.get('product_name')
    quantity = data.get('quantity')
    
    if not order_id or not product_name or quantity is None:
        return jsonify({'success': False, 'message': '缺少必要參數'})
        
    try:
        success = update_order_item(order_id, product_name, int(quantity))
        
        if success:
            return jsonify({'success': True, 'message': '已更新'})
        else:
            return jsonify({'success': False, 'message': '更新失敗'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    """接收匿名回饋 API (儲存至 data/feedback.json)"""
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'success': False, 'message': '請輸入回饋內容'})
        
    try:
        feedback_file = os.path.join(BASE_DIR, 'data', 'feedback.json')
        feedback_list = []
        
        # 讀取現有回饋
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    feedback_list = json.load(f)
            except:
                feedback_list = []
        
        # 新增回饋
        new_feedback = {
            'content': message,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        feedback_list.append(new_feedback)
        
        # 寫回檔案
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, ensure_ascii=False, indent=2)
            
        return jsonify({'success': True, 'message': '感謝您的回饋！'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'儲存失敗: {str(e)}'})


def initialize_app():
    """初始化應用程式"""
    print("=" * 50)
    print("咖啡團購系統")
    print("=" * 50)
    
    # 初始化資料庫
    init_db()
    
    # 檢查是否需要爬取產品
    categories = get_categories()
    if not categories:
        print("首次啟動，正在爬取產品資料...")
        try:
            products = scrape_all_products()
            products_dict = [p.to_dict() for p in products]
            save_products(products_dict)
            print(f"已載入 {len(products)} 個產品")
        except Exception as e:
            print(f"爬取失敗: {e}")
            print("請稍後手動同步產品資料")
    else:
        total = sum(c['count'] for c in categories)
        print(f"已載入 {total} 個產品")
    
    print("=" * 50)


if __name__ == '__main__':
    initialize_app()
    print("伺服器啟動中... 請訪問 http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
