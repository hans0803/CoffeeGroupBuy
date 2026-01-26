#!/usr/bin/env python3
"""
Google 表單整合模組
將訂單資料發送到 Google Apps Script Web App
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional

# Google Apps Script Web App URL (使用者需自行設定)
GOOGLE_SCRIPT_URL = os.environ.get('GOOGLE_SCRIPT_URL', '')


def submit_order_to_google(
    customer_name: str,
    items: list[dict],
    total: int
) -> tuple[bool, str]:
    """
    將訂單提交到 Google 表單
    
    Args:
        customer_name: 購買者姓名
        items: 購買項目列表 [{"name": "產品名", "quantity": 1, "price": 100}, ...]
        total: 總金額
    
    Returns:
        tuple: (成功與否, 訊息)
    """
    if not GOOGLE_SCRIPT_URL:
        return False, "未設定 Google Script URL，請設定環境變數 GOOGLE_SCRIPT_URL"
    
    # 格式化項目清單
    items_text = "\n".join([
        f"- {item['name']} x{item['quantity']} = NT${item['price'] * item['quantity']}"
        for item in items
    ])
    
    payload = {
        "timestamp": datetime.now().isoformat(),
        "customer": customer_name,
        "items": items_text,
        "items_json": json.dumps(items, ensure_ascii=False),
        "total": total
    }
    
    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return True, "訂單已成功提交到 Google 試算表"
        else:
            return False, f"提交失敗: HTTP {response.status_code}"
            
    except requests.RequestException as e:
        return False, f"網路錯誤: {str(e)}"


# ========================================
# Google Apps Script 範例程式碼
# ========================================
GOOGLE_APPS_SCRIPT_EXAMPLE = '''
// ========================================
// Google Apps Script 範例
// 請在 Google Apps Script 中建立新專案並貼上此程式碼
// ========================================

/**
 * 處理 POST 請求，將訂單資料新增到試算表
 */
function doPost(e) {
  try {
    // 取得當前試算表
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // 解析 JSON 資料
    const data = JSON.parse(e.postData.contents);
    
    // 新增一行資料
    sheet.appendRow([
      data.timestamp,      // 時間戳記
      data.customer,       // 購買者
      data.items,          // 商品明細
      data.total,          // 總金額
      new Date()           // 記錄時間
    ]);
    
    // 回傳成功
    return ContentService.createTextOutput('OK');
    
  } catch (error) {
    // 回傳錯誤訊息
    return ContentService.createTextOutput('Error: ' + error.message);
  }
}

/**
 * 初始化試算表標題列（手動執行一次）
 */
function initSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.getRange(1, 1, 1, 5).setValues([
    ['訂單時間', '購買者', '商品明細', '總金額', '記錄時間']
  ]);
  sheet.getRange(1, 1, 1, 5).setFontWeight('bold');
}

// ========================================
// 部署步驟：
// 1. 建立新的 Google 試算表
// 2. 工具 → 指令碼編輯器
// 3. 貼上此程式碼
// 4. 先執行 initSheet() 初始化標題
// 5. 部署 → 新增部署
// 6. 類型選擇「網頁應用程式」
// 7. 執行身分：本人
// 8. 存取權：任何人
// 9. 複製 Web App URL 並設定到環境變數
// ========================================
'''


def print_google_script_instructions():
    """印出 Google Apps Script 設定說明"""
    print("=" * 60)
    print("Google 表單整合設定說明")
    print("=" * 60)
    print(GOOGLE_APPS_SCRIPT_EXAMPLE)
    print("=" * 60)


if __name__ == "__main__":
    print_google_script_instructions()
