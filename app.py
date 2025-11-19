import streamlit as st
import streamlit.components.v1 as components

# 1. 設定頁面配置
st.set_page_config(page_title="食際行動家", layout="wide")

# 2. 將您的 HTML/CSS/JS 放入一個長字串變數中
# 注意：我已經移除了原本卡在 CSS 裡面的 Python 錯誤代碼
html_code = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>蔬果</title>
    
    <style>
        /* --- 全域設定 --- */
        html { scroll-behavior: smooth; }
        body {
            font-family: Arial, "Helvetica Neue", "Microsoft JhengHei", sans-serif;
            background-color: #f0f2f5;
            /* 這裡原本有錯誤的 Python 程式碼，已經移除了 */
            padding-bottom: 100px;
            margin: 0;
            overflow-x: hidden;
        }
        h1 { text-align: center; color: #333; }
        button { cursor: pointer; transition: transform 0.1s, background-color 0.3s; }
        button:active { transform: scale(0.95); }
        input:focus, textarea:focus, select:focus { outline: 2px solid #d9534f; }

        /* --- (修改) 全螢幕廣告/歡迎頁樣式 --- */
        #splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #ffffff;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: transform 0.8s cubic-bezier(0.7, 0, 0.3, 1);
            cursor: pointer;
        }
        
        #splash-screen.hidden {
            transform: translateY(-100%);
        }

        .splash-logo {
            width: 90%;
            height: 90%;
            max-width: 1000px;
            object-fit: contain;
            cursor: pointer;
            animation: breathe 3s infinite ease-in-out;
            user-select: none;
        }

        @keyframes breathe {
            0% { transform: scale(0.98); opacity: 0.9; }
            50% { transform: scale(1.02); opacity: 1; }
            100% { transform: scale(0.98); opacity: 0.9; }
        }

        .click-hint {
            position: absolute;
            bottom: 50px;
            color: #999;
            font-size: 1.2rem;
            animation: blink 2s infinite;
            pointer-events: none;
        }
        @keyframes blink { 50% { opacity: 0; } }

        /* --- 頁面切換動畫 --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        #list-page, #detail-page, #backend-page { animation: fadeInUp 0.4s ease-out; }

        /* --- 導覽列 --- */
        .nav-header { 
            text-align: center; 
            margin-bottom: 30px; 
            animation: fadeInUp 0.6s ease-out; 
            position: relative; 
            padding-top: 10px;
        }
        .logo-container img {
            max-width: 180px;
            height: auto;
            display: block;
            margin: 0 auto 10px auto;
        }
        .nav-header h2 { color: #d9534f; margin: 0; letter-spacing: 1px; display: inline-block; font-size: 1.8rem; }
        
        .backend-entry-btn {
            position: absolute;
            right: 0;
            top: 20px;
            background: none;
            border: 1px solid #ccc;
            padding: 5px 10px;
            border-radius: 20px;
            color: #666;
            font-size: 0.9rem;
        }
        .backend-entry-btn:hover { background-color: #eee; color: #333; }

        /* --- 商品列表樣式 --- */
        #product-list-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .product-card {
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            display: flex; 
            flex-direction: column;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .product-card:hover { transform: translateY(-8px); box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
        .product-card-img { width: 100%; height: 180px; object-fit: cover; cursor: pointer; transition: transform 0.5s; }
        .product-card:hover .product-card-img { transform: scale(1.05); }
        .card-content { padding: 15px; display: flex; flex-direction: column; flex-grow: 1; position: relative; z-index: 1; background: white; }
        .card-content h3 { color: #d9534f; margin: 0 0 10px 0; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .card-content p { margin: 5px 0; color: #555; font-size: 0.95rem; }
        .card-content .price { font-size: 1.2rem; font-weight: bold; color: #000; margin-top: auto; padding-top: 10px;}
        
        .card-actions { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 8px; margin-top: 15px; }
        .view-detail-btn, .add-to-cart-btn, .view-recipe-btn { padding: 8px 0; border: none; border-radius: 8px; font-size: 0.85rem; font-weight: bold; }
        .view-detail-btn { background-color: #6c757d; color: white; }
        .add-to-cart-btn { background-color: #d9534f; color: white; }
        .add-to-cart-btn:hover { background-color: #c9302c; box-shadow: 0 2px 8px rgba(217, 83, 79, 0.4); }
        .view-recipe-btn { background-color: #f0ad4e; color: white; }
        .view-recipe-btn:hover { background-color: #ec971f; box-shadow: 0 2px 8px rgba(240, 173, 78, 0.4); }
        
        .tag { display: inline-block; background-color: #5cb85c; color: white; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem; margin-right: 5px; }
        .expiry-tag { background-color: #f0ad4e; }
        .expired-tag { background-color: #d9534f; }

        /* --- 詳情頁樣式 --- */
        #detail-page { display: none; max-width: 800px; margin: 0 auto; }
        .detail-main-card { background-color: #ffffff; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; margin-bottom: 30px; }
        #detail-image { width: 100%; height: 350px; object-fit: cover; }
        .detail-content { padding: 30px; }
        .back-to-list-btn { background-color: transparent; color: #666; border: 2px solid #ccc; padding: 10px 20px; width: auto; text-align: center; font-size: 1rem; margin-bottom: 20px; border-radius: 30px; font-weight: bold; transition: all 0.3s; }
        .back-to-list-btn:hover { background-color: #666; color: white; border-color: #666; }
        .related-recipes-section { margin-top: 40px; border-top: 2px dashed #eee; padding-top: 30px; }
        .related-recipes-section h2 { color: #d9534f; text-align: center; margin-bottom: 25px; font-size: 1.5rem; }
        #related-recipes-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; }

        .no-recipe-box { grid-column: 1 / -1; background-color: #fff8e1; border: 2px solid #ffe082; color: #8d6e63; padding: 30px; border-radius: 15px; text-align: center; animation: fadeInUp 0.5s; }
        .generate-btn { background-color: #17a2b8; color: white; border: none; padding: 12px 25px; border-radius: 30px; font-size: 1rem; margin-top: 15px; font-weight: bold; box-shadow: 0 4px 10px rgba(23, 162, 184, 0.3); }
        .generate-btn:hover { background-color: #138496; transform: translateY(-2px); }

        /* 食譜卡片 */
        .recipe-card { background-color: #fff; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border: 1px solid #f0f0f0; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.3s; }
        .recipe-card:hover { transform: translateY(-5px); }
        .recipe-card-img { width: 100%; height: 180px; object-fit: cover; }
        .recipe-content { padding: 20px; flex-grow: 1; }
        .recipe-card h3 { margin-top: 0; color: #333; border-bottom: 2px solid #f0ad4e; padding-bottom: 10px; margin-bottom: 10px; }
        .recipe-calories { font-weight: bold; color: #e67e22; font-size: 0.95rem; margin: 10px 0; }
        .recipe-card ol { padding-left: 20px; font-size: 0.95rem; color: #444; line-height: 1.6; }
        
        .ingredient-list { list-style: none; padding: 0; margin: 15px 0; background: #f9f9f9; border-radius: 8px; padding: 10px; }
        .ingredient-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px dashed #ddd; font-size: 0.95rem; }
        .ingredient-item:last-child { border-bottom: none; }
        .del-ing-btn { color: #ff4d4d; font-weight: bold; cursor: pointer; padding: 0 8px; font-size: 1.2rem; transition: transform 0.2s; }
        .del-ing-btn:hover { transform: scale(1.2); }
        
        .add-ing-row { display: flex; gap: 8px; margin-top: 10px; margin-bottom: 20px; }
        .add-ing-input { flex: 1; padding: 8px 12px; border: 1px solid #ccc; border-radius: 20px; transition: border 0.3s; }
        .add-ing-btn { background-color: #5cb85c; color: white; border: none; border-radius: 50%; width: 35px; height: 35px; font-weight: bold; display: flex; justify-content: center; align-items: center; font-size: 1.2rem; }
        .add-ing-btn:hover { background-color: #4cae4c; }
        
        .magic-generate-btn { width: 100%; padding: 12px; background: linear-gradient(45deg, #6f42c1, #8e44ad); color: white; border: none; border-radius: 8px; font-weight: bold; margin-bottom: 15px; transition: all 0.3s; box-shadow: 0 4px 10px rgba(111, 66, 193, 0.3); }
        .magic-generate-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(111, 66, 193, 0.4); }

        .save-recipe-btn { width: 100%; padding: 12px; background-color: #fff; border: 2px solid #5cb85c; color: #5cb85c; font-weight: bold; margin-top: 10px; border-radius: 30px; transition: all 0.3s; }
        .save-recipe-btn:hover { background-color: #eaffea; }
        .save-recipe-btn.saved { background-color: #5cb85c; color: white; }

        /* --- 懸浮按鈕區 (Stack) --- */
        #fab-container-right { position: fixed; bottom: 30px; right: 30px; display: flex; flex-direction: column; gap: 15px; z-index: 1000; align-items: center; }
        
        .fab-btn { width: 70px; height: 70px; color: white; border-radius: 50%; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; font-size: 2rem; transition: transform 0.2s, background-color 0.3s; position: relative; }
        .fab-btn:hover { transform: scale(1.1); }
        
        #cart-fab { background-color: #d9534f; }
        #cart-fab:hover { background-color: #c9302c; }
        
        #chat-fab { background-color: #2c3e50; font-size: 1.8rem; }
        #chat-fab:hover { background-color: #1a252f; }

        #recipe-book-fab { position: fixed; bottom: 30px; left: 30px; width: 70px; height: 70px; background-color: #5cb85c; color: white; border-radius: 50%; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; font-size: 2rem; z-index: 1000; transition: transform 0.2s; }
        #recipe-book-fab:hover { transform: scale(1.1); background-color: #4cae4c; }
        
        .fab-badge { position: absolute; top: -5px; right: -5px; background-color: #333; color: white; font-size: 0.9rem; width: 28px; height: 28px; border-radius: 50%; display: flex; justify-content: center; align-items: center; border: 2px solid #fff; }
        
        /* --- Modal 共用 --- */
        @keyframes modalFadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); z-index: 2000; justify-content: center; align-items: center; backdrop-filter: blur(3px); }
        .modal-panel { 
            background-color: #fff; width: 90%; max-width: 500px; border-radius: 15px; overflow: hidden; display: flex; flex-direction: column; max-height: 80vh; 
            animation: modalFadeIn 0.3s ease-out; 
        }
        .modal-header { padding: 20px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .cart-header-bg { background: linear-gradient(to right, #d9534f, #c9302c); }
        .recipe-header-bg { background: linear-gradient(to right, #5cb85c, #4cae4c); }
        .modal-header h2 { margin: 0; font-size: 1.3rem; }
        .close-modal-btn { background: none; border: none; color: white; font-size: 1.8rem; cursor: pointer; transition: transform 0.2s; }
        .close-modal-btn:hover { transform: rotate(90deg); }
        .modal-body { padding: 20px; overflow-y: auto; }
        .modal-footer { padding: 20px; background-color: #f9f9f9; border-top: 1px solid #eee; }
        
        /* 購物車項目 */
        .list-item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding: 15px 0; }
        .item-info { flex-grow: 1; }
        .item-name { font-weight: bold; font-size: 1.05rem; color: #333; }
        .item-price { color: #666; font-size: 0.9rem; margin-top: 4px; }
        .item-controls { display: flex; align-items: center; gap: 10px; }
        .qty-btn { width: 32px; height: 32px; border-radius: 50%; border: 1px solid #ccc; background: white; color: #333; font-weight: bold; font-size: 1.1rem; display: flex; justify-content: center; align-items: center; padding: 0; transition: all 0.2s; }
        .qty-btn:hover { background-color: #f0f0f0; border-color: #bbb; transform: scale(1.1); }
        .item-qty { min-width: 24px; text-align: center; font-weight: bold; font-size: 1.1rem; }
        .remove-btn { margin-left: 5px; background: none; border: none; font-size: 1.2rem; color: #ff6b6b; opacity: 0.7; cursor: pointer; transition: all 0.2s; }
        .remove-btn:hover { opacity: 1; transform: scale(1.2); }

        .cart-total { display: flex; justify-content: space-between; font-size: 1.3rem; font-weight: bold; margin-bottom: 15px; color: #333; }
        .action-btn { width: 100%; padding: 15px; color: white; border: none; border-radius: 8px; font-size: 1.2rem; font-weight: bold; cursor: pointer; transition: opacity 0.2s; }
        .action-btn:hover { opacity: 0.9; }
        .cart-btn-bg { background-color: #d9534f; }
        .recipe-btn-bg { background-color: #5cb85c; }
        .empty-msg { text-align: center; color: #999; padding: 30px 0; font-size: 1.1rem; }

        /* --- Toast 提示 --- */
        #toast-container { position: fixed; bottom: 110px; left: 50%; transform: translateX(-50%); z-index: 3000; display: flex; flex-direction: column; gap: 10px; align-items: center; pointer-events: none; }
        .toast { background-color: rgba(50, 50, 50, 0.95); color: #fff; padding: 12px 24px; border-radius: 30px; font-size: 1rem; font-weight: bold; opacity: 0; transform: translateY(20px); transition: opacity 0.3s ease, transform 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.4); pointer-events: auto; }
        .toast.show { opacity: 1; transform: translateY(0); }

        /* --- 後台管理介面 --- */
        #backend-page { display: none; max-width: 1100px; margin: 0 auto; }
        .admin-container { background-color: white; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 30px; }
        .admin-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 20px; }
        .admin-header h2 { margin: 0; color: #333; }
        .admin-tabs { display: flex; gap: 15px; margin-bottom: 20px; }
        .admin-tab-btn { padding: 10px 20px; border: 1px solid #ccc; border-radius: 5px; background: white; color: #555; font-weight: bold; }
        .admin-tab-btn.active { background-color: #333; color: white; border-color: #333; }
        
        .admin-table { width: 100%; border-collapse: collapse; }
        .admin-table th, .admin-table td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        .admin-table th { background-color: #f9f9f9; color: #555; }
        .admin-table img { width: 50px; height: 50px; object-fit: cover; border-radius: 5px; }
        .admin-action-btn { padding: 5px 10px; border-radius: 4px; font-size: 0.85rem; border: none; color: white; }
        .btn-delete { background-color: #d9534f; }
        .btn-delete:hover { background-color: #c9302c; }
        
        .admin-form { background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; align-items: end; }
        .form-group { display: flex; flex-direction: column; }
        .form-group label { font-size: 0.9rem; color: #666; margin-bottom: 5px; }
        .form-group input, .form-group select { padding: 8px; border: 1px solid #ccc; border-radius: 5px; }
        .btn-add { background-color: #5cb85c; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; height: 40px; }
        .btn-add:hover { background-color: #4cae4c; }
        
        .back-store-btn { background-color: #6c757d; color: white; border: none; padding: 8px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; }
        .back-store-btn:hover { background-color: #5a6268; }

        /* --- 前台聊天視窗 --- */
        #chat-widget {
            display: none; position: fixed; bottom: 110px; right: 30px; width: 320px; height: 450px; background-color: #7296c2; border-radius: 15px; box-shadow: 0 5px 25px rgba(0,0,0,0.2); z-index: 2000; flex-direction: column; overflow: hidden; border: 1px solid #ddd; animation: modalFadeIn 0.3s ease-out;
        }
        .chat-header { background: #2c3e50; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .chat-header h3 { margin: 0; font-size: 1rem; }
        .close-chat-btn { background: none; border: none; color: white; font-size: 1.2rem; cursor: pointer; }
        .chat-area { flex-grow: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 80%; padding: 10px; border-radius: 15px; font-size: 0.9rem; position: relative; word-wrap: break-word; }
        .msg-bot { align-self: flex-start; background: white; color: #333; border-top-left-radius: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
        .msg-user { align-self: flex-end; background: #98e165; color: #333; border-top-right-radius: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
        .chat-input-area { background: white; padding: 10px; display: flex; gap: 5px; border-top: 1px solid #ddd; }
        .chat-input { flex-grow: 1; border: 1px solid #ddd; border-radius: 20px; padding: 8px 12px; }
        .chat-send-btn { background: transparent; color: #2c3e50; border: none; font-weight: bold; }

    </style>
</head>
<body>

    <div id="splash-screen" onclick="enterSite()">
        <img src="images/食際行動家.png" alt="食際行動家" class="splash-logo" onerror="this.style.display='none'; this.parentElement.innerHTML+='<h2 style=\'color:#d9534f;font-size:3rem;\'>食際行動家</h2>'">
        <div class="click-hint">👆 點擊進入</div>
    </div>

    <div class="nav-header">
        <div class="logo-container">
            <img src="images/食際行動家.png" alt="食際行動家 Logo" onerror="this.style.display='none'">
        </div>
        <h2>🛒 蔬果專區</h2>
        <button class="backend-entry-btn" id="backend-entry-btn">⚙️ 後台管理</button>
    </div>

    <div id="list-page">
        <div id="product-list-container"></div>
    </div>
    
    <div id="detail-page">
        <button class="back-to-list-btn">← 返回商品列表</button>
        
        <div class="detail-main-card">
            <img id="detail-image" src="" alt="商品圖片" onerror="this.src='https://via.placeholder.com/800x350?text=No+Image'">
            <div class="detail-content">
                <h1 id="detail-name">商品名稱</h1>
                <div id="detail-tags"></div>
                <p class="price" id="detail-price" style="text-align: center; font-size: 1.5rem;">NT$ 0</p>
                
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <button class="add-to-cart-btn" id="detail-add-btn" style="padding: 12px; font-size: 1.1rem;">+ 加入購物車</button>
                    <button id="favButton" style="flex: 1; background: #fff; border: 1px solid #ccc; color: #d9534f;">❤️ 收藏商品</button>
                </div>

                <div id="detail-info">
                    <p><strong>來源:</strong> <span id="detail-origin"></span> | <strong>到期日:</strong> <span id="detail-expiry"></span></p>
                    <p style="font-size: 1.1rem; margin-top: 10px;">🕒 狀態：<span id="detail-days-left-status" style="font-weight: bold;"></span></p>
                </div>

                <div class="related-recipes-section" id="related-recipes-section">
                    <h2>💡 創意料理廚房：<span id="recipe-ingredient-name"></span></h2>
                    <div id="related-recipes-container"></div>
                </div>
            </div>
        </div>
    </div>

    <div id="backend-page">
        <div class="admin-container">
            <div class="admin-header">
                <h2>⚙️ 後台管理系統</h2>
                <button class="back-store-btn" id="back-store-btn">← 返回前台</button>
            </div>
            
            <div class="admin-tabs">
                <button class="admin-tab-btn active" onclick="switchAdminTab('products')">商品管理</button>
                <button class="admin-tab-btn" onclick="switchAdminTab('bot')">LINE 機器人設定</button>
                <button class="admin-tab-btn" onclick="switchAdminTab('orders')">訂單檢視</button>
            </div>
            
            <div id="admin-products-section">
                <div class="admin-form">
                    <div class="form-group"><label>名稱</label><input type="text" id="new-p-name" placeholder="如: 西瓜"></div>
                    <div class="form-group"><label>價格</label><input type="number" id="new-p-price" placeholder="如: 200"></div>
                    <div class="form-group"><label>分類</label><select id="new-p-category"><option value="水果">水果</option><option value="蔬菜">蔬菜</option></select></div>
                    <button class="btn-add" onclick="addNewProduct()">+ 新增商品</button>
                </div>
                <table class="admin-table">
                    <thead><tr><th>圖片</th><th>編號</th><th>名稱</th><th>分類</th><th>價格</th><th>操作</th></tr></thead>
                    <tbody id="admin-product-list"></tbody>
                </table>
            </div>

            <div id="admin-bot-section" style="display: none;">
                <div class="admin-form" style="grid-template-columns: 1fr 1fr auto;">
                    <div class="form-group"><label>關鍵字 (顧客說)</label><input type="text" id="new-kw" placeholder="如: 營業時間"></div>
                    <div class="form-group"><label>回覆內容 (機器人說)</label><input type="text" id="new-reply" placeholder="我們 24h 營業"></div>
                    <button class="btn-add" style="height: 36px; margin-bottom: 2px;" onclick="addBotRule()">新增規則</button>
                </div>
                <table class="admin-table">
                    <thead><tr><th>關鍵字</th><th>回覆內容</th><th>操作</th></tr></thead>
                    <tbody id="bot-rules-list"></tbody>
                </table>
            </div>

            <div id="admin-orders-section" style="display: none;">
                <p style="text-align: center; color: #666; margin-top: 50px;">目前尚無訂單資料。</p>
            </div>
        </div>
    </div>

    <div id="fab-container-right">
        <button id="chat-fab" class="fab-btn">💬</button>
        <button id="cart-fab" class="fab-btn">🛒<div id="cart-badge" class="fab-badge">0</div></button>
    </div>
    <button id="recipe-book-fab">📖<div id="recipe-book-badge" class="fab-badge">0</div></button>
    
    <div id="cart-modal" class="modal">
        <div class="modal-panel">
            <div class="modal-header cart-header-bg"><h2>我的購物車</h2><button class="close-modal-btn">&times;</button></div>
            <div class="modal-body" id="cart-items-list"><p class="empty-msg">購物車是空的</p></div>
            <div class="modal-footer">
                <div class="cart-total"><span>總金額:</span><span id="cart-total-price">NT$ 0</span></div>
                <button class="action-btn cart-btn-bg" onclick="alert('感謝購買！')">去買單</button>
            </div>
        </div>
    </div>

    <div id="recipe-book-modal" class="modal">
        <div class="modal-panel">
            <div class="modal-header recipe-header-bg"><h2>我的食譜本</h2><button class="close-modal-btn">&times;</button></div>
            <div class="modal-body" id="recipe-book-list"><p class="empty-msg">尚未收藏任何食譜</p></div>
            <div class="modal-footer">
                <button class="action-btn recipe-btn-bg" onclick="document.getElementById('recipe-book-modal').style.display='none'">關閉</button>
            </div>
        </div>
    </div>

    <div id="chat-widget">
        <div class="chat-header">
            <h3>LINE 官方客服</h3>
            <button class="close-chat-btn" onclick="document.getElementById('chat-widget').style.display='none'">&times;</button>
        </div>
        <div class="chat-area" id="chat-display">
            <div class="msg msg-bot">您好！歡迎光臨 🥦<br>請問有什麼我可以幫您的嗎？</div>
        </div>
        <div class="chat-input-area">
            <input type="text" class="chat-input" id="chat-msg-input" placeholder="輸入訊息..." onkeypress="if(event.key==='Enter') sendChatMsg()">
            <button class="chat-send-btn" onclick="sendChatMsg()">傳送</button>
        </div>
    </div>

    <div id="toast-container"></div>

    <script>
        // --- 廣告頁控制 ---
        function enterSite() {
            const splash = document.getElementById('splash-screen');
            splash.classList.add('hidden');
            // 移除 DOM 避免擋住
            setTimeout(() => splash.style.display = 'none', 800);
        }

        // --- 基礎工具 ---
        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = message;
            container.appendChild(toast);
            void toast.offsetWidth; 
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => { if(container.contains(toast)) container.removeChild(toast); }, 300);
            }, 3000);
        }

        function getFutureDate(daysToAdd) {
            const date = new Date();
            date.setDate(date.getDate() + daysToAdd);
            return date.toISOString().split('T')[0];
        }

        function calculateDaysLeft(targetDateString) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const target = new Date(targetDateString);
            const diffTime = target - today;
            return Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
        }

        // --- 資料庫 (圖片連結) ---
        // 注意：我已將圖片連結改成網路範例圖，因為在 Streamlit 元件中無法直接讀取您的 images/ 資料夾
        // 如果您有自己的圖片網址，請替換掉下面的 https://...
        let productDatabase = [
            { id: "F0001", name: "蘋果", price: 138.4, category: "水果", imageUrl: "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400", calories: 90, origin: "美國", storage: "冷凍", expiryDate: getFutureDate(6), vendor: "每日良品" },
            { id: "F0002", name: "香蕉", price: 80, category: "水果", imageUrl: "https://images.unsplash.com/photo-1571771896612-61871f015852?w=400", calories: 105, origin: "台灣", storage: "常溫", expiryDate: getFutureDate(3), vendor: "樂活農莊" },
            { id: "F0003", name: "鳳梨", price: 155, category: "水果", imageUrl: "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400", calories: 150, origin: "美國", storage: "冷凍", expiryDate: getFutureDate(5), vendor: "綠源生技" },
            { id: "F0004", name: "高麗菜", price: 161.4, category: "蔬菜", imageUrl: "https://images.unsplash.com/photo-1623341214825-9f4f963727da?w=400", calories: 50, origin: "台灣", storage: "冷藏", expiryDate: getFutureDate(7), vendor: "安心食堂" },
            { id: "F0005", name: "番茄", price: 70, category: "蔬菜", imageUrl: "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400", calories: 30, origin: "台灣", storage: "冷藏", expiryDate: getFutureDate(4), vendor: "綠源生技" },
            { id: "F0006", name: "菠菜", price: 90, category: "蔬菜", imageUrl: "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400", calories: 40, origin: "台灣", storage: "冷藏", expiryDate: getFutureDate(2), vendor: "樂活農莊" },
            { id: "F0007", name: "柳橙", price: 120, category: "水果", imageUrl: "https://images.unsplash.com/photo-1547514701-42782101795e?w=400", calories: 120, origin: "美國", storage: "冷藏", expiryDate: getFutureDate(10), vendor: "每日良品" },
            { id: "F0008", name: "地瓜", price: 190.7, category: "蔬菜", imageUrl: "https://images.unsplash.com/photo-1573562389749-3740ba3b6e29?w=400", calories: 180, origin: "台灣", storage: "常溫", expiryDate: getFutureDate(14), vendor: "樂活農莊" },
            { id: "F0009", name: "胡蘿蔔", price: 60, category: "蔬菜", imageUrl: "https://images.unsplash.com/photo-1447175008436-8123782ca61d?w=400", calories: 70, origin: "韓國", storage: "冷藏", expiryDate: getFutureDate(8), vendor: "家香廚坊" },
            { id: "F0010", name: "洋蔥", price: 50, category: "蔬菜", imageUrl: "https://images.unsplash.com/photo-1618512496248-a07fe83aa829?w=400", calories: 60, origin: "美國", storage: "常溫", expiryDate: getFutureDate(20), vendor: "每日良品" }
        ];

        let recipeDatabase = [
            { id: 1, name: "綜合蔬果沙拉", calories: 220, img: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", ingredients: ["番茄", "菠菜", "洋蔥", "蘋果"], steps: ["菠菜洗淨瀝乾，番茄、蘋果切塊。", "將所有食材放入大碗中。", "淋上橄欖油、檸檬汁、鹽攪拌均勻。"] },
            { id: 2, name: "蜂蜜烤地瓜", calories: 280, img: "https://images.unsplash.com/photo-1596393332966-09105923c6d6?w=400", ingredients: ["地瓜"], steps: ["將地瓜洗淨，不需要削皮。", "烤箱 200°C 烤 30-40 分鐘。", "取出切開淋上蜂蜜。"] },
            { id: 3, name: "鳳梨蘋果汁", calories: 240, img: "https://images.unsplash.com/photo-1603569283847-aa295f0d016a?w=400", ingredients: ["鳳梨", "蘋果"], steps: ["鳳梨與蘋果去皮切塊。", "放入果汁機加適量開水。", "攪打均勻即可飲用。"] },
            { id: 4, name: "番茄炒高麗菜", calories: 190, img: "https://images.unsplash.com/photo-1598155523122-3842334d6c10?w=400", ingredients: ["番茄", "高麗菜"], steps: ["高麗菜洗淨切塊，番茄切塊。", "熱鍋爆香蒜末，先炒番茄。", "加入高麗菜快炒，加鹽調味。"] },
            { id: 5, name: "香蕉柳橙冰沙", calories: 225, img: "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=400", ingredients: ["香蕉", "柳橙"], steps: ["香蕉剝皮切塊，柳橙去皮取肉。", "加入冰塊放入果汁機。", "攪打至綿密冰沙狀。"] },
            { id: 6, name: "義式烤蔬菜", calories: 200, img: "https://images.unsplash.com/photo-1590301157890-4810ed35db42?w=400", ingredients: ["胡蘿蔔", "洋蔥", "地瓜"], steps: ["蔬菜切滾刀塊。", "淋上橄欖油、鹽、義式香料拌勻。", "平鋪烤盤，200°C 烤 20-25 分鐘。"] }
        ];

        // --- 購物車邏輯 ---
        let cart = []; 
        function addToCart(id) {
            const p = productDatabase.find(x => x.id === id);
            if(!p) return;
            const item = cart.find(x => x.id === id);
            if(item) item.quantity++; else cart.push({id:p.id, name:p.name, price:p.price, quantity:1});
            updateCartUI();
            showToast(`🛒 已將「${p.name}」加入購物車！`);
        }
        function increaseQuantity(i) { cart[i].quantity++; updateCartUI(); }
        function decreaseQuantity(i) { if(cart[i].quantity > 1) cart[i].quantity--; else if(confirm(`確定要移除「${cart[i].name}」嗎？`)) { cart.splice(i, 1); showToast("🗑️ 已移除商品"); } updateCartUI(); }
        function removeFromCart(i) { if(confirm(`確定要移除「${cart[i].name}」嗎？`)) { cart.splice(i, 1); showToast("🗑️ 已移除商品"); updateCartUI(); } }

        function updateCartUI() {
            const total = cart.reduce((sum, i) => sum + i.quantity, 0);
            document.getElementById('cart-badge').textContent = total;
            const list = document.getElementById('cart-items-list');
            if(cart.length===0) { list.innerHTML = '<p class="empty-msg">購物車是空的</p>'; document.getElementById('cart-total-price').textContent = 'NT$ 0'; return; }
            let html = '', amount = 0;
            cart.forEach((item, i) => {
                const sub = item.price * item.quantity;
                amount += sub;
                html += `<div class="list-item"><div class="item-info"><div class="item-name">${item.name}</div><div class="item-price">NT$ ${item.price.toFixed(0)} / 個</div></div><div class="item-controls"><button class="qty-btn" onclick="decreaseQuantity(${i})">-</button><span class="item-qty">${item.quantity}</span><button class="qty-btn" onclick="increaseQuantity(${i})">+</button><button class="remove-btn" onclick="removeFromCart(${i})">🗑️</button></div></div>`;
            });
            list.innerHTML = html;
            document.getElementById('cart-total-price').textContent = `NT$ ${amount.toFixed(0)}`;
        }

        // --- 食譜本邏輯 ---
        let myRecipes = [];
        window.toggleRecipe = function(recipeName, btnElement) {
            const index = myRecipes.indexOf(recipeName);
            if (index === -1) { myRecipes.push(recipeName); btnElement.textContent = "✅ 已收藏"; btnElement.classList.add("saved"); showToast("✅ 已新增至您的食譜本！"); }
            else { myRecipes.splice(index, 1); btnElement.textContent = "➕ 收藏食譜"; btnElement.classList.remove("saved"); showToast("🗑️ 已從食譜本移除"); }
            updateRecipeBookUI();
        };
        window.removeRecipeFromBook = function(recipeName) {
            const index = myRecipes.indexOf(recipeName);
            if(index > -1) { myRecipes.splice(index, 1); updateRecipeBookUI(); }
        }
        function updateRecipeBookUI() {
            document.getElementById('recipe-book-badge').textContent = myRecipes.length;
            const list = document.getElementById('recipe-book-list');
            if(myRecipes.length === 0) { list.innerHTML = '<p class="empty-msg">尚未收藏任何食譜</p>'; return; }
            let html = '';
            myRecipes.forEach(name => { html += `<div class="list-item"><div class="item-name">${name}</div><button class="remove-btn" onclick="removeRecipeFromBook('${name}')">🗑️</button></div>`; });
            list.innerHTML = html;
        }

        // --- 食譜功能 ---
        window.addIngredient = function(recipeId, inputId) {
            const r = recipeDatabase.find(x => x.id === recipeId);
            const input = document.getElementById(inputId);
            const newVal = input.value.trim();
            if(newVal && r) { r.ingredients.push(newVal); input.value = ''; reloadDetail(r.name); }
        };
        window.removeIngredient = function(recipeId, ingIndex) {
            const r = recipeDatabase.find(x => x.id === recipeId);
            if(r) { r.ingredients.splice(ingIndex, 1); reloadDetail(r.name); }
        };
        window.generateStepsFromIngredients = function(recipeId) {
            const r = recipeDatabase.find(x => x.id === recipeId);
            if(!r || r.ingredients.length===0) { showToast("⚠️ 請先加入一些食材！"); return; }
            const main = r.ingredients[0], others = r.ingredients.slice(1).join('、');
            r.name = `特製${main}${others?'佐'+others:''}風味餐`;
            r.steps = [`將 ${r.ingredients.join('、')} 準備好並清洗乾淨。`, `將 ${main} 切成適口大小備用。`, `熱鍋後，依序放入 ${r.ingredients.join('、')} 進行拌炒或烹煮。`, `加入適量調味料，確認食材熟透後即可盛盤。`];
            reloadDetail(r.name);
            showToast("✨ 食譜內容已更新！");
        };
        window.autoGenerateRecipe = function(productName) {
            const t = [{ title: `涼拌${productName}`, steps: [`將${productName}洗淨切好。`, "準備一碗冰水浸泡保持脆度。", "加入醋、糖、少許鹽巴拌勻。", "撒上一些芝麻即可享用。"] }, { title: `香煎${productName}`, steps: [`將${productName}切成薄片。`, "平底鍋加入奶油熱鍋。", `放入${productName}煎至兩面金黃。`, "撒上黑胡椒粒即可。"] }, { title: `清炒${productName}`, steps: [`${productName}切塊備用。`, "熱鍋爆香蒜頭。", `放入${productName}大火快炒。`, "加點水悶熟，起鍋前調味。"] }];
            const tmpl = t[Math.floor(Math.random()*t.length)];
            const p = productDatabase.find(p => p.name === productName);
            // 如果是生成食譜，圖片使用該商品的圖片
            const newRecipe = { id: Date.now(), name: tmpl.title, calories: Math.floor(Math.random()*200+100), img: p?p.imageUrl:"https://via.placeholder.com/400?text=Recipe", ingredients: [productName, "鹽", "油"], steps: tmpl.steps };
            recipeDatabase.push(newRecipe);
            reloadDetail(productName);
            showToast(`🎉 已新增至食譜：「${newRecipe.name}」！`);
        };
        function reloadDetail(refName) { const btn = document.getElementById('detail-add-btn'); if(btn) showDetailPage(btn.getAttribute('data-current-product-id')); }

        // --- (新) LINE Bot 邏輯 ---
        let botRules = [
            { keyword: "營業時間", response: "我們的營業時間是每天 08:00 - 22:00 喔！" },
            { keyword: "地址", response: "我們位於台北市信義區快樂路 123 號。" },
            { keyword: "電話", response: "客服專線：02-1234-5678" },
            { keyword: "優惠", response: "現在蘋果、香蕉都在特價中，快來搶購！" }
        ];
        function renderBotRules() {
            const tbody = document.getElementById('bot-rules-list');
            let html = '';
            botRules.forEach((rule, index) => { html += `<tr><td>${rule.keyword}</td><td>${rule.response}</td><td><button class="admin-action-btn btn-delete" onclick="deleteBotRule(${index})">刪除</button></td></tr>`; });
            tbody.innerHTML = html;
        }
        window.addBotRule = function() {
            const kw = document.getElementById('new-kw').value.trim();
            const resp = document.getElementById('new-reply').value.trim();
            if(kw && resp) { botRules.push({ keyword: kw, response: resp }); document.getElementById('new-kw').value = ''; document.getElementById('new-reply').value = ''; renderBotRules(); showToast("✨ 規則已新增"); }
        };
        window.deleteBotRule = function(index) { botRules.splice(index, 1); renderBotRules(); };

        // 前台聊天傳送
        window.sendChatMsg = function() {
            const input = document.getElementById('chat-msg-input');
            const msg = input.value.trim();
            if(!msg) return;
            const chatArea = document.getElementById('chat-display');
            chatArea.innerHTML += `<div class="msg msg-user">${msg}</div>`;
            input.value = '';
            chatArea.scrollTop = chatArea.scrollHeight;
            setTimeout(() => {
                let reply = "抱歉，我不太懂您的意思，您可以輸入「營業時間」或「地址」試試看。";
                const match = botRules.find(r => msg.includes(r.keyword));
                if(match) reply = match.response;
                chatArea.innerHTML += `<div class="msg msg-bot">${reply}</div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
            }, 600);
        };

        // --- 後台管理邏輯 ---
        function renderAdminProductList() {
            const tbody = document.getElementById('admin-product-list');
            let html = '';
            productDatabase.forEach((p, index) => { html += `<tr><td><img src="${p.imageUrl}" alt="${p.name}"></td><td>${p.id}</td><td>${p.name}</td><td>${p.category}</td><td>${p.price}</td><td><button class="admin-action-btn btn-delete" onclick="deleteProduct(${index})">刪除</button></td></tr>`; });
            tbody.innerHTML = html;
        }
        window.deleteProduct = function(index) { if(confirm("確定要刪除此商品嗎？")) { productDatabase.splice(index, 1); renderAdminProductList(); showToast("🗑️ 商品已刪除"); } };
        window.addNewProduct = function() {
            const name = document.getElementById('new-p-name').value;
            const price = parseFloat(document.getElementById('new-p-price').value);
            const category = document.getElementById('new-p-category').value;
            if(!name || !price) { alert("請輸入完整資訊"); return; }
            const newId = "F" + (productDatabase.length + 1).toString().padStart(4, '0');
            productDatabase.push({ id: newId, name: name, price: price, category: category, imageUrl: "https://via.placeholder.com/150?text=" + name, calories: 100, origin: "台灣", storage: "常溫", expiryDate: getFutureDate(7), vendor: "自有品牌" });
            document.getElementById('new-p-name').value = ''; document.getElementById('new-p-price').value = ''; renderAdminProductList(); showToast("✨ 商品新增成功！");
        };
        window.switchAdminTab = function(tab) {
            document.querySelectorAll('.admin-tab-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById('admin-products-section').style.display = tab==='products'?'block':'none';
            document.getElementById('admin-bot-section').style.display = tab==='bot'?'block':'none';
            document.getElementById('admin-orders-section').style.display = tab==='orders'?'block':'none';
            if(tab === 'bot') renderBotRules();
        };

        // --- 頁面顯示 ---
        const listPage = document.getElementById('list-page');
        const detailPage = document.getElementById('detail-page');
        const backendPage = document.getElementById('backend-page');
        const fabContainer = document.getElementById('fab-container-right');

        function showListPage() { detailPage.style.display = 'none'; backendPage.style.display = 'none'; fabContainer.style.display = 'flex'; document.getElementById('recipe-book-fab').style.display = 'flex'; listPage.style.display = 'block'; window.scrollTo(0, 0); }
        function showBackendPage() { listPage.style.display = 'none'; detailPage.style.display = 'none'; fabContainer.style.display = 'none'; document.getElementById('recipe-book-fab').style.display = 'none'; backendPage.style.display = 'block'; renderAdminProductList(); window.scrollTo(0, 0); }

        function showDetailPage(id) {
            const p = productDatabase.find(x => x.id === id);
            if(!p) return;
            document.getElementById('detail-image').src = p.imageUrl;
            document.getElementById('detail-name').textContent = p.name;
            document.getElementById('detail-price').textContent = `NT$ ${p.price.toFixed(0)}`;
            document.getElementById('detail-origin').textContent = p.origin;
            document.getElementById('detail-expiry').textContent = p.expiryDate;
            document.getElementById('recipe-ingredient-name').textContent = p.name;
            const daysLeft = calculateDaysLeft(p.expiryDate);
            const statusSpan = document.getElementById('detail-days-left-status');
            if (daysLeft < 0) { statusSpan.textContent = `⚠️ 已過期 (${Math.abs(daysLeft)} 天)`; statusSpan.style.color = "#d9534f"; } 
            else if (daysLeft <= 3) { statusSpan.textContent = `🔥 即將到期 (剩 ${daysLeft} 天)`; statusSpan.style.color = "#f0ad4e"; } 
            else { statusSpan.textContent = `✅ 有效 (剩 ${daysLeft} 天)`; statusSpan.style.color = "#5cb85c"; }
            document.getElementById('detail-add-btn').setAttribute('data-current-product-id', id);
            document.querySelector('.back-to-list-btn').onclick = showListPage;
            document.getElementById('detail-add-btn').onclick = () => addToCart(p.id);
            const recipesContainer = document.getElementById('related-recipes-container');
            let recipesHtml = '';
            const matchedRecipes = recipeDatabase.filter(r => r.ingredients.some(i => i.includes(p.name)) || r.name.includes(p.name));
            if (matchedRecipes.length > 0) {
                matchedRecipes.forEach((r) => {
                    const isSaved = myRecipes.includes(r.name);
                    const btnText = isSaved ? "✅ 已收藏" : "➕ 收藏食譜";
                    const btnClass = isSaved ? "save-recipe-btn saved" : "save-recipe-btn";
                    const uniqueInputId = `new-ing-${r.id}`;
                    const ingListHtml = r.ingredients.map((ing, i) => `<li class="ingredient-item"><span class="ingredient-name">${ing}</span><span class="del-ing-btn" onclick="removeIngredient(${r.id}, ${i})">&times;</span></li>`).join('');
                    recipesHtml += `<div class="recipe-card"><img src="${r.img}" alt="${r.name}" class="recipe-card-img"><div class="recipe-content"><h3>${r.name}</h3><p class="recipe-calories">🔥 約 ${r.calories} 大卡</p><h4>所需食材：</h4><ul class="ingredient-list">${ingListHtml}</ul><div class="add-ing-row"><input type="text" id="${uniqueInputId}" class="add-ing-input" placeholder="輸入食材..."><button class="add-ing-btn" onclick="addIngredient(${r.id}, '${uniqueInputId}')">+</button></div><button class="magic-generate-btn" onclick="generateStepsFromIngredients(${r.id})">⚡ 根據上方食材生成新食譜</button><h4>步驟：</h4><ol>${r.steps.map(step => `<li>${step}</li>`).join('')}</ol><button class="${btnClass}" onclick="toggleRecipe('${r.name}', this)">${btnText}</button></div></div>`;
                });
            } else {
                recipesHtml = `<div class="no-recipe-box"><h3>😞 目前尚無「${p.name}」的相關食譜</h3><p>您可以嘗試自動生成！</p><button class="generate-btn" onclick="autoGenerateRecipe('${p.name}')">✨ AI 幫我想食譜</button></div>`;
            }
            recipesContainer.innerHTML = recipesHtml;
            listPage.style.display = 'none'; detailPage.style.display = 'block'; window.scrollTo(0, 0);
        }

        document.addEventListener('DOMContentLoaded', function() {
            const container = document.getElementById('product-list-container');
            let html = '';
            productDatabase.forEach(p => {
                const daysLeft = calculateDaysLeft(p.expiryDate);
                let tagHtml = daysLeft < 0 ? `<span class="tag expired-tag">⚠️ 已過期</span>` : `<span class="tag expiry-tag">剩 ${daysLeft} 天</span>`;
                html += `<div class="product-card"><img src="${p.imageUrl}" alt="${p.name}" class="product-card-img" onclick="showDetailPage('${p.id}')"><div class="card-content"><h3>${p.name}</h3><p class="price">NT$ ${p.price.toFixed(0)}</p><p><span class="tag">${p.category}</span>${tagHtml}</p><div class="card-actions"><button class="view-detail-btn" data-id="${p.id}">詳情</button><button class="view-recipe-btn" data-id="${p.id}">👨‍🍳 食譜</button><button class="add-to-cart-btn" data-id="${p.id}">+ 加入</button></div></div></div>`;
            });
            container.innerHTML = html;

            container.addEventListener('click', e => {
                const id = e.target.getAttribute('data-id');
                if(e.target.classList.contains('view-detail-btn')) showDetailPage(id);
                if(e.target.classList.contains('add-to-cart-btn')) addToCart(id);
                if(e.target.classList.contains('view-recipe-btn')) { showDetailPage(id); setTimeout(() => { document.getElementById('related-recipes-section').scrollIntoView({ behavior: 'smooth' }); }, 100); }
            });

            document.getElementById('backend-entry-btn').onclick = showBackendPage;
            document.getElementById('back-store-btn').onclick = showListPage;

            const cartModal = document.getElementById('cart-modal');
            document.getElementById('cart-fab').onclick = () => cartModal.style.display = 'flex';
            cartModal.querySelector('.close-modal-btn').onclick = () => cartModal.style.display = 'none';
            cartModal.onclick = e => { if(e.target === cartModal) cartModal.style.display = 'none'; };

            const recipeModal = document.getElementById('recipe-book-modal');
            document.getElementById('recipe-book-fab').onclick = () => recipeModal.style.display = 'flex';
            recipeModal.querySelector('.close-modal-btn').onclick = () => recipeModal.style.display = 'none';
            recipeModal.onclick = e => { if(e.target === recipeModal) recipeModal.style.display = 'none'; };
            
            const chatWidget = document.getElementById('chat-widget');
            document.getElementById('chat-fab').onclick = () => chatWidget.style.display = 'flex';
            chatWidget.querySelector('.close-chat-btn').onclick = () => chatWidget.style.display = 'none';
        });
    </script>
</body>
</html>
"""

# 3. 渲染 HTML 元件 (這步最關鍵，讓它在 Streamlit 中執行)
# height 設定為 1000 確保有足夠空間顯示長頁面
components.html(html_code, height=1000, scrolling=True)
