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
        /* --- 全域設定 --- */
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f6f8; margin: 0; 
            padding-bottom: 80px; /* 手機版預留底部空間 */
            overflow-x: hidden;
        }

        :root { --primary: #d9534f; --text: #333; --bg: #fff; }

        /* RWD 控制 */
        .desktop-only { display: none !important; }
        .mobile-only { display: flex !important; }

        @media (min-width: 768px) {
            body { padding-bottom: 0; padding-top: 70px; }
            .desktop-only { display: flex !important; }
            .mobile-only { display: none !important; }
        }

        /* --- 登入封面 (Splash Screen - 全螢幕滿版) --- */
        #splash { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background: white; z-index: 99999; 
            display: flex; flex-direction: column; justify-content: center; align-items: center; 
            transition: opacity 0.6s ease-out;
        }
        .splash-logo { width: 70%; max-width: 500px; animation: breathe 3s infinite; object-fit: contain; }
        @keyframes breathe { 0%, 100% { transform: scale(0.95); opacity: 0.9; } 50% { transform: scale(1.05); opacity: 1; } }
        .click-hint { margin-top: 20px; color: #999; font-size: 1.2rem; animation: blink 2s infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* --- 導覽列 --- */
        /* 手機底部 */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 65px;
            background: white; justify-content: space-around; align-items: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05); z-index: 5000; border-top: 1px solid #eee;
        }
        .nav-item { flex: 1; text-align: center; color: #999; font-size: 0.75rem; background:none; border:none; cursor: pointer; }
        .nav-item.active { color: var(--primary); font-weight: bold; }
        .nav-icon { font-size: 1.4rem; display: block; margin-bottom: 2px; }

        /* 電腦頂部 */
        .top-nav {
            position: fixed; top: 0; left: 0; width: 100%; height: 70px;
            background: white; justify-content: space-between; align-items: center;
            padding: 0 50px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); z-index: 5000;
        }
        .logo { font-size: 1.5rem; font-weight: bold; color: #333; cursor: pointer; display: flex; align-items: center; gap: 10px; }
        .desktop-menu button {
            background: none; border: none; font-size: 1rem; margin-left: 20px; cursor: pointer; color: #666; transition: 0.2s;
        }
        .desktop-menu button:hover, .desktop-menu button.active { color: var(--primary); font-weight: bold; }
        .cart-btn-desktop { background: var(--primary) !important; color: white !important; padding: 8px 20px; border-radius: 20px; }

        /* --- 主容器 --- */
        .container { max-width: 1200px; margin: 0 auto; padding: 15px; }

        /* --- 橫幅 (Banner) --- */
        .banner-container {
            width: 100%; 
            height: 180px; /* 手機高度 */
            background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .banner-img { height: 100%; width: auto; object-fit: contain; }
        /* 電腦版橫幅更高 */
        @media (min-width: 768px) {
            .banner-container { height: 300px; }
        }

        /* --- 分類滑動列 (Categories) --- */
        .category-bar {
            display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 15px;
            scrollbar-width: none; /* Firefox 隱藏捲軸 */
        }
        .category-bar::-webkit-scrollbar { display: none; /* Chrome 隱藏捲軸 */ }
        
        .cat-btn {
            white-space: nowrap;
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid #ddd;
            background: white;
            color: #666;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .cat-btn.active {
            background: var(--primary); color: white; border-color: var(--primary); box-shadow: 0 4px 10px rgba(217, 83, 79, 0.3);
        }

        /* --- 商品網格 --- */
        .grid { 
            display: grid; gap: 15px;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); 
        }
        .card { 
            background: white; border-radius: 12px; overflow: hidden; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.05); cursor: pointer; transition: transform 0.2s; 
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .card-img { width: 100%; height: 160px; object-fit: cover; }
        .card-body { padding: 12px; }
        .card-title { font-weight: bold; margin-bottom: 5px; color: #333; }
        .price { color: var(--primary); font-weight: bold; font-size: 1.1rem; }

        /* --- 詳情頁 --- */
        .page { display: none; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .detail-wrapper { 
            display: flex; flex-direction: column; background: white; border-radius: 0; 
        }
        @media (min-width: 768px) {
            .detail-wrapper { 
                flex-direction: row; border-radius: 20px; padding: 40px; gap: 40px; margin-top: 20px;
            }
            .detail-hero { flex: 1; }
            .detail-hero img { border-radius: 15px; height: 400px !important; }
            .detail-info { flex: 1; padding: 0 !important; margin-top: 0 !important; background: none !important; }
            .back-btn { top: 90px !important; left: 40px !important; }
        }
        .detail-hero { position: relative; }
        .detail-hero img { width: 100%; height: 300px; object-fit: cover; }
        .detail-info { padding: 20px; background: white; border-radius: 20px 20px 0 0; margin-top: -20px; position: relative; }
        .back-btn { position: absolute; top: 20px; left: 20px; width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.9); border:none; z-index: 10; font-size:1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor:pointer;}

        /* --- Modal --- */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 6000; }
        .modal-content { 
            position: absolute; bottom: 0; left: 0; width: 100%; max-height: 85vh; 
            background: white; border-radius: 20px 20px 0 0; padding: 20px; 
            display: flex; flex-direction: column; animation: slideUp 0.3s;
        }
        @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
        @media (min-width: 768px) {
            .modal { align-items: center; justify-content: center; }
            .modal-content { 
                position: relative; width: 500px; border-radius: 15px; bottom: auto; left: auto; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2); animation: fadeIn 0.3s;
            }
        }

        /* --- 通用元件 --- */
        .btn { width: 100%; padding: 12px; border-radius: 10px; border: none; font-weight: bold; font-size: 1rem; margin-top: 10px; cursor: pointer; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-outline { background: white; border: 1px solid #ddd; color: #555; }
        .tag { background: #eee; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; color: #666; }

    </style>
</head>
<body>

    <div id="splash" onclick="this.style.opacity=0; setTimeout(()=>this.style.display='none',600)">
        <img src="images/食際行動家.png" class="splash-logo" onerror="this.parentElement.innerHTML+='<h1 style=\\'color:#d9534f; font-size:3rem;\\'>食際行動家</h1>';this.style.display='none'">
        <div class="click-hint">👆 點擊進入市集</div>
    </div>

    <div class="top-nav desktop-only">
        <div class="logo" onclick="switchPage('market')">
            <img src="images/食際行動家.png" style="height:40px;"> 食際行動家
        </div>
        <div class="desktop-menu">
            <button id="dt-nav-market" class="active" onclick="switchPage('market')">生鮮市集</button>
            <button id="dt-nav-recipe" onclick="switchPage('recipe')">食譜牆</button>
            <button class="cart-btn-desktop" onclick="openModal('cart')">購物車 (<span class="cart-count-num">0</span>)</button>
        </div>
    </div>

    <div class="container">
        
        <div id="page-market" class="page" style="display:block;">
            
            <div class="banner-container">
                <img src="images/食際行動家.png" class="banner-img">
            </div>

            <div class="category-bar" id="cat-bar">
                <button class="cat-btn active" onclick="filterCat('all', this)">全部</button>
                <button class="cat-btn" onclick="filterCat('水果', this)">🍎 水果</button>
                <button class="cat-btn" onclick="filterCat('蔬菜', this)">🥦 蔬菜</button>
                <button class="cat-btn" onclick="filterCat('肉品', this)">🥩 肉品</button>
                <button class="cat-btn" onclick="filterCat('海鮮', this)">🐟 海鮮</button>
                <button class="cat-btn" onclick="filterCat('飲品', this)">🥤 飲品</button>
            </div>

            <div id="grid-products" class="grid"></div>
        </div>

        <div id="page-recipe" class="page">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h2>食譜牆</h2>
                <button class="btn-outline" style="width:auto; padding:8px 20px;" onclick="showCreateRecipe()">＋ 自訂食譜</button>
            </div>
            <div id="grid-recipes" class="grid"></div>
        </div>

        <div id="page-detail" class="page">
            <button class="back-btn" onclick="switchPage('market')">←</button>
            <div class="detail-wrapper">
                <div class="detail-hero">
                    <img id="dt-img" src="">
                </div>
                <div class="detail-info">
                    <h1 id="dt-name" style="margin:0; font-size:1.8rem;"></h1>
                    <div style="margin:10px 0;">
                        <span id="dt-price" style="color:#d9534f; font-size:1.5rem; font-weight:bold;"></span>
                        <span id="dt-tag" class="tag" style="float:right; margin-top:5px;"></span>
                    </div>
                    <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
                    <p style="color:#666; line-height:1.6; font-size:1rem;">
                        📍 產地：<span id="dt-origin"></span><br>
                        ❄️ 保存：<span id="dt-storage"></span><br>
                        📅 到期：<span id="dt-expiry"></span>
                    </p>
                    <div style="display:flex; gap:10px; margin-top:20px;">
                        <button class="btn btn-primary" onclick="addToCart()">＋ 加入購物車</button>
                        <button class="btn btn-outline" onclick="findRecipe()">📖 相關料理</button>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <div class="bottom-nav mobile-only">
        <button class="nav-item active" id="mb-nav-market" onclick="switchPage('market')">
            <span class="nav-icon">🥦</span>市集
        </button>
        <button class="nav-item" id="mb-nav-recipe" onclick="switchPage('recipe')">
            <span class="nav-icon">👨‍🍳</span>食譜
        </button>
        <button class="nav-item" onclick="openModal('cart')">
            <span class="nav-icon">🛒<span class="cart-count-num" style="font-size:0.8rem; color:#d9534f; vertical-align:top;">0</span></span>購物車
        </button>
    </div>

    <div id="modal-cart" class="modal" onclick="if(event.target===this) closeModal('cart')">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h3 style="margin:0;">我的購物車</h3>
                <span onclick="closeModal('cart')" style="cursor:pointer; font-size:1.5rem;">✕</span>
            </div>
            <div id="cart-list" style="flex:1; overflow-y:auto; min-height:150px;"></div>
            <div style="border-top:1px solid #eee; padding-top:15px; margin-top:10px;">
                <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:1.2rem;">
                    <span>總計</span><span id="cart-total">$0</span>
                </div>
                <button class="btn btn-primary" onclick="alert('結帳成功！'); cart=[]; updateCartUI(); closeModal('cart')">前往結帳</button>
            </div>
        </div>
    </div>

    <div id="modal-step" class="modal" onclick="if(event.target===this) closeModal('step')">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h3 style="margin:0;" id="step-title">料理步驟</h3>
                <span onclick="closeModal('step')" style="cursor:pointer; font-size:1.5rem;">✕</span>
            </div>
            <div id="step-body" style="flex:1; overflow-y:auto; line-height:1.8;"></div>
            <button class="btn btn-outline" onclick="closeModal('step')">關閉</button>
        </div>
    </div>

    <script>
        function getFutureDate(d) { const date = new Date(); date.setDate(date.getDate()+d); return date.toISOString().split('T')[0]; }

        // --- 資料庫 (已擴充分類) ---
        const products = [
            { id: "P1", name: "蘋果", price: 139, img: "images/蘋果.jpg", cat: "水果", origin: "美國", storage: "冷藏", date: getFutureDate(6) },
            { id: "P2", name: "香蕉", price: 80, img: "images/香蕉.jpg", cat: "水果", origin: "台灣", storage: "常溫", date: getFutureDate(3) },
            { id: "P3", name: "高麗菜", price: 160, img: "images/高麗菜.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(7) },
            { id: "P4", name: "番茄", price: 70, img: "images/番茄.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(5) },
            { id: "P5", name: "洋蔥", price: 50, img: "images/洋蔥.jpg", cat: "蔬菜", origin: "美國", storage: "常溫", date: getFutureDate(20) },
            { id: "P6", name: "地瓜", price: 190, img: "images/地瓜.jpg", cat: "蔬菜", origin: "台灣", storage: "常溫", date: getFutureDate(14) },
            { id: "P7", name: "柳橙", price: 120, img: "images/柳橙.JPG", cat: "水果", origin: "美國", storage: "冷藏", date: getFutureDate(10) },
            { id: "P8", name: "菠菜", price: 90, img: "images/菠菜.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(2) },
            { id: "P9", name: "胡蘿蔔", price: 60, img: "images/胡蘿蔔.jpg", cat: "蔬菜", origin: "韓國", storage: "冷藏", date: getFutureDate(8) },
            { id: "P10", name: "鳳梨", price: 155, img: "images/鳳梨.jpg", cat: "水果", origin: "美國", storage: "冷凍", date: getFutureDate(5) },
            
            // 新增的肉品與海鮮假資料 (圖片暫用 placeholder)
            { id: "P11", name: "豬梅花肉片", price: 200, img: "https://via.placeholder.com/300?text=Pork", cat: "肉品", origin: "台灣", storage: "冷凍", date: getFutureDate(30) },
            { id: "P12", name: "牛小排", price: 500, img: "https://via.placeholder.com/300?text=Beef", cat: "肉品", origin: "美國", storage: "冷凍", date: getFutureDate(30) },
            { id: "P13", name: "鮭魚切片", price: 350, img: "https://via.placeholder.com/300?text=Salmon", cat: "海鮮", origin: "挪威", storage: "冷凍", date: getFutureDate(15) },
            { id: "P14", name: "鮮乳", price: 90, img: "https://via.placeholder.com/300?text=Milk", cat: "飲品", origin: "台灣", storage: "冷藏", date: getFutureDate(10) }
        ];

        const recipes = [
            { id: "R1", name: "綜合蔬果沙拉", cal: 220, img: "images/綜合蔬果沙拉.jpg", steps: ["所有食材洗淨切塊", "加入橄欖油與鹽拌勻"] },
            { id: "R2", name: "番茄炒高麗菜", cal: 180, img: "images/番茄炒高麗菜.jpg", steps: ["熱鍋爆香", "加入番茄炒軟", "加入高麗菜炒熟"] },
            { id: "R3", name: "蜂蜜烤地瓜", cal: 250, img: "images/蜂蜜烤地瓜.jpg", steps: ["洗淨", "200度烤40分鐘"] },
            { id: "R4", name: "鳳梨蘋果汁", cal: 150, img: "images/鳳梨蘋果汁.jpg", steps: ["切塊", "加水打成汁"] },
            { id: "R5", name: "香蕉柳橙冰沙", cal: 180, img: "images/香蕉柳橙冰沙.jpg", steps: ["加冰塊", "打成冰沙"] },
            { id: "R6", name: "義式烤蔬菜", cal: 200, img: "images/義式烤蔬菜.jpg", steps: ["切塊", "撒上香料烤熟"] }
        ];

        let cart = [];
        let currentPid = null;

        function init() {
            renderProducts(products); // 初始渲染所有商品
            renderRecipes();
        }

        function renderProducts(list) {
            document.getElementById('grid-products').innerHTML = list.map(p => `
                <div class="card" onclick="showDetail('${p.id}')">
                    <img src="${p.img}" class="card-img" onerror="this.src='https://via.placeholder.com/300?text=${p.name}'">
                    <div class="card-body">
                        <div class="card-title">${p.name}</div>
                        <div class="price">$${p.price}</div>
                    </div>
                </div>
            `).join('');
        }

        // 分類篩選功能
        function filterCat(cat, btn) {
            // 切換按鈕樣式
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // 篩選資料
            if (cat === 'all') {
                renderProducts(products);
            } else {
                const filtered = products.filter(p => p.cat === cat);
                renderProducts(filtered);
            }
        }

        function renderRecipes() {
            document.getElementById('grid-recipes').innerHTML = recipes.map(r => `
                <div class="card" onclick="showStep('${r.id}')">
                    <img src="${r.img}" class="card-img" onerror="this.src='https://via.placeholder.com/300'">
                    <div class="card-body">
                        <div class="card-title">${r.name}</div>
                        <div style="color:#666; font-size:0.9rem;">🔥 ${r.cal} kcal</div>
                        <button class="btn btn-outline" style="padding:5px; margin-top:5px; font-size:0.8rem;">查看做法</button>
                    </div>
                </div>
            `).join('');
        }

        function switchPage(page) {
            document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelectorAll('.desktop-menu button').forEach(n => n.classList.remove('active'));
            
            if(document.getElementById('mb-nav-'+page)) document.getElementById('mb-nav-'+page).classList.add('active');
            if(document.getElementById('dt-nav-'+page)) document.getElementById('dt-nav-'+page).classList.add('active');

            document.getElementById('page-'+page).style.display = 'block';
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
            switchPage('detail');
        }

        function addToCart() {
            if(!currentPid) return;
            const p = products.find(x => x.id === currentPid);
            const item = cart.find(x => x.id === currentPid);
            if(item) item.qty++; else cart.push({id:p.id, name:p.name, price:p.price, qty:1});
            updateCartUI();
            alert('✅ 已加入購物車');
        }

        function updateCartUI() {
            const count = cart.reduce((sum, i) => sum + i.qty, 0);
            const total = cart.reduce((sum, i) => sum + i.price*i.qty, 0);
            document.querySelectorAll('.cart-count-num').forEach(el => el.innerText = count);
            document.getElementById('cart-total').innerText = '$' + total;
            document.getElementById('cart-list').innerHTML = cart.length ? cart.map(i => `
                <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f5f5f5;">
                    <span>${i.name} x ${i.qty}</span><span>$${i.price*i.qty}</span>
                </div>`).join('') : '<p style="text-align:center; color:#999;">購物車是空的</p>';
        }

        function showStep(rid) {
            const r = recipes.find(x => x.id === rid);
            document.getElementById('step-title').innerText = r.name;
            document.getElementById('step-body').innerHTML = `<ol style="padding-left:20px;">${r.steps.map(s=>`<li>${s}</li>`).join('')}</ol>`;
            openModal('step');
        }
        
        function findRecipe() {
            const p = products.find(x => x.id === currentPid);
            alert(`正在為您尋找「${p.name}」相關食譜...`);
            switchPage('recipe');
        }

        function showCreateRecipe() {
            const name = prompt("請輸入食譜名稱：");
            if(name) {
                recipes.unshift({id:"C"+Date.now(), name:name, img:"https://via.placeholder.com/300?text="+name, cal:0, steps:["自訂步驟"]});
                renderRecipes();
            }
        }

        function openModal(id) { 
            const m = document.getElementById('modal-'+id);
            m.style.display = (window.innerWidth >= 768) ? 'flex' : 'block';
        }
        function closeModal(id) { document.getElementById('modal-'+id).style.display = 'none'; }

        window.onload = init;
    </script>
</body>
</html>
"""

final_html = html_template.replace("images/", BASE_URL)
components.html(final_html, height=1200, scrolling=True)
