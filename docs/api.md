# API 介面文件 (API Documentation)

本系統主要為 Server-Side Rendering (SSR)，但部分功能透過 AJAX API 互動。

## 📦 訂單管理 (Orders)

### 1. 提交訂單
- **URL**: `/api/orders`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **描述**: 將購物車內的商品結算為正式訂單。
- **Payload**:
  ```json
  {
    "customer": "王小明"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "order_id": "xxxxxxxx",
    "message": "訂單已提交"
  }
  ```

### 2. 刪除訂單
- **URL**: `/api/orders/delete`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **描述**: 刪除指定 ID 的訂單 (僅限 My Orders 頁面使用)。
- **Payload**:
  ```json
  {
    "order_id": "xxxxxxxx"
  }
  ```
- **Response**:
  ```json
  { "success": true }
  ```

### 3. 更新訂單數量
- **URL**: `/api/orders/update`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **描述**: 修改訂單中特定商品的數量。
- **Payload**:
  ```json
  {
    "order_id": "xxxxxxxx",
    "product_id": "prod_123",
    "quantity": 5
  }
  ```
- **Response**:
  ```json
  { "success": true, "message": "已更新" }
  ```

---

## 🛒 購物車 (Cart)

### 1. 加入購物車
- **URL**: `/api/cart/add`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "product_id": "prod_123",
    "quantity": 1
  }
  ```

### 2. 更新購物車
- **URL**: `/api/cart/update`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "product_id": "prod_123",
    "quantity": 3
  }
  ```

---

## 💬 回饋系統 (Feedback)

### 1. 提交匿名回饋
- **URL**: `/api/feedback`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **描述**: 接收前台用戶的回饋訊息，存入 `feedback.json`。
- **Payload**:
  ```json
  {
    "message": "系統很好用"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "感謝您的回饋！"
  }
  ```
