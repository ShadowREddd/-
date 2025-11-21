import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 👇 您的 GitHub 資訊
# ==========================================
GITHUB_USER = "ShadowREddd"   
REPO_NAME = "-"     
BRANCH_NAME = "main"            

# 指向根目錄
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH_NAME}/"
# ==========================================

st.set_page_config(page_title="食際行動家", layout="wide", initial_sidebar_state="collapsed")

html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>食際行動家</title>
    <style>
        /* --- 基礎設定 --- */
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { 
            font-family: "Microsoft JhengHei", -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f4f6f8; margin: 0; 
            padding-bottom: 80px; overflow-x: hidden;
        }
        :root { --primary: #d9534f; --text: #333; --bg: #fff; }

        /* RWD */
        .desktop-only { display: none !important; }
        .mobile-only { display: flex !important; }
        @media (min-width: 768px) {
            body { padding-bottom: 0; padding-top: 70px; }
            .desktop-only { display: flex !important; }
            .mobile-only { display: none !important; }
        }

        /* --- 1. 登入封面 --- */
        #splash { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background: white; z-index: 99999; 
            display: flex; flex-direction: column; justify-content: center; align-items: center; 
            transition: opacity 0.5s ease-out; overflow: hidden; cursor: pointer;
        }
        .splash-logo { 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            object-fit: cover; object-position: center;
            animation: breathe 3s infinite; z-index: -1;
        }
        @keyframes breathe { 0%, 100% { transform: scale(1); opacity: 0.95; } 50% { transform: scale(1.02); opacity: 1; } }

        /* --- 2. 登入頁面 --- */
        #login-page {
            display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: #fff; z-index: 8000;
            flex-direction: column; justify-content: center; align-items: center;
            padding: 20px; animation: fadeIn 0.5s;
        }
        .login-card { width: 100%; max-width: 400px; text-align: center; }
        .login-logo { width: 120px; margin-bottom: 20px; }
        .login-title { font-size: 1.8rem; margin-bottom: 30px; color: #333; }
        .login-input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-size: 1rem; background: #f9f9f9; }
        .login-btn { width: 100%; padding: 15px; background: var(--primary); color: white; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: bold; cursor: pointer; }
        .login-footer { margin-top: 20px; color: #999; font-size: 0.9rem; }

        /* --- 3. 主程式 --- */
        #main-app { display: none; opacity: 0; transition: opacity 0.5s; }

        /* 導覽列 */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 65px;
            background: white; justify-content: space-around; align-items: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05); z-index: 5000; border-top: 1px solid #eee;
        }
        .nav-item { flex: 1; text-align: center; color: #999; font-size: 0.75rem; background:none; border:none; cursor: pointer; }
        .nav-item.active { color: var(--primary); font-weight: bold; }
        .nav-icon { font-size: 1.4rem; display: block; margin-bottom: 2px; }

        .top-nav {
            position: fixed; top: 0; left: 0; width: 100%; height: 70px;
            background: white; justify-content: space-between; align-items: center;
            padding: 0 50px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); z-index: 5000;
        }
        .back-home-btn { font-size: 1.1rem; font-weight: bold; color: #666; cursor: pointer; display: flex; align-items: center; gap: 8px; }
        .desktop-menu button { background: none; border: none; font-size: 1rem; margin-left: 20px; cursor: pointer; color: #666; }
        .desktop-menu button:hover, .desktop-menu button.active { color: var(--primary); font-weight: bold; }
        .cart-btn-desktop { background: var(--primary) !important; color: white !important; padding: 8px 20px; border-radius: 20px; }

        /* 橫幅 */
        .container { max-width: 1200px; margin: 0 auto; padding: 15px; }
        .banner-container {
            width: 100%; height: 180px; border-radius: 15px; margin-bottom: 20px;
            display: flex; align-items: center; justify-content: center; overflow: hidden;
            position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .banner-img { width: 100%; height: 100%; object-fit: cover; }
        @media (min-width: 768px) { .banner-container { height: 300px; } }

        /* 分類 */
        .category-bar { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 15px; scrollbar-width: none; }
        .category-bar::-webkit-scrollbar { display: none; }
        .cat-btn { white-space: nowrap; padding: 8px 16px; border-radius: 20px; border: 1px solid #ddd; background: white; color: #666; cursor: pointer; }
        .cat-btn.active { background: var(--primary); color: white; border-color: var(--primary); }

        /* 網格 & 卡片 (完全重寫 CSS 以修復點擊) */
        .grid { display: grid; gap: 15px; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); }
        
        .card { 
            background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
            cursor: pointer; /* 關鍵：滑鼠變手型 */
            transition: transform 0.2s; display: flex; flex-direction: column;
            position: relative;
        }
        .card:active { transform: scale(0.98); background-color: #f9f9f9; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        
        /* 移除 pointer-events: none，讓點擊事件自然冒泡 */
        .card-img { width: 100%; height: 150px; object-fit: cover; }
        .card-body { padding: 10px; flex-grow: 1; display: flex; flex-direction: column; }
        
        .card-title { font-weight: bold; margin-bottom: 5px; color: #333; }
        .price { color: var(--primary); font-weight: bold; font-size: 1.1rem; margin-top: auto; }
        
        .status-badge { display: inline-block; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; margin-bottom: 5px; }
        .status-good { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status-bad { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }

        /* 按鈕群組 */
        .card-actions { display: flex; gap: 5px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee; }
        
        /* 按鈕樣式 */
        .btn-card-action { 
            flex: 1; padding: 8px; border-radius: 6px; font-size: 0.85rem; 
            cursor: pointer; border: none; font-weight: bold; transition: 0.2s;
        }
        .btn-outline-sm { background: white; border: 1px solid #ddd; color: #555; }
        .btn-outline-sm:hover { background: #f0f0f0; }
        .btn-primary-sm { background: var(--primary); color: white; }
        .btn-primary-sm:hover { background: #c9302c; }

        .gen-recipe-btn {
            margin-top: 5px; width: 100%; padding: 8px; 
            background: #e3f2fd; border: 1px solid #90caf9; color: #1976d2;
            border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-weight: bold;
        }
        .gen-recipe-btn:hover { background: #bbdefb; }

        /* 詳情頁 */
        .page { display: none; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .detail-wrapper { display: flex; flex-direction: column; background: white; border-radius: 0; }
        @media (min-width: 768px) {
            .detail-wrapper { flex-direction: row; border-radius: 20px; padding: 40px; gap: 40px; margin-top: 20px; }
            .detail-hero { flex: 1; }
            .detail-hero img { border-radius: 15px; height: 400px !important; }
            .detail-info { flex: 1; padding: 0 !important; margin-top: 0 !important; }
            .back-btn { top: 90px !important; left: 40px !important; }
        }
        .detail-hero { position: relative; }
        .detail-hero img { width: 100%; height: 300px; object-fit: cover; }
        .detail-info { padding: 20px; background: white; border-radius: 20px 20px 0 0; margin-top: -20px; position: relative; }
        .back-btn { position: absolute; top: 20px; left: 20px; width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.9); border:none; z-index: 10; font-size:1.2rem; cursor:pointer;}
        .detail-status-tag { display: inline-block; padding: 5px 10px; border-radius: 4px; font-size: 0.9rem; font-weight: bold; }

        /* Modals */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 6000; }
        .modal-content { position: absolute; bottom: 0; left: 0; width: 100%; max-height: 85vh; background: white; border-radius: 20px 20px 0 0; padding: 20px; display: flex; flex-direction: column; animation: slideUp 0.3s; }
        @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
        @media (min-width: 768px) {
            .modal { align-items: center; justify-content: center; }
            .modal-content { position: relative; width: 500px; border-radius: 15px; bottom: auto; left: auto; animation: fadeIn 0.3s; }
        }

        /* Admin & Form */
        .admin-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        .admin-table th, .admin-table td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        .form-group { margin-bottom: 15px; }
        .form-label { display: block; font-weight: bold; margin-bottom: 5px; color: #333; }
        .form-input, .form-select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; }
        .add-row { display: flex; gap: 10px; margin-bottom: 10px; }
        .add-btn-small { background: var(--primary); color: white; border: none; border-radius: 8px; width: 40px; cursor: pointer; font-size: 1.2rem; }
        .tag-container { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px; background: #f9f9f9; border-radius: 8px; min-height: 50px; }
        .ing-tag { background: white; border: 1px solid #ddd; padding: 5px 12px; border-radius: 20px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px; }
        .ing-tag span { color: #d9534f; cursor: pointer; font-weight: bold; margin-left: 5px; }
        .step-list, .ing-list { padding-left: 20px; margin: 0; color: #444; line-height: 1.6; }
        .ing-list { list-style-type: disc; margin-bottom: 15px; }
        .step-list li, .ing-list li { margin-bottom: 5px; }
        h4 { margin: 15px 0 8px 0; color: var(--primary); border-bottom: 1px solid #eee; padding-bottom: 5px; }
        .btn { width: 100%; padding: 12px; border-radius: 10px; border: none; font-weight: bold; font-size: 1rem; margin-top: 10px; cursor: pointer; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-outline { background: white; border: 1px solid #ddd; color: #555; }
        .tag { background: #eee; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; color: #666; }
        .mobile-top-bar { display: flex; align-items: center; padding: 10px 5px; margin-bottom: 10px; }
        .qty-btn { width: 28px; height: 28px; border-radius: 50%; border: 1px solid #ddd; background: white; font-weight: bold; cursor: pointer; display:flex; align-items:center; justify-content:center;}
        .del-btn { color: #d9534f; background: none; border: none; cursor: pointer; font-size: 1.2rem; margin-left: 5px; }
        
        /* 自訂食譜 AI 按鈕 */
        .ai-magic-btn {
            width: 100%; padding: 12px; margin-bottom: 15px;
            background: linear-gradient(45deg, #17a2b8, #2c3e50); 
            color: white; border: none; border-radius: 10px; font-weight: bold; font-size: 1rem;
            cursor: pointer; box-shadow: 0 4px 10px rgba(23, 162, 184, 0.3);
            display: flex; align-items: center; justify-content: center; gap: 10px;
        }
        .ai-magic-btn:hover { filter: brightness(1.1); transform:translateY(-2px); transition:0.2s; }

        /* Chat & Admin */
        .chat-fab { position: fixed; bottom: 80px; right: 20px; z-index: 5500; width: 60px; height: 60px; border-radius: 50%; background: #2c3e50; color: white; border: none; font-size: 1.8rem; cursor: pointer; }
        @media (min-width: 768px) { .chat-fab { bottom: 30px; right: 30px; } }
        #chat-widget { display: none; position: fixed; bottom: 150px; right: 20px; width: 320px; height: 450px; background: #fff; border-radius: 15px; box-shadow: 0 5px 25px rgba(0,0,0,0.2); z-index: 5600; flex-direction: column; }
        @media (min-width: 768px) { #chat-widget { bottom: 100px; right: 30px; } }
        .chat-header { background: #2c3e50; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .chat-body { flex: 1; padding: 15px; overflow-y: auto; background: #f4f6f8; display: flex; flex-direction: column; gap: 10px; }
        .chat-input-area { padding: 10px; background: white; border-top: 1px solid #eee; display: flex; gap: 5px; }
        .msg { max-width: 80%; padding: 10px; border-radius: 15px; font-size: 0.9rem; }
        .msg-bot { align-self: flex-start; background: white; border: 1px solid #eee; }
        .msg-user { align-self: flex-end; background: #d9fdd3; }

    </style>
</head>
<body>

    <div id="splash" onclick="goToLogin()">
        <img src="images/食際行動家.png" class="splash-logo">
    </div>

    <div id="login-page" style="display:none;">
        <div class="login-card">
            <img src="images/食際行動家.png" class="login-logo">
            <div class="login-title">歡迎回來</div>
            <input type="text" class="login-input" placeholder="使用者帳號">
            <input type="password" class="login-input" placeholder="密碼">
            <button class="login-btn" onclick="performLogin()">登入</button>
            <div class="login-footer">或使用 Google / Facebook 登入</div>
        </div>
    </div>

    <div id="main-app">
        <button class="chat-fab" onclick="toggleChat()">💬</button>

        <div id="chat-widget">
            <div class="chat-header"><span style="font-weight:bold;">線上客服</span><span onclick="toggleChat()" style="cursor:pointer;">✕</span></div>
            <div class="chat-body" id="chat-body"><div class="msg msg-bot">您好！請問有什麼需要幫忙的嗎？🥦</div></div>
            <div class="chat-input-area"><input type="text" id="chat-input" class="form-input" placeholder="輸入訊息..." onkeypress="if(event.key==='Enter') sendChat()"><button class="add-btn-small" onclick="sendChat()" style="width:60px; font-size:0.9rem;">傳送</button></div>
        </div>

        <div class="top-nav desktop-only">
            <div class="back-home-btn" onclick="location.reload()"><span style="font-size:1.5rem;">⬅</span> 登出</div>
            <div class="desktop-menu">
                <button id="dt-nav-market" class="active" onclick="switchPage('market')">生鮮市集</button>
                <button id="dt-nav-recipe" onclick="switchPage('recipe')">食譜牆</button>
                <button class="cart-btn-desktop" onclick="openModal('cart')">購物車 (<span class="cart-count-num">0</span>)</button>
            </div>
        </div>

        <div class="container">
            <div id="page-market" class="page" style="display:block;">
                <div class="mobile-top-bar mobile-only">
                    <div class="back-home-btn" onclick="location.reload()"><span style="font-size:1.3rem;">⬅</span> 登出</div>
                </div>
                <div class="banner-container"><img src="images/食際行動家.png" class="banner-img"></div>
                <div class="category-bar" id="cat-bar">
                    <button class="cat-btn" onclick="filterCat('水果', this)">🍎 水果</button>
                    <button class="cat-btn" onclick="filterCat('蔬菜', this)">🥦 蔬菜</button>
                    <button class="cat-btn" onclick="filterCat('菇類', this)">🍄 菇類</button>
                    <button class="cat-btn" onclick="filterCat('肉品', this)">🥩 肉品</button>
                    <button class="cat-btn" onclick="filterCat('海鮮', this)">🐟 海鮮</button>
                </div>
                <div id="grid-products" class="grid">
                    <div style="grid-column:1/-1; text-align:center; padding:50px; color:#888;"><div style="font-size:3rem; margin-bottom:10px;">🥦🍎🥩</div><div style="font-size:1.2rem;">請點擊上方分類開始選購</div></div>
                </div>
            </div>

            <div id="page-recipe" class="page">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <h2>食譜牆</h2>
                    <div style="display:flex; gap:10px;">
                        <input type="text" id="recipe-search" placeholder="搜尋食譜..." oninput="filterRecipes()" style="padding:8px; border:1px solid #ddd; border-radius:20px; outline:none;">
                        <button class="btn-outline" style="width:auto; padding:8px 20px;" onclick="openCreateRecipeModal()">＋ 自訂</button>
                    </div>
                </div>
                <div id="grid-recipes" class="grid"></div>
            </div>

            <div id="page-detail" class="page">
                <button class="back-btn" onclick="switchPage('market')">←</button>
                <div class="detail-wrapper">
                    <div class="detail-hero"><img id="dt-img" src=""></div>
                    <div class="detail-info">
                        <h1 id="dt-name" style="margin:0; font-size:1.8rem;"></h1>
                        <div style="margin:10px 0;">
                            <span id="dt-condition-badge"></span>
                            <span id="dt-price" style="color:#d9534f; font-size:1.5rem; font-weight:bold; float:right;"></span>
                        </div>
                        <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
                        <p style="color:#666; line-height:1.8; font-size:1.1rem;">
                            📍 <strong>產地：</strong><span id="dt-origin"></span><br>
                            ❄️ <strong>保存：</strong><span id="dt-storage"></span><br>
                            📅 <strong>到期：</strong><span id="dt-expiry"></span><br>
                            👀 <strong>外觀：</strong><span id="dt-condition-text" class="detail-status-tag"></span>
                        </p>
                        <div style="display:flex; gap:10px; margin-top:30px;">
                            <button class="btn btn-primary" onclick="addToCart()">＋ 加入購物車</button>
                            <button class="btn btn-outline" onclick="quickGenerateRecipeDetail()">➕ 加入食譜</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="page-backend" class="page">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                    <h2>⚙️ 後台管理系統</h2>
                    <button class="btn-outline" style="width:auto;" onclick="switchPage('market')">返回前台</button>
                </div>
                <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 2px 10px rgba(0,0,0,0.05);">
                    <h3>📦 庫存管理</h3>
                    <table class="admin-table">
                        <thead><tr><th>名稱</th><th>狀態</th><th>價格</th><th>操作</th></tr></thead>
                        <tbody id="admin-list"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="bottom-nav mobile-only">
            <button class="nav-item active" id="mb-nav-market" onclick="switchPage('market')"><span class="nav-icon">🥦</span>市集</button>
            <button class="nav-item" id="mb-nav-recipe" onclick="switchPage('recipe')"><span class="nav-icon">👨‍🍳</span>食譜</button>
            <button class="nav-item" onclick="openModal('cart')"><span class="nav-icon">🛒<span class="cart-count-num" style="font-size:0.8rem; color:#d9534f; vertical-align:top;">0</span></span>購物車</button>
        </div>

    </div>

    <div id="modal-cart" class="modal" onclick="if(event.target===this) closeModal('cart')">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;"><h3 style="margin:0;">我的購物車</h3><span onclick="closeModal('cart')" style="cursor:pointer; font-size:1.5rem;">✕</span></div>
            <div id="cart-list" style="flex:1; overflow-y:auto; min-height:150px;"></div>
            <div style="border-top:1px solid #eee; padding-top:15px; margin-top:10px;">
                <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:1.2rem;"><span>總計</span><span id="cart-total">$0</span></div>
                <button class="btn btn-primary" onclick="alert('結帳成功！'); cart=[]; updateCartUI(); closeModal('cart')">前往結帳</button>
            </div>
        </div>
    </div>

    <div id="modal-step" class="modal" onclick="if(event.target===this) closeModal('step')">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;"><h3 style="margin:0;" id="step-title">料理步驟</h3><span onclick="closeModal('step')" style="cursor:pointer; font-size:1.5rem;">✕</span></div>
            <div id="step-body" style="flex:1; overflow-y:auto; line-height:1.8;"></div>
            <button class="btn btn-outline" onclick="closeModal('step')">關閉</button>
        </div>
    </div>

    <div id="modal-create" class="modal" onclick="if(event.target===this) closeModal('create')">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;"><h3 style="margin:0;">新增私房食譜</h3><span onclick="closeModal('create')" style="cursor:pointer; font-size:1.5rem;">✕</span></div>
            <div style="flex:1; overflow-y:auto; padding-right:5px;">
                <div class="form-group"><label class="form-label">食譜名稱</label><input type="text" id="new-r-name" class="form-input" placeholder="例如：阿嬤的紅燒肉"></div>
                <div class="form-group"><label class="form-label">預估卡路里</label><input type="number" id="new-r-cal" class="form-input" placeholder="例如：500"></div>
                <div class="form-group"><label class="form-label">選擇食材 (從市集)</label><div class="add-row"><select id="product-select" class="form-select"><option value="">-- 請選擇食材 --</option></select><button class="add-btn-small" onclick="addIngredientFromSelect()">＋</button></div></div>
                <div class="form-group"><label class="form-label">或 手動輸入</label><div class="add-row"><input type="text" id="manual-ing-input" class="form-input" placeholder="例如：鹽、醬油..."><button class="add-btn-small" onclick="addManualIngredient()">＋</button></div></div>
                <div id="new-ing-list" class="tag-container"><span style="color:#999; font-size:0.9rem;">尚未加入食材</span></div>
                <div class="form-group" style="margin-top:15px;"><label class="form-label">步驟</label><div class="add-row"><input type="text" id="new-step-input" class="form-input" placeholder="輸入步驟..."><button class="add-btn-small" onclick="addNewStep()">＋</button></div><div id="new-step-list" style="background:#f9f9f9; padding:10px; border-radius:8px; min-height:50px;"></div></div>
            </div>
            <div style="margin-top:10px; border-top:1px solid #eee; padding-top:10px;">
                <button class="ai-magic-btn" onclick="autoGenerateRichRecipe()">🎲 AI 隨機生成創意食譜</button>
                <button class="btn btn-primary" onclick="saveCustomRecipe()">✨ 發布食譜</button>
            </div>
        </div>
    </div>

    <script>
        function getFutureDate(d) { const date = new Date(); date.setDate(date.getDate()+d); return date.toISOString().split('T')[0]; }

        const products = [
            { id: "P1", name: "蘋果", price: 139, img: "images/蘋果.jpg", cat: "水果", origin: "美國", storage: "冷藏", date: getFutureDate(6), condition: "良好" },
            { id: "P2", name: "香蕉", price: 80, img: "images/香蕉.jpg", cat: "水果", origin: "台灣", storage: "常溫", date: getFutureDate(3), condition: "破損" },
            { id: "P7", name: "柳橙", price: 120, img: "images/柳橙.JPG", cat: "水果", origin: "美國", storage: "冷藏", date: getFutureDate(10), condition: "良好" },
            { id: "P10", name: "鳳梨", price: 155, img: "images/鳳梨.jpg", cat: "水果", origin: "美國", storage: "冷凍", date: getFutureDate(5), condition: "良好" },
            { id: "P3", name: "高麗菜", price: 160, img: "images/高麗菜.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(7), condition: "良好" },
            { id: "P4", name: "番茄", price: 70, img: "images/番茄.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(5), condition: "破損" },
            { id: "P5", name: "洋蔥", price: 50, img: "images/洋蔥.jpg", cat: "蔬菜", origin: "美國", storage: "常溫", date: getFutureDate(20), condition: "良好" },
            { id: "P6", name: "地瓜", price: 190, img: "images/地瓜.jpg", cat: "蔬菜", origin: "台灣", storage: "常溫", date: getFutureDate(14), condition: "良好" },
            { id: "P8", name: "菠菜", price: 90, img: "images/菠菜.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(2), condition: "破損" },
            { id: "P9", name: "胡蘿蔔", price: 60, img: "images/胡蘿蔔.jpg", cat: "蔬菜", origin: "韓國", storage: "冷藏", date: getFutureDate(8), condition: "良好" },
            { id: "P11", name: "花椰菜", price: 55, img: "https://images.unsplash.com/photo-1568584711075-3d021a7c3d54?w=400", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(5), condition: "良好" },
            { id: "P12", name: "甜玉米", price: 40, img: "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(7), condition: "良好" },
            { id: "P14", name: "彩椒", price: 45, img: "https://images.unsplash.com/photo-1563565375-f3fdf5ecfae9?w=400", cat: "蔬菜", origin: "荷蘭", storage: "冷藏", date: getFutureDate(12), condition: "良好" },
            { id: "P15", name: "馬鈴薯", price: 35, img: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400", cat: "蔬菜", origin: "美國", storage: "常溫", date: getFutureDate(30), condition: "破損" },
            { id: "P13", name: "鮮香菇", price: 65, img: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400", cat: "菇類", origin: "台灣", storage: "冷藏", date: getFutureDate(10), condition: "良好" },
            { id: "P16", name: "豬肉", price: 220, img: "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400", cat: "肉品", origin: "台灣", storage: "冷凍", date: getFutureDate(30), condition: "良好" },
            { id: "P17", name: "牛肉", price: 450, img: "https://images.unsplash.com/photo-1613482184648-47399b2df699?w=400", cat: "肉品", origin: "美國", storage: "冷凍", date: getFutureDate(30), condition: "良好" },
            { id: "P20", name: "鮭魚切片", price: 350, img: "https://images.unsplash.com/photo-1599084993091-1cb5c0721cc6?w=400", cat: "海鮮", origin: "挪威", storage: "冷凍", date: getFutureDate(15) }
        ];

        const allRecipes = [
            { id: "R1", name: "綜合蔬果沙拉", cal: 220, img: "images/綜合蔬果沙拉.jpg", steps: ["所有食材洗淨切塊", "加入橄欖油與鹽拌勻"], ingredients: ["蘋果", "番茄", "洋蔥"] },
            { id: "R2", name: "番茄炒高麗菜", cal: 180, img: "images/番茄炒高麗菜.jpg", steps: ["熱鍋爆香", "加入番茄炒軟", "加入高麗菜炒熟"], ingredients: ["番茄", "高麗菜"] },
            { id: "R3", name: "蜂蜜烤地瓜", cal: 250, img: "images/蜂蜜烤地瓜.jpg", steps: ["洗淨", "200度烤40分鐘"], ingredients: ["地瓜"] },
            { id: "R4", name: "鳳梨蘋果汁", cal: 150, img: "images/鳳梨蘋果汁.jpg", steps: ["切塊", "加水打成汁"], ingredients: ["鳳梨", "蘋果"] },
            { id: "R5", name: "香蕉柳橙冰沙", cal: 180, img: "images/香蕉柳橙冰沙.jpg", steps: ["加冰塊", "打成冰沙"], ingredients: ["香蕉", "柳橙"] },
            { id: "R6", name: "義式烤蔬菜", cal: 200, img: "images/義式烤蔬菜.jpg", steps: ["切塊", "撒上香料烤熟"], ingredients: ["胡蘿蔔", "洋蔥"] },
            {
                id: "Hidden1", name: "奶油酪梨雞胸肉佐蒜香地瓜葉", cal: 450, img: "https://images.unsplash.com/photo-1606756790138-7c48643e2912?w=400", hidden: true,
                ingredients: ["雞胸肉 (250g)", "酪梨 1 顆", "地瓜葉 1 把", "牛奶/豆漿 100ml", "洋蔥 1/4 顆", "蒜頭 3-4 瓣"],
                steps: ["雞胸肉切塊，加鹽、黑胡椒、橄欖油醃 10 分鐘。", "熱鍋煎雞胸肉至金黃，盛起備用。", "原鍋炒香洋蔥丁與蒜末，加入酪梨肉壓成泥。", "倒入牛奶煮成濃滑醬汁，加鹽調味。", "放回雞肉煨煮 1-2 分鐘即可。", "另起鍋爆香蒜片，快炒地瓜葉，加鹽調味。"]
            }
        ];

        let cart = [];
        let currentPid = null;
        let tempIngredients = [];
        let tempSteps = [];

        function init() {
            const defaultRecipes = allRecipes.filter(r => !r.hidden);
            renderRecipes(defaultRecipes);
        }

        function goToLogin() {
            const s = document.getElementById('splash');
            const l = document.getElementById('login-page');
            s.style.opacity=0; setTimeout(() => { s.style.display='none'; l.style.display='flex'; }, 500);
        }
        function performLogin() {
            const l = document.getElementById('login-page');
            const a = document.getElementById('main-app');
            l.style.opacity=0; setTimeout(() => { l.style.display='none'; a.style.display='block'; setTimeout(()=>a.style.opacity=1,50); if(window.innerWidth<768)document.body.style.paddingBottom='80px'; else document.body.style.paddingTop='70px'; }, 500);
        }

        function renderProducts(list) {
            if(!list || list.length===0) { document.getElementById('grid-products').innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:50px; color:#888;"><div style="font-size:3rem;">🥦🍎🥩</div><div>請點擊上方分類開始選購</div></div>'; return; }
            document.getElementById('grid-products').innerHTML = list.map(p => {
                let badgeClass = p.condition === '良好' ? 'status-good' : 'status-bad';
                let badgeText = p.condition === '良好' ? '✅ 外觀良好' : '⚠️ 外觀破損';
                
                // onclick 綁定在最外層 div，按鈕區阻止冒泡
                return `
                <div class="card" onclick="showDetail('${p.id}')">
                    <div class="card-click-area">
                        <img src="${p.img}" class="card-img">
                        <div class="card-body">
                            <div class="card-title">${p.name}</div>
                            <div><span class="status-badge ${badgeClass}">${badgeText}</span></div>
                            <div class="price">$${p.price}</div>
                        </div>
                    </div>
                    
                    <div class="card-body" style="padding-top:0; pointer-events:auto;">
                        <div class="card-actions">
                             <button class="btn-card-action btn-outline-sm" onclick="event.stopPropagation(); showDetail('${p.id}')">📄 詳細</button>
                             <button class="btn-card-action btn-primary-sm" onclick="event.stopPropagation(); addToCart('${p.id}')">🛒 加入</button>
                        </div>
                        <button class="gen-recipe-btn" onclick="event.stopPropagation(); quickGenerateRecipe('${p.name}')">➕ 加入食譜</button>
                    </div>
                </div>`;
            }).join('');
        }

        function quickGenerateRecipe(name) {
            const newR = {
                id: "Auto" + Date.now(),
                name: "特製" + name + "料理",
                cal: 300,
                img: "https://via.placeholder.com/300?text=" + name,
                ingredients: [name, "鹽", "油"],
                steps: ["將" + name + "洗淨切好", "大火快炒", "調味後起鍋"]
            };
            allRecipes.unshift(newR);
            switchPage('recipe');
            showStep(newR.id);
        }
        
        function quickGenerateRecipeDetail() {
            const p = products.find(x => x.id === currentPid);
            quickGenerateRecipe(p.name);
        }

        function filterCat(cat, btn) {
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if(cat==='all') renderProducts(products);
            else renderProducts(products.filter(p => p.cat === cat));
        }

        function filterRecipes() {
            const kw = document.getElementById('recipe-search').value.trim();
            const filtered = allRecipes.filter(r => {
                if (r.hidden) return kw.includes("酪梨");
                if (!kw) return true;
                return r.name.includes(kw) || (r.ingredients && r.ingredients.some(i => i.includes(kw)));
            });
            renderRecipes(filtered);
        }

        function renderRecipes(list) {
            if(!list || list.length===0) { document.getElementById('grid-recipes').innerHTML = '<div style="text-align:center; color:#999; grid-column:1/-1; padding:20px;">找不到食譜... 試試「酪梨」？</div>'; return; }
            document.getElementById('grid-recipes').innerHTML = list.map(r => `
                <div class="card" onclick="showStep('${r.id}')">
                    <img src="${r.img}" class="card-img" onerror="this.src='https://via.placeholder.com/300?text=${r.name}'">
                    <div class="card-body">
                        <div class="card-title">${r.name}</div>
                        <div style="color:#666; font-size:0.9rem;">🔥 ${r.cal} kcal</div>
                        <button class="btn-outline-sm btn-card-action" style="margin-top:10px;">查看做法</button>
                    </div>
                </div>`).join('');
        }

        function switchPage(page) {
            document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelectorAll('.desktop-menu button').forEach(n => n.classList.remove('active'));
            if(document.getElementById('mb-nav-'+page)) document.getElementById('mb-nav-'+page).classList.add('active');
            if(document.getElementById('dt-nav-'+page)) document.getElementById('dt-nav-'+page).classList.add('active');
            document.getElementById('page-'+page).style.display = 'block';
            if(page==='recipe') { document.getElementById('recipe-search').value=''; renderRecipes(allRecipes.filter(r=>!r.hidden)); }
            if(page==='market') { 
                if(document.getElementById('grid-products').innerHTML.includes('請點擊上方')) { } 
                else { } 
            }
            window.scrollTo(0,0);
        }

        function showDetail(pid) {
            currentPid = pid;
            const p = products.find(x => x.id === pid);
            document.getElementById('dt-img').src = p.img;
            document.getElementById('dt-name').innerText = p.name;
            document.getElementById('dt-price').innerText = '$' + p.price;
            document.getElementById('dt-origin').innerText = p.origin;
            document.getElementById('dt-storage').innerText = p.storage;
            document.getElementById('dt-expiry').innerText = p.date;
            document.getElementById('dt-tag').innerText = p.cat;
            
            const conditionText = document.getElementById('dt-condition-text');
            conditionText.innerText = p.condition === '良好' ? '✅ 外觀良好，適合送禮或直接食用' : '⚠️ 外觀有輕微破損，建議盡快食用或加工';
            conditionText.style.color = p.condition === '良好' ? '#28a745' : '#dc3545';
            conditionText.className = p.condition === '良好' ? 'detail-status-tag status-good' : 'detail-status-tag status-bad';

            switchPage('detail');
        }

        function addToCart(optId) {
            const targetId = optId || currentPid;
            if(!targetId) return;
            const p = products.find(x => x.id === targetId);
            const item = cart.find(x => x.id === targetId);
            if(item) item.qty++; else cart.push({id:p.id, name:p.name, price:p.price, qty:1});
            updateCartUI();
            alert('✅ 已加入購物車');
        }
        
        function changeQty(id, delta) {
            const item = cart.find(x => x.id === id);
            if (!item) return;
            item.qty += delta;
            if (item.qty <= 0) {
                if(confirm('確定要移除此商品嗎？')) {
                    cart = cart.filter(x => x.id !== id);
                } else {
                    item.qty = 1; // 恢復
                }
            }
            updateCartUI();
        }

        function removeFromCart(id) {
            if(confirm('確定要移除此商品嗎？')) {
                cart = cart.filter(x => x.id !== id);
                updateCartUI();
            }
        }

        function updateCartUI() {
            const count = cart.reduce((sum, i) => sum + i.qty, 0);
            const total = cart.reduce((sum, i) => sum + i.price*i.qty, 0);
            document.querySelectorAll('.cart-count-num').forEach(el => el.innerText = count);
            document.getElementById('cart-total').innerText = '$' + total;
            
            if (cart.length === 0) {
                document.getElementById('cart-list').innerHTML = '<p style="text-align:center; color:#999;">購物車是空的</p>';
            } else {
                document.getElementById('cart-list').innerHTML = cart.map(item => `
                    <div class="cart-item">
                        <div class="cart-info">
                            <div class="cart-name">${item.name}</div>
                            <div class="cart-price">$${item.price} / 個</div>
                        </div>
                        <div class="cart-controls">
                            <button class="qty-btn" onclick="changeQty('${item.id}', -1)">-</button>
                            <span style="font-weight:bold; min-width:20px; text-align:center;">${item.qty}</span>
                            <button class="qty-btn" onclick="changeQty('${item.id}', 1)">+</button>
                            <button class="del-btn" onclick="removeFromCart('${item.id}')">🗑️</button>
                        </div>
                    </div>
                `).join('');
            }
        }

        function showStep(rid) {
            const r = allRecipes.find(x => x.id === rid);
            document.getElementById('step-title').innerText = r.name;
            let html = '<h4>🍽 食材</h4><ul class="ing-list">' + (r.ingredients?r.ingredients.map(i=>`<li>${i}</li>`).join(''):'<li>無資料</li>') + '</ul>';
            html += '<h4>👩‍🍳 做法</h4><ol class="step-list">' + (r.steps?r.steps.map(s=>`<li>${s}</li>`).join(''):'<li>無資料</li>') + '</ol>';
            document.getElementById('step-body').innerHTML = html;
            openModal('step');
        }
        
        function findRecipe() {
            const p = products.find(x => x.id === currentPid);
            alert(`正在搜尋「${p.name}」食譜...`);
            switchPage('recipe');
            setTimeout(() => {
                const searchInput = document.getElementById('recipe-search');
                if(searchInput) { searchInput.value = p.name; filterRecipes(); }
            }, 100);
        }

        function toggleChat() { const w = document.getElementById('chat-widget'); w.style.display = (w.style.display === 'flex') ? 'none' : 'flex'; }
        function sendChat() {
            const input = document.getElementById('chat-input'); const msg = input.value.trim(); if(!msg) return;
            const body = document.getElementById('chat-body'); body.innerHTML += `<div class="msg msg-user">${msg}</div>`; input.value = ''; body.scrollTop = body.scrollHeight;
            if(msg === '[後台]') { setTimeout(() => { body.innerHTML += `<div class="msg msg-bot">驗證成功，跳轉後台...</div>`; setTimeout(() => { toggleChat(); showBackend(); }, 1000); }, 500); return; }
            setTimeout(() => { body.innerHTML += `<div class="msg msg-bot">收到！我們將盡快回覆。</div>`; body.scrollTop = body.scrollHeight; }, 800);
        }
        function showBackend() { switchPage('backend'); renderAdmin(); }
        function renderAdmin() { document.getElementById('admin-list').innerHTML = products.map(p => `<tr><td>${p.name}</td><td>${p.condition}</td><td>$${p.price}</td><td><button style="color:red;border:none;background:none;cursor:pointer;" onclick="alert('刪除')">刪除</button></td></tr>`).join(''); }

        function openCreateRecipeModal() {
            document.getElementById('new-r-name').value = ''; document.getElementById('new-r-cal').value = '';
            tempIngredients = []; tempSteps = []; updateCustomPreview();
            document.getElementById('product-select').innerHTML = '<option value="">-- 請選擇食材 --</option>' + products.map(p => `<option value="${p.name}">${p.name}</option>`).join('');
            openModal('create');
        }
        function addIngredientFromSelect() { const v = document.getElementById('product-select').value; if(v && !tempIngredients.includes(v)) { tempIngredients.push(v); updateCustomPreview(); } }
        function addManualIngredient() { const v = document.getElementById('manual-ing-input').value.trim(); if(v) { tempIngredients.push(v); document.getElementById('manual-ing-input').value = ''; updateCustomPreview(); } }
        function addNewStep() { const v = document.getElementById('new-step-input').value.trim(); if(v) { tempSteps.push(v); document.getElementById('new-step-input').value=''; updateCustomPreview(); } }
        function updateCustomPreview() {
            document.getElementById('new-ing-list').innerHTML = tempIngredients.length ? tempIngredients.map((ing, i) => `<div class="ing-tag">${ing} <span onclick="tempIngredients.splice(${i},1);updateCustomPreview()">✕</span></div>`).join('') : '尚未加入';
            document.getElementById('new-step-list').innerHTML = tempSteps.length ? tempSteps.map((s, i) => `<div style="border-bottom:1px dashed #ddd; padding:5px 0; display:flex; justify-content:space-between;"><span>${i+1}. ${s}</span><span onclick="tempSteps.splice(${i},1);updateCustomPreview()" style="color:red;cursor:pointer;">✕</span></div>`).join('') : '無步驟';
        }

        // --- 智慧 AI 食譜生成 (連續隨機版) ---
        function autoGenerateRichRecipe() {
            if (tempIngredients.length === 0) {
                alert("⚠️ 請先選擇至少一種食材，AI 才能幫您想食譜！");
                return;
            }
            
            const mainIng = tempIngredients[0];
            
            const templates = [
                {
                    getName: (ing) => "塔香爆炒" + ing,
                    getSteps: (ing) => [
                        `將${ing}切成適口大小，蒜頭拍碎備用。`,
                        "熱鍋下油，放入蒜末爆香至金黃色。",
                        `轉大火，放入${ing}快速翻炒。`,
                        "加入醬油、糖、米酒調味，起鍋前放入九層塔提香。"
                    ],
                    extraIng: ["蒜頭", "九層塔", "醬油"]
                },
                {
                    getName: (ing) => "清蒸檸檬" + ing,
                    getSteps: (ing) => [
                        `將${ing}洗淨擺盤，鋪上薑片去腥。`,
                        "淋上米酒與魚露，放入蒸鍋大火蒸 10 分鐘。",
                        "取出後撒上蔥絲與辣椒絲。",
                        "淋上熱油激發香氣，最後擠上新鮮檸檬汁。"
                    ],
                    extraIng: ["薑片", "蔥絲", "檸檬"]
                },
                {
                    getName: (ing) => "家常紅燒" + ing,
                    getSteps: (ing) => [
                        `將${ing}切塊，放入滾水中汆燙去血水。`,
                        "熱鍋炒糖色，放入食材翻炒上色。",
                        "加入醬油、八角、水，小火慢燉 40 分鐘。",
                        "湯汁收乾至濃稠即可起鍋。"
                    ],
                    extraIng: ["八角", "冰糖", "醬油"]
                },
                {
                    getName: (ing) => "爽口涼拌" + ing,
                    getSteps: (ing) => [
                        `將${ing}切絲或切片，滾水汆燙後冰鎮。`,
                        "準備醬汁：蒜泥、醋、糖、香油拌勻。",
                        "將醬汁淋在食材上，撒上白芝麻。",
                        "放入冰箱冷藏 30 分鐘入味後食用。"
                    ],
                    extraIng: ["蒜泥", "白芝麻", "香油"]
                }
            ];

            const randomTemplate = templates[Math.floor(Math.random() * templates.length)];

            document.getElementById('new-r-name').value = randomTemplate.getName(mainIng);
            document.getElementById('new-r-cal').value = Math.floor(Math.random() * 400) + 200; 
            
            tempSteps = randomTemplate.getSteps(mainIng);
            
            randomTemplate.extraIng.forEach(ing => {
                if(!tempIngredients.includes(ing)) tempIngredients.push(ing);
            });

            updateCustomPreview();
        }

        function saveCustomRecipe() {
            const name = document.getElementById('new-r-name').value.trim();
            const cal = document.getElementById('new-r-cal').value;
            const hasAvocado = name.includes("酪梨") || tempIngredients.some(i => i.includes("酪梨"));
            const hasChicken = name.includes("雞胸肉") || tempIngredients.some(i => i.includes("雞胸肉"));
            if (hasAvocado && hasChicken) {
                alert("🥑🍗 恭喜！發現隱藏料理：奶油酪梨雞胸肉佐蒜香地瓜葉！");
                const unlocked = { ...allRecipes.find(r => r.id === "Hidden1"), id: "Unlocked_" + Date.now(), hidden: false };
                allRecipes.unshift(unlocked); closeModal('create'); document.getElementById('recipe-search').value = ''; renderRecipes(allRecipes.filter(r => !r.hidden)); return;
            }
            if(!name || tempIngredients.length===0 || tempSteps.length===0) { alert("請填寫完整！"); return; }
            allRecipes.unshift({id: "C"+Date.now(), name: name, img: "https://via.placeholder.com/300?text="+name, cal: cal||0, steps: [...tempSteps], ingredients: [...tempIngredients]});
            alert("✨ 發布成功！"); closeModal('create'); document.getElementById('recipe-search').value = ''; renderRecipes(allRecipes.filter(r => !r.hidden));
        }

        function openModal(id) { const m = document.getElementById('modal-'+id); m.style.display = (window.innerWidth >= 768) ? 'flex' : 'block'; }
        function closeModal(id) { document.getElementById('modal-'+id).style.display = 'none'; }

        window.onload = init;
    </script>
</body>
</html>
