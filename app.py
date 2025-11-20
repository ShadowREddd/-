import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 👇 【請修改這裡】您的 GitHub 資訊
# ==========================================
GITHUB_USER = "您的GitHub帳號"   
REPO_NAME = "您的儲存庫名稱"     
BRANCH_NAME = "main"            

# 自動生成圖片路徑
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH_NAME}/"
# ==========================================

# 1. 設定頁面 (加入 initial_sidebar_state="collapsed" 讓手機版空間更大)
st.set_page_config(
    page_title="食際行動家", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>蔬果</title>
    
    <style>
        /* --- 全域設定 --- */
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        html { scroll-behavior: smooth; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f0f2f5;
            padding-bottom: 100px;
            margin: 0;
            overflow-x: hidden;
            font-size: 16px; /* 手機版預設字體 */
        }
        h1 { text-align: center; color: #333; margin: 15px 0; }
        button { cursor: pointer; transition: transform 0.1s, background-color 0.3s; touch-action: manipulation; }
        button:active { transform: scale(0.95); }
        input:focus, textarea:focus, select:focus { outline: 2px solid #d9534f; }

        /* --- 廣告/歡迎頁 --- */
        #splash-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: #ffffff; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: transform 0.6s cubic-bezier(0.7, 0, 0.3, 1); 
            cursor: pointer; 
        }
        #splash-screen.hidden { transform: translateY(-100%); }
        .splash-logo { width: 80%; max-width: 600px; object-fit: contain; animation: breathe 3s infinite; }
        @keyframes breathe { 0%, 100% { transform: scale(0.98); opacity: 0.9; } 50% { transform: scale(1.02); opacity: 1; } }
        .click-hint { position: absolute; bottom: 80px; color: #999; font-size: 1.2rem; animation: blink 2s infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* --- 導覽列 --- */
        .nav-header { text-align: center; margin-bottom: 20px; padding-top: 10px; position: relative; }
        .logo-container img { max-width: 150px; height: auto; display: block; margin: 0 auto 10px auto; }
        .nav-header h2 { color: #d9534f; margin: 0; font-size: 1.5rem; }
        .backend-entry-btn {
            position: absolute; right: 10px; top: 10px;
            background: rgba(255,255,255,0.8); border: 1px solid #ccc;
            padding: 5px 10px; border-radius: 20px; color: #666; font-size: 0.8rem;
        }

        /* --- 商品列表 (Grid) --- */
        #product-list-container {
            display: grid;
            /* 手機預設 2 欄，螢幕夠寬才變多欄 */
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 15px;
            padding: 10px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .product-card {
            background: #fff; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex; flex-direction: column; overflow: hidden;
        }
        .product-card-img { width: 100%; height: 140px; object-fit: cover; }
        .card-content { padding: 10px; display: flex; flex-direction: column; flex-grow: 1; }
        .card-content h3 { font-size: 1rem; margin: 0 0 5px 0; color: #333; }
        .card-content p { font-size: 0.85rem; margin: 3px 0; color: #666; }
        .card-content .price { font-size: 1.1rem; color: #000; font-weight: bold; margin-top: auto; }
        
        .card-actions { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; margin-top: 10px; }
        .card-actions button { padding: 6px 0; font-size: 0.8rem; border-radius: 6px; border: none; color: white; }
        .view-detail-btn { background: #6c757d; }
        .view-recipe-btn { background: #f0ad4e; }
        .add-to-cart-btn { background: #d9534f; }

        .tag { display: inline-block; background: #5cb85c; color: white; padding: 2px 6px; border-radius: 10px; font-size: 0.75rem; margin-right: 3px; }
        .expiry-tag { background: #f0ad4e; }
        .expired-tag { background: #d9534f; }

        /* --- 詳情頁 --- */
        #detail-page { display: none; padding: 10px; }
        .detail-main-card { background: #fff; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        #detail-image { width: 100%; height: 300px; object-fit: cover; }
        .detail-content { padding: 20px; }
        .back-to-list-btn { margin-bottom: 15px; border: 1px solid #999; background: white; padding: 8px 20px; border-radius: 20px; }
        
        /* --- 手機版特別優化 (Media Queries) --- */
        @media (max-width: 768px) {
            #product-list-container { gap: 10px; padding: 10px; }
            .product-card-img { height: 130px; }
            .card-actions { grid-template-columns: 1fr; gap: 8px; } /* 按鈕改為垂直排列 */
            .card-actions button { padding: 10px 0; font-size: 0.9rem; } /* 加大按鈕 */
            
            /* 詳情頁圖片變小一點 */
            #detail-image { height: 250px; }
            
            /* 購物車/食譜 Modal 滿版 */
            .modal-panel { width: 95%; height: 85vh; }
            
            /* 聊天視窗滿版 */
            #chat-widget { width: 90%; right: 5%; bottom: 90px; height: 60vh; }
            
            /* FAB 按鈕調整 */
            .fab-btn { width: 60px; height: 60px; font-size: 1.6rem; }
            #fab-container-right { right: 20px; bottom: 20px; }
            #recipe-book-fab { left: 20px; bottom: 20px; width: 60px; height: 60px; }
        }

        /* --- 其他通用樣式 (Modal/Toast/Chat) --- */
        .related-recipes-section { margin-top: 30px; border-top: 1px dashed #ccc; padding-top: 20px; }
        .recipe-card { margin-bottom: 20px; border: 1px solid #eee; border-radius: 10px; overflow: hidden; }
        .recipe-card-img { width: 100%; height: 160px; object-fit: cover; }
        .recipe-content { padding: 15px; }
        
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 2000; justify-content: center; align-items: center; }
        .modal-panel { background: white; width: 90%; max-width: 500px; border-radius: 15px; display: flex; flex-direction: column; max-height: 90vh; }
        .modal-header { padding: 15px; background: #333; color: white; display: flex; justify-content: space-between; align-items: center; }
        .modal-body { padding: 15px; overflow-y: auto; flex: 1; }
        .modal-footer { padding: 15px; border-top: 1px solid #eee; }
        .list-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
        
        /* Toast */
        #toast-container { position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%); z-index: 3001; display: flex; flex-direction: column; gap: 8px; width: 80%; pointer-events: none; }
        .toast { background: rgba(0,0,0,0.8); color: white; padding: 10px 20px; border-radius: 25px; text-align: center; opacity: 0; transition: opacity 0.3s; }
        .toast.show { opacity: 1; }

        /* Admin Table 手機橫向捲軸 */
        .admin-table { width: 100%; border-collapse: collapse; min-width: 600px; } /* 強制最小寬度 */
        #admin-products-section { overflow-x: auto; } /* 允許滑動 */
        .admin-table th, .admin-table td { padding: 10px; border-bottom: 1px solid #eee; text-align: left; }
        
        /* Chat */
        #chat-widget { display: none; position: fixed; bottom: 110px; right: 30px; width: 320px; height: 450px; background: #f1f1f1; z-index: 2000; flex-direction: column; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .chat-area { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 8px 12px; border-radius: 15px; max-width: 80%; font-size: 0.95rem; }
        .msg-user { align-self: flex-end; background: #98e165; }
        .msg-bot { align-self: flex-start; background: white; }
        .chat-input-area { display: flex; padding: 10px; background: white; border-top: 1px solid #ddd; }
        .chat-input { flex: 1; padding: 8px; border-radius: 20px; border: 1px solid #ddd; margin-right: 5px; }

        /* FABs */
        #fab-container-right { position: fixed; bottom: 30px; right: 30px; display: flex; flex-direction: column; gap: 15px; z-index: 1000; }
        .fab-btn, #recipe-book-fab { width: 65px; height: 65px; border-radius: 50%; border: none; color: white; font-size: 1.8rem; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; }
        #cart-fab { background: #d9534f; }
        #chat-fab { background: #2c3e50; }
        #recipe-book-fab { position: fixed; bottom: 30px; left: 30px; background: #5cb85c; z-index: 1000; }
        .fab-badge { position: absolute; top: -5px; right: -5px; background: #333; color: white; width: 24px; height: 24px; border-radius: 50%; font-size: 0.8rem; display: flex; justify-content: center; align-items: center; border: 2px solid white; }
        
        /* 後台表單 RWD */
        .admin-form { display: grid; grid-template-columns: 1fr; gap: 10px; background: #f9f9f9; padding: 15px; margin-bottom: 15px; }
        @media (min-width: 600px) { .admin-form { grid-template-columns: 1fr 1fr 1fr auto; } }

        /* 按鈕樣式補強 */
        .magic-generate-btn { width: 100%; padding: 12px; background: linear-gradient(45deg, #6f42c1, #8e44ad); color: white; border: none; border-radius: 8px; margin-bottom: 10px; }
        .save-recipe-btn { width: 100%; padding: 12px; border: 1px solid #5cb85c; background: white; color: #5cb85c; border-radius: 20px; }
        .save-recipe-btn.saved { background: #5cb85c; color: white; }
    </style>
</head>
<body>

    <div id="splash-screen" onclick="enterSite()">
        <img src="images/食際行動家.png" alt="食際行動家" class="splash-logo" onerror="this.style.display='none'; this.parentElement.innerHTML+='<h2 style=\\'color:#d9534f;font-size:2.5rem;\\'>食際行動家</h2>'">
        <div class="click-hint">👆 點擊進入</div>
    </div>

    <div class="nav-header">
        <div class="logo-container">
            <img src="images/食際行動家.png" alt="食際行動家 Logo" onerror="this.style.display='none'">
        </div>
        <h2>🛒 蔬果專區</h2>
        <button class="backend-entry-btn" id="backend-entry-btn">⚙️ 後台</button>
    </div>

    <div id="list-page">
        <div id="product-list-container"></div>
    </div>
    
    <div id="detail-page">
        <button class="back-to-list-btn">← 返回列表</button>
        
        <div class="detail-main-card">
            <img id="detail-image" src="" alt="商品圖片" onerror="this.src='https://via.placeholder.com/600x400?text=No+Image'">
            <div class="detail-content">
                <h1 id="detail-name">商品名稱</h1>
                <div id="detail-tags"></div>
                <p class="price" id="detail-price" style="text-align: center; margin: 10px 0;">NT$ 0</p>
                
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <button class="add-to-cart-btn" id="detail-add-btn" style="flex:1.5; padding: 12px; color:white; border:none; border-radius:8px;">+ 加入購物車</button>
                    <button id="favButton" style="flex: 1; background: #fff; border: 1px solid #ccc; color: #d9534f; border-radius:8px;">❤️ 收藏</button>
                </div>

                <div id="detail-info">
                    <p><strong>來源:</strong> <span id="detail-origin"></span></p>
                    <p><strong>到期日:</strong> <span id="detail-expiry"></span></p>
                    <p style="margin-top: 10px;">🕒 狀態：<span id="detail-days-left-status" style="font-weight: bold;"></span></p>
                </div>

                <div class="related-recipes-section" id="related-recipes-section">
                    <h2>💡 創意料理：<span id="recipe-ingredient-name"></span></h2>
                    <div id="related-recipes-container"></div>
                </div>
            </div>
        </div>
    </div>

    <div id="backend-page">
        <div class="admin-container" style="background:white; padding:15px; border-radius:10px;">
            <div class="admin-header" style="display:flex; justify-content:space-between; margin-bottom:15px;">
                <h2 style="margin:0;">⚙️ 後台</h2>
                <button class="back-store-btn" id="back-store-btn" style="background:#666; color:white; border:none; padding:5px 15px; border-radius:15px;">← 返回</button>
            </div>
            
            <div class="admin-tabs" style="display:flex; gap:10px; margin-bottom:15px; overflow-x:auto;">
                <button class="admin-tab-btn active" onclick="switchAdminTab('products')" style="flex:1; padding:10px; border:1px solid #ccc;">商品</button>
                <button class="admin-tab-btn" onclick="switchAdminTab('bot')" style="flex:1; padding:10px; border:1px solid #ccc;">機器人</button>
                <button class="admin-tab-btn" onclick="switchAdminTab('orders')" style="flex:1; padding:10px; border:1px solid #ccc;">訂單</button>
            </div>
            
            <div id="admin-products-section">
                <div class="admin-form">
                    <input type="text" id="new-p-name" placeholder="名稱" style="padding:8px;">
                    <input type="number" id="new-p-price" placeholder="價格" style="padding:8px;">
                    <select id="new-p-category" style="padding:8px;"><option value="水果">水果</option><option value="蔬菜">蔬菜</option></select>
                    <button onclick="addNewProduct()" style="background:#5cb85c; color:white; border:none; padding:8px;">+ 新增</button>
                </div>
                <table class="admin-table">
                    <thead><tr><th>圖片</th><th>名稱</th><th>分類</th><th>價格</th><th>操作</th></tr></thead>
                    <tbody id="admin-product-list"></tbody>
                </table>
            </div>

            <div id="admin-bot-section" style="display: none;">
                <div class="admin-form">
                    <input type="text" id="new-kw" placeholder="關鍵字" style="padding:8px;">
                    <input type="text" id="new-reply" placeholder="回覆內容" style="padding:8px;">
                    <button onclick="addBotRule()" style="background:#5cb85c; color:white; border:none; padding:8px;">新增規則</button>
                </div>
                <table class="admin-table">
                    <thead><tr><th>關鍵字</th><th>回覆內容</th><th>操作</th></tr></thead>
                    <tbody id="bot-rules-list"></tbody>
                </table>
            </div>

            <div id="admin-orders-section" style="display: none;">
                <p style="text-align: center; color: #666; margin-top: 50px;">無訂單。</p>
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
            <div class="modal-header" style="background:#d9534f;"><h2>購物車</h2><button class="close-modal-btn" style="background:none;border:none;color:white;font-size:1.5rem;">&times;</button></div>
            <div class="modal-body" id="cart-items-list"><p style="text-align:center;color:#999;">空空如也</p></div>
            <div class="modal-footer">
                <div class="cart-total" style="display:flex; justify-content:space-between; font-weight:bold; margin-bottom:10px;"><span>總計:</span><span id="cart-total-price">NT$ 0</span></div>
                <button style="width:100%; padding:15px; background:#d9534f; color:white; border:none; border-radius:8px;" onclick="alert('感謝購買！')">結帳</button>
            </div>
        </div>
    </div>

    <div id="recipe-book-modal" class="modal">
        <div class="modal-panel">
            <div class="modal-header" style="background:#5cb85c;"><h2>食譜本</h2><button class="close-modal-btn" style="background:none;border:none;color:white;font-size:1.5rem;">&times;</button></div>
            <div class="modal-body" id="recipe-book-list"><p style="text-align:center;color:#999;">無收藏</p></div>
            <div class="modal-footer">
                <button style="width:100%; padding:10px; background:#5cb85c; color:white; border:none; border-radius:8px;" onclick="document.getElementById('recipe-book-modal').style.display='none'">關閉</button>
            </div>
        </div>
    </div>

    <div id="chat-widget">
        <div class="modal-header" style="background:#2c3e50;">
            <h3 style="margin:0;font-size:1rem;">客服</h3>
            <button class="close-chat-btn" onclick="document.getElementById('chat-widget').style.display='none'" style="background:none;border:none;color:white;">&times;</button>
        </div>
        <div class="chat-area" id="chat-display">
            <div class="msg msg-bot">您好！需要幫忙嗎？🥦</div>
        </div>
        <div class="chat-input-area">
            <input type="text" class="chat-input" id="chat-msg-input" placeholder="輸入..." onkeypress="if(event.key==='Enter') sendChatMsg()">
            <button class="chat-send-btn" onclick="sendChatMsg()" style="background:none;border:none;color:#2c3e50;font-weight:bold;">傳送</button>
        </div>
    </div>

    <div id="toast-container"></div>

    <script>
        // --- 核心 JS 邏輯 (與之前相同) ---
        function enterSite() {
            const splash = document.getElementById('splash-screen');
            splash.classList.add('hidden');
            setTimeout(() => splash.style.display = 'none', 800);
        }

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

        let productDatabase = [
            { id: "F0001", name: "蘋果", price: 138.4, category: "水果", imageUrl: "images/蘋果.jpg", calories: 90, origin: "美國", storage: "冷凍", expiryDate: getFutureDate(6), vendor: "每日良品" },
            { id: "F0002", name: "香蕉", price: 80, category: "水果", imageUrl: "images/香蕉.jpg", calories: 105, origin: "台灣", storage: "常溫", expiryDate: getFutureDate(3), vendor: "樂活農莊" },
            { id: "F0003", name: "鳳梨", price: 155, category: "水果", imageUrl: "images/鳳梨.jpg", calories: 150, origin: "美國", storage: "冷凍", expiryDate: getFutureDate(5), vendor: "綠源生技" },
            { id: "F0004", name: "高麗菜", price: 161.4, category: "蔬菜", imageUrl: "images/高麗菜.jpg", calories: 50, origin: "台灣", storage: "冷藏", expiryDate: getFutureDate(7), vendor: "安心食堂" },
            { id: "F0005", name: "番茄", price: 70, category: "蔬菜", imageUrl: "images/番茄.jpg", calories: 30, origin: "台灣", storage: "冷藏", expiryDate: getFutureDate(4), vendor: "綠源生技" },
            { id: "F0006", name: "菠菜", price: 90, category: "蔬菜", imageUrl: "images/菠菜.jpg", calories: 40, origin: "台灣", storage: "冷藏", expiryDate: getFutureDate(2), vendor: "樂活農莊" },
            { id: "F0007", name: "柳橙", price: 120, category: "水果", imageUrl: "images/柳橙.jpg", calories: 120, origin: "美國", storage: "冷藏", expiryDate: getFutureDate(10), vendor: "每日良品" },
            { id: "F0008", name: "地瓜", price: 190.7, category: "蔬菜", imageUrl: "images/地瓜.jpg", calories: 180, origin: "台灣", storage: "常溫", expiryDate: getFutureDate(14), vendor: "樂活農莊" },
            { id: "F0009", name: "胡蘿蔔", price: 60, category: "蔬菜", imageUrl: "images/胡蘿蔔.jpg", calories: 70, origin: "韓國", storage: "冷藏", expiryDate: getFutureDate(8), vendor: "家香廚坊" },
            { id: "F0010", name: "洋蔥", price: 50, category: "蔬菜", imageUrl: "images/洋蔥.jpg", calories: 60, origin: "美國", storage: "常溫", expiryDate: getFutureDate(20), vendor: "每日良品" }
        ];

        let recipeDatabase = [
            { id: 1, name: "綜合蔬果沙拉", calories: 220, img: "images/綜合蔬果沙拉.jpg", ingredients: ["番茄", "菠菜", "洋蔥", "蘋果"], steps: ["菠菜洗淨瀝乾，番茄、蘋果切塊。", "將所有食材放入大碗中。", "淋上橄欖油、檸檬汁、鹽攪拌均勻。"] },
            { id: 2, name: "蜂蜜烤地瓜", calories: 280, img: "images/蜂蜜烤地瓜.jpg", ingredients: ["地瓜"], steps: ["將地瓜洗淨，不需要削皮。", "烤箱 200°C 烤 30-40 分鐘。", "取出切開淋上蜂蜜。"] },
            { id: 3, name: "鳳梨蘋果汁", calories: 240, img: "images/鳳梨蘋果汁.jpg", ingredients: ["鳳梨", "蘋果"], steps: ["鳳梨與蘋果去皮切塊。", "放入果汁機加適量開水。", "攪打均勻即可飲用。"] },
            { id: 4, name: "番茄炒高麗菜", calories: 190, img: "images/番茄炒高麗菜.jpg", ingredients: ["番茄", "高麗菜"], steps: ["高麗菜洗淨切塊，番茄切塊。", "熱鍋爆香蒜末，先炒番茄。", "加入高麗菜快炒，加鹽調味。"] },
            { id: 5, name: "香蕉柳橙冰沙", calories: 225, img: "images/香蕉柳橙冰沙.jpg", ingredients: ["香蕉", "柳橙"], steps: ["香蕉剝皮切塊，柳橙去皮取肉。", "加入冰塊放入果汁機。", "攪打至綿密冰沙狀。"] },
            { id: 6, name: "義式烤蔬菜", calories: 200, img: "images/義式烤蔬菜.jpg", ingredients: ["胡蘿蔔", "洋蔥", "地瓜"], steps: ["蔬菜切滾刀塊。", "淋上橄欖油、鹽、義式香料拌勻。", "平鋪烤盤，200°C 烤 20-25 分鐘。"] }
        ];

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
            if(cart.length===0) { list.innerHTML = '<p style="text-align:center;color:#999;">空空如也</p>'; document.getElementById('cart-total-price').textContent = 'NT$ 0'; return; }
            let html = '', amount = 0;
            cart.forEach((item, i) => {
                const sub = item.price * item.quantity;
                amount += sub;
                html += `<div class="list-item"><div><div style="font-weight:bold;">${item.name}</div><div style="font-size:0.85rem;color:#666;">$${item.price.toFixed(0)}</div></div><div style="display:flex;align-items:center;gap:5px;"><button onclick="decreaseQuantity(${i})" style="width:25px;height:25px;">-</button><span>${item.quantity}</span><button onclick="increaseQuantity(${i})" style="width:25px;height:25px;">+</button><button onclick="removeFromCart(${i})" style="border:none;background:none;">🗑️</button></div></div>`;
            });
            list.innerHTML = html;
            document.getElementById('cart-total-price').textContent = `NT$ ${amount.toFixed(0)}`;
        }

        let myRecipes = [];
        window.toggleRecipe = function(recipeName, btnElement) {
            const index = myRecipes.indexOf(recipeName);
            if (index === -1) { myRecipes.push(recipeName); btnElement.textContent = "✅ 已收藏"; btnElement.classList.add("saved"); showToast("✅ 已收藏"); }
            else { myRecipes.splice(index, 1); btnElement.textContent = "➕ 收藏"; btnElement.classList.remove("saved"); showToast("🗑️ 已移除"); }
            updateRecipeBookUI();
        };
        window.removeRecipeFromBook = function(recipeName) {
            const index = myRecipes.indexOf(recipeName);
            if(index > -1) { myRecipes.splice(index, 1); updateRecipeBookUI(); }
        }
        function updateRecipeBookUI() {
            document.getElementById('recipe-book-badge').textContent = myRecipes.length;
            const list = document.getElementById('recipe-book-list');
            if(myRecipes.length === 0) { list.innerHTML = '<p style="text-align:center;color:#999;">無收藏</p>'; return; }
            let html = '';
            myRecipes.forEach(name => { html += `<div class="list-item"><div>${name}</div><button onclick="removeRecipeFromBook('${name}')" style="border:none;background:none;">🗑️</button></div>`; });
            list.innerHTML = html;
        }

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
            if(!r || r.ingredients.length===0) { showToast("⚠️ 請先加入食材"); return; }
            const main = r.ingredients[0];
            r.name = `特製${main}料理`;
            r.steps = [`準備 ${r.ingredients.join('、')}`, `將${main}切好`, `全部下鍋煮熟`, `調味後上桌`];
            reloadDetail(r.name);
            showToast("✨ 食譜已更新");
        };
        function reloadDetail(refName) { const btn = document.getElementById('detail-add-btn'); if(btn) showDetailPage(btn.getAttribute('data-current-product-id')); }

        let botRules = [
            { keyword: "營業時間", response: "08:00 - 22:00" },
            { keyword: "地址", response: "台北市信義區快樂路 123 號" },
            { keyword: "電話", response: "02-1234-5678" }
        ];
        function renderBotRules() {
            const tbody = document.getElementById('bot-rules-list');
            let html = '';
            botRules.forEach((rule, index) => { html += `<tr><td>${rule.keyword}</td><td>${rule.response}</td><td><button onclick="deleteBotRule(${index})" style="background:#d9534f;color:white;border:none;">刪</button></td></tr>`; });
            tbody.innerHTML = html;
        }
        window.addBotRule = function() {
            const kw = document.getElementById('new-kw').value.trim();
            const resp = document.getElementById('new-reply').value.trim();
            if(kw && resp) { botRules.push({ keyword: kw, response: resp }); document.getElementById('new-kw').value = ''; document.getElementById('new-reply').value = ''; renderBotRules(); showToast("✨ 已新增"); }
        };
        window.deleteBotRule = function(index) { botRules.splice(index, 1); renderBotRules(); };

        window.sendChatMsg = function() {
            const input = document.getElementById('chat-msg-input');
            const msg = input.value.trim();
            if(!msg) return;
            const chatArea = document.getElementById('chat-display');
            chatArea.innerHTML += `<div class="msg msg-user">${msg}</div>`;
            input.value = '';
            chatArea.scrollTop = chatArea.scrollHeight;
            setTimeout(() => {
                let reply = "請輸入「營業時間」或「地址」。";
                const match = botRules.find(r => msg.includes(r.keyword));
                if(match) reply = match.response;
                chatArea.innerHTML += `<div class="msg msg-bot">${reply}</div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
            }, 600);
        };

        function renderAdminProductList() {
            const tbody = document.getElementById('admin-product-list');
            let html = '';
            productDatabase.forEach((p, index) => { html += `<tr><td><img src="${p.imageUrl}" alt="${p.name}" style="width:40px;height:40px;object-fit:cover;"></td><td>${p.name}</td><td>${p.category}</td><td>${p.price}</td><td><button onclick="deleteProduct(${index})" style="background:#d9534f;color:white;border:none;">刪</button></td></tr>`; });
            tbody.innerHTML = html;
        }
        window.deleteProduct = function(index) { if(confirm("刪除？")) { productDatabase.splice(index, 1); renderAdminProductList(); showToast("🗑️ 已刪除"); } };
        window.addNewProduct = function() {
            const name = document.getElementById('new-p-name').value;
            const price = parseFloat(document.getElementById('new-p-price').value);
            const category = document.getElementById('new-p-category').value;
            if(!name || !price) { alert("資料不全"); return; }
            const newId = "F" + (productDatabase.length + 1).toString().padStart(4, '0');
            productDatabase.push({ id: newId, name: name, price: price, category: category, imageUrl: "https://via.placeholder.com/150?text=" + name, calories: 100, origin: "台灣", storage: "常溫", expiryDate: getFutureDate(7), vendor: "自有" });
            document.getElementById('new-p-name').value = ''; document.getElementById('new-p-price').value = ''; renderAdminProductList(); showToast("✨ 已新增");
        };
        window.switchAdminTab = function(tab) {
            document.querySelectorAll('.admin-tab-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById('admin-products-section').style.display = tab==='products'?'block':'none';
            document.getElementById('admin-bot-section').style.display = tab==='bot'?'block':'none';
            document.getElementById('admin-orders-section').style.display = tab==='orders'?'block':'none';
            if(tab === 'bot') renderBotRules();
        };

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
            else if (daysLeft <= 3) { statusSpan.textContent = `🔥 即將到期 (${daysLeft} 天)`; statusSpan.style.color = "#f0ad4e"; } 
            else { statusSpan.textContent = `✅ 有效 (${daysLeft} 天)`; statusSpan.style.color = "#5cb85c"; }
            document.getElementById('detail-add-btn').setAttribute('data-current-product-id', id);
            document.querySelector('.back-to-list-btn').onclick = showListPage;
            document.getElementById('detail-add-btn').onclick = () => addToCart(p.id);
            
            const recipesContainer = document.getElementById('related-recipes-container');
            let recipesHtml = '';
            const matchedRecipes = recipeDatabase.filter(r => r.ingredients.some(i => i.includes(p.name)) || r.name.includes(p.name));
            if (matchedRecipes.length > 0) {
                matchedRecipes.forEach((r) => {
                    const isSaved = myRecipes.includes(r.name);
                    const btnText = isSaved ? "✅ 已收藏" : "➕ 收藏";
                    const btnClass = isSaved ? "save-recipe-btn saved" : "save-recipe-btn";
                    const uniqueInputId = `new-ing-${r.id}`;
                    recipesHtml += `<div class="recipe-card"><img src="${r.img}" alt="${r.name}" class="recipe-card-img"><div class="recipe-content"><h3>${r.name}</h3><p>🔥 ${r.calories} kcal</p><h4>食材：</h4><ul style="padding-left:20px;">${r.ingredients.map(i=>`<li>${i}</li>`).join('')}</ul><div style="display:flex;gap:5px;margin:10px 0;"><input type="text" id="${uniqueInputId}" placeholder="食材..." style="flex:1;padding:5px;border:1px solid #ccc;border-radius:15px;"><button onclick="addIngredient(${r.id}, '${uniqueInputId}')" style="width:30px;background:#5cb85c;color:white;border:none;border-radius:50%;">+</button></div><button class="magic-generate-btn" onclick="generateStepsFromIngredients(${r.id})">⚡ 生成食譜</button><h4>步驟：</h4><ol style="padding-left:20px;">${r.steps.map(step => `<li>${step}</li>`).join('')}</ol><button class="${btnClass}" onclick="toggleRecipe('${r.name}', this)">${btnText}</button></div></div>`;
                });
            } else {
                recipesHtml = `<div style="text-align:center;padding:20px;background:#fff8e1;border:1px solid #ffe082;border-radius:10px;"><h3>無食譜</h3><p>AI 幫你想？</p><button style="background:#17a2b8;color:white;border:none;padding:10px 20px;border-radius:20px;" onclick="window.location.reload()">✨ 生成食譜</button></div>`;
            }
            recipesContainer.innerHTML = recipesHtml;
            
            listPage.style.display = 'none'; detailPage.style.display = 'block'; window.scrollTo(0, 0);
        }

        document.addEventListener('DOMContentLoaded', function() {
            const container = document.getElementById('product-list-container');
            let html = '';
            productDatabase.forEach(p => {
                const daysLeft = calculateDaysLeft(p.expiryDate);
                let tagHtml = daysLeft < 0 ? `<span class="tag expired-tag">已過期</span>` : `<span class="tag expiry-tag">剩${daysLeft}天</span>`;
                html += `<div class="product-card"><img src="${p.imageUrl}" alt="${p.name}" class="product-card-img" onclick="showDetailPage('${p.id}')"><div class="card-content"><h3>${p.name}</h3><p>${tagHtml}</p><p class="price">NT$ ${p.price.toFixed(0)}</p><div class="card-actions"><button class="view-detail-btn" data-id="${p.id}">詳情</button><button class="view-recipe-btn" data-id="${p.id}">食譜</button><button class="add-to-cart-btn" data-id="${p.id}">+ 加入</button></div></div></div>`;
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

final_html = html_template.replace("images/", BASE_URL + "images/")

# 注意：height 設定為 1200，讓手機滑動空間足夠
components.html(final_html, height=1200, scrolling=True)
