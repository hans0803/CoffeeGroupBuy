/**
 * 咖啡團購系統 - 前端腳本
 */

// ========================================
// 購物車功能
// ========================================

/**
 * 加入購物車
 */
function addToCart(productId, productName, price, buttonElem) {
    if (buttonElem) {
        buttonElem.disabled = true;
        buttonElem.innerText = '處理中...';
    }
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
                if (buttonElem) {
                    buttonElem.innerText = '已在購物車';
                    buttonElem.style.background = '#e2e8f0';
                    buttonElem.style.color = '#64748b';
                    buttonElem.style.cursor = 'not-allowed';
                    buttonElem.style.border = '1px solid #cbd5e1';
                    buttonElem.style.boxShadow = 'none';
                }
            } else {
                showNotification(data.message || '發生錯誤', 'error');
                if (buttonElem) {
                    buttonElem.disabled = false;
                    buttonElem.innerText = '加入購物車';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('網路錯誤，請重試', 'error');
            if (buttonElem) {
                buttonElem.disabled = false;
                buttonElem.innerText = '加入購物車';
            }
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
    initStarRating();
    initFilterSheet();
    initNavPopups();
});

// ========================================
// 底部導覽列彈出選單
// ========================================

function toggleNavPopup(event, popupId) {
    // If the click is on a link, let it navigate
    if (event.target.tagName === 'A' || event.target.closest('a')) {
        return;
    }

    event.preventDefault();
    event.stopPropagation();

    const popup = document.getElementById(popupId);
    if (!popup) return;

    // Close all other popups first
    document.querySelectorAll('.nav-popup.show').forEach(p => {
        if (p.id !== popupId) p.classList.remove('show');
    });

    popup.classList.toggle('show');
}

function initNavPopups() {
    // Close popups when tapping anywhere else
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.bottom-nav-item')) {
            document.querySelectorAll('.nav-popup.show').forEach(p => {
                p.classList.remove('show');
            });
        }
    });

    // When a link inside a popup is clicked, hide it instantly
    document.querySelectorAll('.nav-popup a').forEach(link => {
        link.addEventListener('click', () => {
            const popup = link.closest('.nav-popup');
            if (popup) {
                popup.style.display = 'none'; // Instant hide
                setTimeout(() => popup.style.display = '', 500); // Restore after navigation starts
            }
        });
    });
}

// ========================================
// 篩選面板 Bottom Sheet (行動端)
// ========================================

function toggleSidebar() {
    const sidebar = document.getElementById('filterSidebar');
    const overlay = document.getElementById('filterOverlay');
    if (!sidebar) return;

    // 第一次互動時啟動動畫，防止頁面初始化時閃爍
    sidebar.classList.add('has-transition');

    if (sidebar.classList.contains('open')) {
        closeFilterSheet();
    } else {
        sidebar.classList.add('open');
        if (overlay) overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
        // Clear any inline styles set by dragging to let CSS !important take over
        sidebar.style.removeProperty('transform');
        sidebar.style.removeProperty('transition');
    }
}

function closeFilterSheet() {
    const sidebar = document.getElementById('filterSidebar');
    const overlay = document.getElementById('filterOverlay');
    if (sidebar) {
        sidebar.classList.remove('open');
        sidebar.style.transform = '';
    }
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
}

function initFilterSheet() {
    const sidebar = document.getElementById('filterSidebar');
    if (!sidebar) return;

    // 初始化時不要有動畫，防止頁面跳轉或重新整理時的閃爍
    sidebar.classList.remove('has-transition');

    // 延遲啟動動畫，確保初始渲染已完成
    setTimeout(() => {
        sidebar.classList.add('has-transition');
    }, 300);

    // 監聽側邊欄內的所有點擊事件 (Event Delegation)
    sidebar.addEventListener('click', (e) => {
        const target = e.target;
        // 如果點擊的是篩選連結或按鈕
        if (target.closest('a') || target.closest('button')) {
            // 點擊即時關閉，不要動畫
            sidebar.classList.remove('has-transition');
            closeFilterSheet();
        }
    });

    // 監聽表單提交 (自訂價格範圍)
    sidebar.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', () => {
            sidebar.classList.remove('has-transition');
            closeFilterSheet();
        });
    });

    let startY = 0;
    let currentY = 0;
    let isDragging = false;

    sidebar.addEventListener('touchstart', function (e) {
        // Only start drag from near the top (drag handle area)
        const touch = e.touches[0];
        const rect = sidebar.getBoundingClientRect();
        const touchOffset = touch.clientY - rect.top;

        // Allow drag initiation within the top 40px (drag handle), or if scrolled to top
        if (touchOffset < 40 || sidebar.scrollTop <= 0) {
            startY = touch.clientY;
            isDragging = true;
        }
    }, { passive: true });

    sidebar.addEventListener('touchmove', function (e) {
        if (!isDragging) return;

        currentY = e.touches[0].clientY;
        const deltaY = currentY - startY;

        // Only allow downward drag (positive delta)
        if (deltaY > 0) {
            // Apply resistance on drag (dampened movement)
            const dampened = deltaY * 0.6;
            sidebar.style.transform = `translateY(${dampened}px)`;
            sidebar.style.transition = 'none';

            // Prevent default scroll behavior when dragging down
            if (sidebar.scrollTop <= 0) {
                e.preventDefault();
            }
        }
    }, { passive: false });

    sidebar.addEventListener('touchend', function () {
        if (!isDragging) return;
        isDragging = false;

        const deltaY = currentY - startY;
        sidebar.style.transition = '';

        // If dragged more than 100px down, close; otherwise snap back
        if (deltaY > 100) {
            closeFilterSheet();
        } else {
            sidebar.style.transform = '';
        }
    }, { passive: true });
}

