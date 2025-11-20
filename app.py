import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 👇 【已修正】您的 GitHub 資訊
# ==========================================
GITHUB_USER = "ShadowREddd"   
REPO_NAME = "-"     
BRANCH_NAME = "main"            

# 自動生成圖片路徑 (指向根目錄)
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH_NAME}/"
# ==========================================

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
    <title>食際行動家</title>
    
    <style>
        /* --- 基礎設定 --- */
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        html { scroll-behavior: smooth; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f0f2f5;
            padding-bottom: 80px; /* 留給底部導覽列 */
            margin: 0;
            overflow-x: hidden;
            font-size: 16px;
        }
        button { cursor: pointer; transition: all 0.2s; border: none; outline: none; }
        button:active { transform: scale(0.95); }
        input, select, textarea { font-size: 1rem; border: 1px solid #ddd; border-radius: 8px; padding: 10px; width: 100%; margin-bottom: 10px; }
        input:focus, textarea:focus { border-color: #d9534f; outline: none; }

        /* --- 底部導覽列 --- */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
            background: white; display: flex; justify-content: space-around; align-items: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05); z-index: 5000;
        }
        .nav-item {
            flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
            color: #999; font-size: 0.8rem; height: 100%; background: none;
        }
        .nav-item.active { color: #d9534f; font-weight: bold; }
        .nav-icon { font-size: 1.5rem; margin-bottom: 2px; }

        /* --- 頂部標題列 --- */
        .top-header {
            position: sticky; top: 0; z-index: 1000; background: white;
            padding: 15px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            display: flex; justify-content: center; align-items: center;
        }
        .top-header h2 { margin: 0; font-size: 1.2rem; color: #333; }
        .header-btn-right { position: absolute; right: 15px; background: #f1f1f1; color: #555; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; }

        /* --- 頁面容器 --- */
        .page { display: none; padding: 15px; max-width: 1000px; margin: 0 auto; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* --- 商品列表 (Grid) --- */
        .grid-container {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px;
        }
        .card {
            background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            overflow: hidden; display: flex; flex-direction: column;
        }
        .card-img { width: 100%; height: 140px; object-fit: cover; }
        .card-body { padding: 10px; flex: 1; display: flex; flex-direction: column; }
        .card-title { font-weight: bold; margin-bottom: 5px; font-size: 1rem; color: #333; }
        .card-info { font-size: 0.85rem; color: #666; margin-bottom: 5px; }
        .price-tag { font-weight: bold; color: #d9534f; font-size: 1.1rem; margin-top: auto; }
        
        .btn-row { display: flex; gap: 5px; margin-top: 10px; }
        .btn-primary { background: #d9534f; color: white; flex: 1; padding: 8px; border-radius: 6px; font-size: 0.9rem; }
        .btn-secondary { background: #f0f0f0; color: #333; flex: 1; padding: 8px; border-radius: 6px; font-size: 0.9rem; }
        .btn-outline { background: white; border: 1px solid #ddd; color: #555; flex: 1; padding: 8px; border-radius: 6px; }

        /* --- 食譜牆樣式 --- */
        .recipe-header-actions { display: flex; justify-content: space-between; margin-bottom: 15px; }
        .create-recipe-btn { background: linear-gradient(45deg, #ff9966, #ff5e62); color: white; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 10px rgba(255, 94, 98, 0.3); width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; }
        
        /* --- 自訂食譜表單 --- */
        #custom-recipe-form { background: white; padding: 20px; border-radius: 15px; }
        .form-label { font-weight: bold; margin-bottom: 5px; display: block; color: #333; }
        .ing-row { display: flex; gap: 5px; margin-bottom: 5px; }
        .btn-add-item { background: #5cb85c; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
        .btn-remove-item { background: #d9534f; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; }
        .list-preview { background: #f9f9f9; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
        .list-preview-item { display: flex; justify-content: space-between; border-bottom: 1px dashed #ddd; padding: 5px 0; font-size: 0.9rem; }

        /* --- 詳情頁 --- */
        .detail-hero { position: relative; }
        .detail-hero img { width: 100%; height: 300px; object-fit: cover; border-radius: 0 0 20px 20px; }
        .detail-container { padding: 20px; background: white; margin-top: -30px; position: relative; border-radius: 20px 20px 0 0; z-index: 10; min-height: 300px; }
        .detail-title { font-size: 1.8rem; margin: 0 0 10px 0; color: #333; }
        .tag { display: inline-block; padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; color: white; background: #999; margin-right: 5px; }
        .tag-exp-ok { background: #5cb85c; }
        .tag-exp-warn { background: #f0ad4e; }
        .tag-exp-bad { background: #d9534f; }

        .recipe-link-btn { 
            margin-top: 20px; background: #fff8e1; color: #8d6e63; border: 1px solid #ffe082; 
            padding: 15px; width: 100%; border-radius: 12px; text-align: left; 
            display: flex; justify-content: space-between; align-items: center; font-weight: bold;
        }

        /* --- Modal (購物車/食譜本) --- */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 6000; justify-content: center; align-items: center; }
        .modal-content { background: white; width: 90%; max-width: 400px; max-height: 80vh; border-radius: 15px; overflow: hidden; display: flex; flex-direction: column; }
        .modal-header { padding: 15px; background: #333; color: white; display: flex; justify-content: space-between; }
        .modal-body { padding: 15px; overflow-y: auto; flex: 1; }
        .modal-footer { padding: 15px; border-top: 1px solid #eee; }

        /* --- Toast --- */
        #toast { position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.8); color: white; padding: 10px 20px; border-radius: 20px; opacity: 0; transition: opacity 0.3s; z-index: 7000; pointer-events: none; white-space: nowrap; }
        #toast.show { opacity: 1; }

    </style>
</head>
<body>

    <div class="top-header">
        <h2 id="header-title">食際行動家</h2>
        <button class="header-btn-right" onclick="showBackend()">後台</button>
    </div>

    <div id="market-page" class="page" style="display: block;">
        <div id="product-grid" class="grid-container"></div>
    </div>

    <div id="recipe-page" class="page">
        <div class="recipe-header-actions">
            <input type="text" id="recipe-search" placeholder="🔍 搜尋食材或料理..." onkeyup="filterRecipes()" style="margin-bottom:0; width:auto; flex:1; margin-right:10px;">
            <button class="create-recipe-btn" onclick="showCreateRecipePage()" style="width:auto; padding: 0 15px; font-size:0.9rem;">＋ 自訂</button>
        </div>
        <div id="recipe-grid" class="grid-container"></div>
    </div>

    <div id="detail-page" class="page" style="padding:0; max-width: none;">
        <div class="detail-hero">
            <img id="dt-img" src="">
            <button onclick="switchTab('market')" style="position: absolute; top: 20px; left: 20px; background: rgba(255,255,255,0.8); border-radius: 50%; width: 40px; height: 40px; font-size: 1.2rem;">←</button>
        </div>
        <div class="detail-container">
            <h1 id="dt-name" class="detail-title"></h1>
            <div style="margin-bottom: 15px;">
                <span id="dt-tag" class="tag"></span>
                <span id="dt-price" style="font-size: 1.5rem; font-weight: bold; color: #d9534f; float: right;"></span>
            </div>
            <p style="color:#666; line-height: 1.6;">
                產地：<span id="dt-origin"></span><br>
                保存：<span id="dt-storage"></span><br>
                到期日：<span id="dt-expiry"></span>
            </p>
            
            <div style="display: flex; gap: 10px; margin: 20px 0;">
                <button class="btn-primary" id="dt-add-btn" style="padding: 15px; font-size: 1.1rem;">＋ 加入購物車</button>
            </div>

            <button class="recipe-link-btn" id="dt-recipe-link">
                <span>📖 看看「<span id="dt-ing-name"></span>」可以做什麼料理？</span>
                <span>➔</span>
            </button>
        </div>
    </div>

    <div id="create-recipe-page" class="page">
        <div style="display:flex; align-items:center; margin-bottom:15px;">
            <button onclick="switchTab('recipe')" style="background:none; font-size:1.5rem; margin-right:10px;">←</button>
            <h2 style="margin:0;">新增私房食譜</h2>
        </div>
        <div id="custom-recipe-form">
            <label class="form-label">食譜名稱</label>
            <input type="text" id="new-r-name" placeholder="例如：阿嬤的紅燒肉">
            
            <label class="form-label">預估卡路里 (大卡)</label>
            <input type="number" id="new-r-cal" placeholder="例如：500">
            
            <label class="form-label">所需食材 (請逐一新增)</label>
            <div class="ing-row">
                <input type="text" id="temp-ing-input" placeholder="輸入食材...">
                <button class="btn-add-item" onclick="addTempIngredient()">＋</button>
            </div>
            <div id="new-r-ing-list" class="list-preview">尚未加入食材</div>

            <label class="form-label">料理步驟 (請逐一新增)</label>
            <div class="ing-row">
                <textarea id="temp-step-input" rows="2" placeholder="輸入步驟說明..."></textarea>
                <button class="btn-add-item" onclick="addTempStep()">＋</button>
            </div>
            <div id="new-r-step-list" class="list-preview">尚未加入步驟</div>

            <button class="create-recipe-btn" onclick="saveCustomRecipe()" style="width:100%; margin-top:10px;">✨ 完成並發布</button>
        </div>
    </div>

    <div id="backend-page" class="page">
        <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
            <h2>後台管理</h2>
            <button class="btn-outline" onclick="switchTab('market')">返回前台</button>
        </div>
        <div style="background:white; padding:15px; border-radius:10px;">
            <h3>商品列表</h3>
            <table style="width:100%; font-size:0.9rem;">
                <thead><tr><th align="left">名稱</th><th align="right">操作</th></tr></thead>
                <tbody id="admin-list"></tbody>
            </table>
        </div>
    </div>

    <div class="bottom-nav">
        <button class="nav-item active" onclick="switchTab('market')" id="tab-market">
            <div class="nav-icon">🥦</div>
            <div>市集</div>
        </button>
        <button class="nav-item" onclick="switchTab('recipe')" id="tab-recipe">
            <div class="nav-icon">👨‍🍳</div>
            <div>食譜牆</div>
        </button>
        <button class="nav-item" onclick="openModal('cart-modal')">
            <div class="nav-icon">🛒<span id="cart-count" style="font-size:0.8rem; vertical-align:top; color:#d9534f;">0</span></div>
            <div>購物車</div>
        </button>
        <button class="nav-item" onclick="openModal('book-modal')">
            <div class="nav-icon">📖</div>
            <div>收藏本</div>
        </button>
    </div>

    <div id="cart-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header"><span>購物車</span><span onclick="closeModal('cart-modal')">✕</span></div>
            <div class="modal-body" id="cart-body"><p style="text-align:center; color:#999;">購物車是空的</p></div>
            <div class="modal-footer">
                <div style="display:flex; justify-content:space-between; font-weight:bold; margin-bottom:10px;">
                    <span>總計</span><span id="cart-total">$0</span>
                </div>
                <button class="btn-primary" style="width:100%;" onclick="alert('結帳成功！'); cart=[]; updateCart(); closeModal('cart-modal');">前往結帳</button>
            </div>
        </div>
    </div>

    <div id="book-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header"><span>我的收藏食譜</span><span onclick="closeModal('book-modal')">✕</span></div>
            <div class="modal-body" id="book-body"><p style="text-align:center; color:#999;">尚未收藏</p></div>
        </div>
    </div>

    <div id="toast">提示訊息</div>

    <script>
        // --- 資料區 ---
        function getFutureDate(d) { const date = new Date(); date.setDate(date.getDate()+d); return date.toISOString().split('T')[0]; }
        
        // 修正重點：副檔名必須與 GitHub 上完全一致 (.jpg vs .JPG)
        let products = [
            { id: "P1", name: "蘋果", price: 139, img: "images/蘋果.jpg", cat: "水果", date: getFutureDate(6), origin: "美國", storage: "冷藏" },
            { id: "P2", name: "香蕉", price: 80, img: "images/香蕉.jpg", cat: "水果", date: getFutureDate(3), origin: "台灣", storage: "常溫" },
            { id: "P3", name: "高麗菜", price: 160, img: "images/高麗菜.JPG", cat: "蔬菜", date: getFutureDate(7), origin: "台灣", storage: "冷藏" }, // JPG
            { id: "P4", name: "番茄", price: 70, img: "images/番茄.JPG", cat: "蔬菜", date: getFutureDate(5), origin: "台灣", storage: "冷藏" }, // JPG
            { id: "P5", name: "洋蔥", price: 50, img: "images/洋蔥.jpg", cat: "蔬菜", date: getFutureDate(20), origin: "美國", storage: "常溫" },
            { id: "P6", name: "地瓜", price: 190, img: "images/地瓜.jpg", cat: "蔬菜", date: getFutureDate(14), origin: "台灣", storage: "常溫" },
            { id: "P7", name: "柳橙", price: 120, img: "images/柳橙.JPG", cat: "水果", date: getFutureDate(10), origin: "美國", storage: "冷藏" }, // JPG
            { id: "P8", name: "菠菜", price: 90, img: "images/菠菜.JPG", cat: "蔬菜", date: getFutureDate(2), origin: "台灣", storage: "冷藏" }, // JPG
            { id: "P9", name: "胡蘿蔔", price: 60, img: "images/胡蘿蔔.jpg", cat: "蔬菜", date: getFutureDate(8), origin: "韓國", storage: "冷藏" },
            { id: "P10", name: "鳳梨", price: 155, img: "images/鳳梨.jpg", cat: "水果", date: getFutureDate(5), origin: "美國", storage: "冷凍" }
        ];

        let recipes = [
            { id: "R1", name: "綜合蔬果沙拉", cal: 220, img: "images/綜合蔬果沙拉.jpg", ingredients: ["蘋果", "番茄", "洋蔥"], steps: ["所有食材洗淨切塊", "加入橄欖油與鹽拌勻"] },
            { id: "R2", name: "番茄炒高麗菜", cal: 180, img: "images/番茄炒高麗菜.jpg", ingredients: ["番茄", "高麗菜"], steps: ["熱鍋爆香", "加入番茄炒軟", "加入高麗菜炒熟"] },
            { id: "R3", name: "蜂蜜烤地瓜", cal: 250, img: "images/蜂蜜烤地瓜.jpg", ingredients: ["地瓜"], steps: ["洗淨", "200度烤40分鐘"] },
            { id: "R4", name: "鳳梨蘋果汁", cal: 150, img: "images/鳳梨蘋果汁.jpg", ingredients: ["鳳梨", "蘋果"], steps: ["切塊", "加水打成汁"] },
            { id: "R5", name: "香蕉柳橙冰沙", cal: 180, img: "images/香蕉柳橙冰沙.jpg", ingredients: ["香蕉", "柳橙"], steps: ["加冰塊", "打成冰沙"] },
            { id: "R6", name: "義式烤蔬菜", cal: 200, img: "images/義式烤蔬菜.jpg", ingredients: ["胡蘿蔔", "洋蔥"], steps: ["切塊", "撒上香料烤熟"] }
        ];

        let cart = [];
        let savedRecipes = [];
        
        // 自訂食譜暫存
        let tempIngredients = [];
        let tempSteps = [];

        // --- 核心功能 ---
        function showToast(msg) {
            const t = document.getElementById('toast');
            t.textContent = msg; t.classList.add('show');
            setTimeout(() => t.classList.remove('show'), 2000);
        }

        function switchTab(tabName) {
            // 隱藏所有頁面
            document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
            document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
            
            if(tabName === 'market') {
                document.getElementById('market-page').style.display = 'block';
                document.getElementById('tab-market').classList.add('active');
                document.getElementById('header-title').textContent = "市集";
            } else if(tabName === 'recipe') {
                document.getElementById('recipe-page').style.display = 'block';
                document.getElementById('tab-recipe').classList.add('active');
                document.getElementById('header-title').textContent = "食譜牆";
                renderRecipes(); // 重新渲染
                document.getElementById('recipe-search').value = ''; // 清空搜尋
            }
            window.scrollTo(0,0);
        }

        function showDetail(pid) {
            const p = products.find(x => x.id === pid);
            if(!p) return;
            
            document.getElementById('market-page').style.display = 'none';
            document.getElementById('detail-page').style.display = 'block';
            
            document.getElementById('dt-img').src = p.img;
            document.getElementById('dt-name').textContent = p.name;
            document.getElementById('dt-price').textContent = "NT$ " + p.price;
            document.getElementById('dt-origin').textContent = p.origin;
            document.getElementById('dt-storage').textContent = p.storage;
            document.getElementById('dt-expiry').textContent = p.date;
            document.getElementById('dt-ing-name').textContent = p.name;
            
            // 設定食譜連結按鈕：點擊後跳轉到食譜牆並搜尋該食材
            const btn = document.getElementById('dt-recipe-link');
            btn.onclick = function() {
                switchTab('recipe');
                const searchInput = document.getElementById('recipe-search');
                searchInput.value = p.name;
                filterRecipes(); // 執行搜尋
                showToast(`已為您搜尋「${p.name}」相關食譜`);
            };

            // 加入購物車按鈕
            document.getElementById('dt-add-btn').onclick = function() {
                addToCart(p.id);
            };
            
            window.scrollTo(0,0);
        }

        function showBackend() {
            document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
            document.getElementById('backend-page').style.display = 'block';
            renderAdmin();
        }

        // --- 商品邏輯 ---
        function renderProducts() {
            const grid = document.getElementById('product-grid');
            let html = '';
            products.forEach(p => {
                html += `
                <div class="card" onclick="showDetail('${p.id}')">
                    <img src="${p.img}" class="card-img">
                    <div class="card-body">
                        <div class="card-title">${p.name}</div>
                        <div class="card-info">${p.cat}</div>
                        <div class="price-tag">NT$ ${p.price}</div>
                    </div>
                </div>`;
            });
            grid.innerHTML = html;
        }

        // --- 食譜邏輯 (重點修改) ---
        function renderRecipes(list = recipes) {
            const grid = document.getElementById('recipe-grid');
            if(list.length === 0) {
                grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; color:#999; padding:20px;">找不到相關食譜，試試自訂一個？</div>';
                return;
            }
            let html = '';
            list.forEach(r => {
                const isSaved = savedRecipes.includes(r.id);
                html += `
                <div class="card">
                    <img src="${r.img}" class="card-img" onerror="this.src='https://via.placeholder.com/300?text=Recipe'">
                    <div class="card-body">
                        <div class="card-title">${r.name}</div>
                        <div class="card-info">🔥 ${r.cal} kcal</div>
                        <div class="card-info">食材: ${r.ingredients.join('、')}</div>
                        <div class="btn-row">
                            <button class="btn-outline" onclick="alert('步驟：\\n${r.steps.join('\\n')}')">查看做法</button>
                            <button class="${isSaved ? 'btn-primary' : 'btn-secondary'}" onclick="toggleSaveRecipe('${r.id}')">
                                ${isSaved ? '已收藏' : '收藏'}
                            </button>
                        </div>
                    </div>
                </div>`;
            });
            grid.innerHTML = html;
        }

        function filterRecipes() {
            const kw = document.getElementById('recipe-search').value.trim();
            if(!kw) { renderRecipes(recipes); return; }
            const filtered = recipes.filter(r => 
                r.name.includes(kw) || r.ingredients.some(i => i.includes(kw))
            );
            renderRecipes(filtered);
        }

        function toggleSaveRecipe(rid) {
            const idx = savedRecipes.indexOf(rid);
            if(idx === -1) { savedRecipes.push(rid); showToast("已收藏到食譜本"); }
            else { savedRecipes.splice(idx, 1); showToast("已取消收藏"); }
            renderRecipes(); // 更新按鈕狀態
            updateBookModal();
        }

        // --- 自訂食譜邏輯 ---
        function showCreateRecipePage() {
            document.getElementById('recipe-page').style.display = 'none';
            document.getElementById('create-recipe-page').style.display = 'block';
            // 重置表單
            document.getElementById('new-r-name').value = '';
            document.getElementById('new-r-cal').value = '';
            tempIngredients = [];
            tempSteps = [];
            updateCustomPreview();
        }

        function addTempIngredient() {
            const input = document.getElementById('temp-ing-input');
            const val = input.value.trim();
            if(val) { tempIngredients.push(val); input.value=''; updateCustomPreview(); }
        }
        function addTempStep() {
            const input = document.getElementById('temp-step-input');
            const val = input.value.trim();
            if(val) { tempSteps.push(val); input.value=''; updateCustomPreview(); }
        }
        function updateCustomPreview() {
            const ingList = document.getElementById('new-r-ing-list');
            ingList.innerHTML = tempIngredients.length ? tempIngredients.map((item, i) => 
                `<div class="list-preview-item"><span>${item}</span><span style="color:red;cursor:pointer;" onclick="tempIngredients.splice(${i},1);updateCustomPreview()">✕</span></div>`
            ).join('') : '尚未加入食材';

            const stepList = document.getElementById('new-r-step-list');
            stepList.innerHTML = tempSteps.length ? tempSteps.map((item, i) => 
                `<div class="list-preview-item"><span>${i+1}. ${item}</span><span style="color:red;cursor:pointer;" onclick="tempSteps.splice(${i},1);updateCustomPreview()">✕</span></div>`
            ).join('') : '尚未加入步驟';
        }

        function saveCustomRecipe() {
            const name = document.getElementById('new-r-name').value.trim();
            const cal = document.getElementById('new-r-cal').value;
            
            if(!name || tempIngredients.length===0 || tempSteps.length===0) {
                alert("請完整填寫名稱、食材與步驟！"); return;
            }

            const newRecipe = {
                id: "C" + Date.now(),
                name: name,
                cal: cal || 0,
                img: "https://via.placeholder.com/300?text=" + name, // 自訂食譜暫用無圖
                ingredients: [...tempIngredients],
                steps: [...tempSteps]
            };
            
            recipes.unshift(newRecipe); // 加到最前面
            showToast("✨ 私房食譜發布成功！");
            switchTab('recipe'); // 回到食譜牆
        }

        // --- 購物車 & Modal ---
        function addToCart(pid) {
            const p = products.find(x => x.id === pid);
            const item = cart.find(x => x.id === pid);
            if(item) item.qty++; else cart.push({id:pid, name:p.name, price:p.price, qty:1});
            updateCart(); showToast("已加入購物車");
        }
        function updateCart() {
            const total = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
            const count = cart.reduce((acc, item) => acc + item.qty, 0);
            document.getElementById('cart-count').textContent = count;
            document.getElementById('cart-total').textContent = "$" + total;
            
            const body = document.getElementById('cart-body');
            if(cart.length === 0) body.innerHTML = '<p style="text-align:center; color:#999;">購物車是空的</p>';
            else {
                body.innerHTML = cart.map(item => `
                    <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #eee;">
                        <div>${item.name} x ${item.qty}</div>
                        <div>$${item.price * item.qty}</div>
                    </div>
                `).join('');
            }
        }
        
        function updateBookModal() {
            const body = document.getElementById('book-body');
            if(savedRecipes.length === 0) body.innerHTML = '<p style="text-align:center; color:#999;">尚未收藏</p>';
            else {
                body.innerHTML = savedRecipes.map(rid => {
                    const r = recipes.find(x => x.id === rid);
                    return r ? `<div style="padding:10px; border-bottom:1px solid #eee;">${r.name}</div>` : '';
                }).join('');
            }
        }

        function openModal(id) { document.getElementById(id).style.display = 'flex'; if(id==='book-modal') updateBookModal(); }
        function closeModal(id) { document.getElementById(id).style.display = 'none'; }

        // --- 後台 ---
        function renderAdmin() {
            document.getElementById('admin-list').innerHTML = products.map(p => `
                <tr>
                    <td>${p.name}</td>
                    <td align="right"><button style="color:red; background:none;" onclick="alert('刪除功能演示')">刪除</button></td>
                </tr>
            `).join('');
        }

        // --- 初始化 ---
        window.onload = function() {
            renderProducts();
        };

    </script>
</body>
</html>
"""

# 替換圖片連結 (直接替換為 BASE_URL，因為圖片在根目錄)
final_html = html_template.replace("images/", BASE_URL)

# 渲染 (高度設為 1000 確保手機滑動順暢)
components.html(final_html, height=1000, scrolling=True)
