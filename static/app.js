/**
 * 咖啡團購系統 - 前端腳本
 */

// ========================================
// 購物車功能
// ========================================

/**
 * 加入購物車
 */
function addToCart(productId, productName, price) {
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            name: productName,
            price: price,
            quantity: 1
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('已加入購物車！', 'success');
                updateCartCount(data.cart_count);
            } else {
                showNotification(data.message || '發生錯誤', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('網路錯誤，請重試', 'error');
        });
}

/**
 * 更新商品數量
 */
function updateQuantity(productId, delta) {
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            delta: delta
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

/**
 * 從購物車移除商品
 */
function removeFromCart(productId) {
    fetch('/api/cart/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

/**
 * 更新購物車數量顯示
 */
function updateCartCount(count) {
    const cartCountEl = document.getElementById('cart-count');
    if (cartCountEl) {
        cartCountEl.textContent = count;
        // 加入動畫效果
        cartCountEl.classList.add('bounce');
        setTimeout(() => cartCountEl.classList.remove('bounce'), 300);
    }
}

// ========================================
// 通知功能
// ========================================

/**
 * 顯示通知訊息
 */
function showNotification(message, type = 'success') {
    // 移除現有通知
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    // 建立通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">✕</button>
    `;

    // 加入樣式
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#2E7D32' : '#C62828'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 1rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    // 按鈕樣式
    const btn = notification.querySelector('button');
    btn.style.cssText = `
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 1rem;
        opacity: 0.8;
    `;

    document.body.appendChild(notification);

    // 自動消失
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ========================================
// 動畫樣式
// ========================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    .bounce {
        animation: bounce 0.3s ease;
    }
`;
document.head.appendChild(style);

// ========================================
// 頁面載入完成
// ========================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('☕ 咖啡團購系統已載入');
});