// ========================================
// 評論功能 (Reviews)
// ========================================

let currentReviewProductId = null;
let currentReviewProductName = null;

/**
 * 打開評價列表 Modal
 */
function openReviewModal(productId, productName) {
    currentReviewProductId = productId;
    currentReviewProductName = productName;

    document.getElementById('reviewListTitle').innerText = '💬 ' + productName + ' 的評價';
    document.getElementById('reviewListModal').style.display = 'flex';

    const container = document.getElementById('reviewListContainer');
    container.innerHTML = '<div style="text-align:center; padding: 2rem; color: #666;">載入中...</div>';

    fetch('/api/products/' + productId + '/reviews')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.reviews.length > 0) {
                let html = '';
                data.reviews.forEach(review => {
                    const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
                    const date = new Date(review.created_at).toLocaleDateString();
                    html += `
                        <div class="review-card">
                            <div class="review-header">
                                <span class="review-name">${review.reviewer_name}</span>
                                <span class="review-date">${date}</span>
                            </div>
                            <div class="review-stars">${stars}</div>
                            ${review.comment ? `<div class="review-text">${review.comment.replace(/</g, "&lt;")}</div>` : ''}
                        </div>
                    `;
                });
                container.innerHTML = html;
            } else {
                container.innerHTML = '<div style="text-align:center; padding: 2rem; color: #999;">目前還沒有評價，成為第一個評價的人吧！</div>';
            }
        })
        .catch(err => {
            console.error(err);
            container.innerHTML = '<div style="text-align:center; padding: 2rem; color: #c62828;">載入失敗，請稍後再試</div>';
        });
}

function closeReviewListModal() {
    document.getElementById('reviewListModal').style.display = 'none';
}

/**
 * 打開寫評價 Modal
 */
function openWriteReviewModal() {
    closeReviewListModal();
    document.getElementById('writeReviewTitle').innerText = '評分：' + currentReviewProductName;
    document.getElementById('writeReviewModal').style.display = 'flex';

    // Reset form
    document.getElementById('reviewRating').value = '0';
    document.getElementById('reviewComment').value = '';
    const stars = document.querySelectorAll('#starRating span');
    stars.forEach(s => s.classList.remove('active'));
    document.getElementById('submitReviewBtn').disabled = false;
    document.getElementById('submitReviewBtn').innerText = '送出評論';
}

function closeWriteReviewModal() {
    document.getElementById('writeReviewModal').style.display = 'none';
}

/**
 * 初始化星星評分點擊事件
 */
function initStarRating() {
    const stars = document.querySelectorAll('#starRating span');
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const val = this.getAttribute('data-value');
            document.getElementById('reviewRating').value = val;

            // Highlight up to the clicked star
            stars.forEach(s => {
                if (parseInt(s.getAttribute('data-value')) <= parseInt(val)) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });
    });
}

/**
 * 送出評價
 */
function submitReview() {
    const rating = parseInt(document.getElementById('reviewRating').value);
    const reviewerName = document.getElementById('reviewNameSelect').value;
    const comment = document.getElementById('reviewComment').value.trim();

    if (rating === 0) {
        alert('請點擊星星進行評分！');
        return;
    }

    const btn = document.getElementById('submitReviewBtn');
    btn.disabled = true;
    btn.innerText = '處理中...';

    fetch('/api/products/' + currentReviewProductId + '/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            reviewer_name: reviewerName,
            rating: rating,
            comment: comment
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showNotification('感謝您的評價！', 'success');
                closeWriteReviewModal();
                // Reload page to show updated star ratings on the card
                setTimeout(() => location.reload(), 1000);
            } else {
                alert(data.message || '發生錯誤');
                btn.disabled = false;
                btn.innerText = '送出評論';
            }
        })
        .catch(err => {
            console.error(err);
            alert('網路錯誤，請稍後再試');
            btn.disabled = false;
            btn.innerText = '送出評論';
        });
}

// Global click outside to close for ALL modals
window.onclick = function (event) {
    const fbModal = document.getElementById('feedbackModal');
    const rlModal = document.getElementById('reviewListModal');
    const wrModal = document.getElementById('writeReviewModal');

    if (event.target == fbModal) fbModal.style.display = 'none';
    if (event.target == rlModal) rlModal.style.display = 'none';
    if (event.target == wrModal) wrModal.style.display = 'none';
}
