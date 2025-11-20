import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 👇 GitHub 設定
# ==========================================
GITHUB_USER = "ShadowREddd"
REPO_NAME = "-"
BRANCH_NAME = "main"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH_NAME}/"
# ==========================================

st.set_page_config(page_title="食際行動家(電腦版)", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <style>
        /* --- 電腦版核心樣式 --- */
        body { font-family: "Microsoft JhengHei", sans-serif; background: #f4f6f8; margin: 0; }
        
        /* 頂部導覽列 (Web 風格) */
        .top-nav {
            background: white; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 1000;
        }
        .logo { font-size: 1.5rem; font-weight: bold; color: #333; cursor: pointer; }
        .nav-links button {
            background: none; border: none; font-size: 1rem; margin-left: 20px; cursor: pointer; color: #666; transition: 0.2s;
        }
        .nav-links button:hover, .nav-links button.active { color: #d9534f; font-weight: bold; }
        .cart-btn { background: #d9534f !important; color: white !important; padding: 8px 20px; border-radius: 20px; }

        /* 容器 */
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
        
        /* 商品網格 (電腦多欄) */
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 25px; }
        .card { 
            background: white; border-radius: 10px; overflow: hidden; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s; border: 1px solid #eee;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .card-img { width: 100%; height: 200px; object-fit: cover; }
        .card-body { padding: 15px; }
        .card-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 10px; }
        .price { color: #d9534f; font-size: 1.2rem; font-weight: bold; }

        /* 詳情頁 (左右佈局) */
        .detail-layout { display: flex; gap: 40px; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .detail-left { flex: 1; }
        .detail-right { flex: 1; display: flex; flex-direction: column; justify-content: center; }
        .detail-img { width: 100%; border-radius: 10px; }
        
        /* 按鈕 */
        .btn { padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; transition: 0.2s; }
        .btn-primary { background: #d9534f; color: white; }
        .btn-primary:hover { background: #c9302c; }
        .btn-secondary { background: #f0f0f0; color: #333; }
        .btn-secondary:hover { background: #e0e0e0; }

        /* 彈跳視窗 (中央顯示) */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 2000; justify-content: center; align-items: center; }
        .modal-box { background: white; width: 500px; padding: 30px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }

        /* 頁面切換 */
        .page { display: none; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body>

    <div class="top-nav">
        <div class="logo" onclick="switchPage('market')">食際行動家 💻</div>
        <div class="nav-links">
            <button id="nav-market" class="active" onclick="switchPage('market')">生鮮市集</button>
            <button id="nav-recipe" onclick="switchPage('recipe')">食譜牆</button>
            <button class="cart-btn" onclick="openModal('cart')">購物車 (<span id="cart-count">0</span>)</button>
        </div>
    </div>

    <div class="container">
        <div id="page-market" class="page" style="display:block;">
            <div id="grid-products" class="grid"></div>
        </div>

        <div id="page-recipe" class="page">
            <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
                <h2>精選食譜</h2>
                <button class="btn btn-primary" onclick="alert('電腦版自訂食譜功能開發中')">＋ 新增食譜</button>
            </div>
            <div id="grid-recipes" class="grid"></div>
        </div>

        <div id="page-detail" class="page">
            <button class="btn btn-secondary" onclick="switchPage('market')" style="margin-bottom:20px;">← 返回列表</button>
            <div class="detail-layout">
                <div class="detail-left">
                    <img id="dt-img" class="detail-img" src="">
                </div>
                <div class="detail-right">
                    <h1 id="dt-name" style="font-size:2.5rem; margin-bottom:10px;"></h1>
                    <div id="dt-price" style="color:#d9534f; font-size:2rem; font-weight:bold; margin-bottom:20px;"></div>
                    <p style="font-size:1.2rem; color:#666; line-height:1.8;">
                        產地：<span id="dt-origin"></span><br>
                        保存方式：<span id="dt-storage"></span>
                    </p>
                    <div style="margin-top:30px; display:flex; gap:15px;">
                        <button class="btn btn-primary" onclick="addToCart()">＋ 加入購物車</button>
                        <button class="btn btn-secondary" onclick="findRecipe()">📖 查看相關食譜</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="modal-cart" class="modal-overlay" onclick="if(event.target===this) closeModal('cart')">
        <div class="modal-box">
            <h2 style="margin-top:0;">我的購物車</h2>
            <div id="cart-list" style="max-height:300px; overflow-y:auto; margin:20px 0; border-top:1px solid #eee; border-bottom:1px solid #eee;"></div>
            <div style="text-align:right; font-size:1.2rem; font-weight:bold; margin-bottom:20px;">
                總計：<span id="cart-total">$0</span>
            </div>
            <div style="text-align:right;">
                <button class="btn btn-secondary" onclick="closeModal('cart')">繼續購物</button>
                <button class="btn btn-primary" onclick="alert('結帳成功！'); cart=[]; updateCartUI(); closeModal('cart')">前往結帳</button>
            </div>
        </div>
    </div>

    <script>
        // 資料庫 (與手機版相同)
        const products = [
            {id:"P1", name:"蘋果", price:139, img:"images/蘋果.jpg", origin:"美國", storage:"冷藏"},
            {id:"P2", name:"香蕉", price:80, img:"images/香蕉.jpg", origin:"台灣", storage:"常溫"},
            {id:"P3", name:"高麗菜", price:160, img:"images/高麗菜.JPG", origin:"台灣", storage:"冷藏"},
            {id:"P4", name:"番茄", price:70, img:"images/番茄.JPG", origin:"台灣", storage:"冷藏"},
            {id:"P5", name:"洋蔥", price:50, img:"images/洋蔥.jpg", origin:"美國", storage:"常溫"},
            {id:"P6", name:"地瓜", price:190, img:"images/地瓜.jpg", origin:"台灣", storage:"常溫"},
            {id:"P7", name:"柳橙", price:120, img:"images/柳橙.JPG", origin:"美國", storage:"冷藏"},
            {id:"P8", name:"菠菜", price:90, img:"images/菠菜.JPG", origin:"台灣", storage:"冷藏"},
            {id:"P9", name:"胡蘿蔔", price:60, img:"images/胡蘿蔔.jpg", origin:"韓國", storage:"冷藏"},
            {id:"P10", name:"鳳梨", price:155, img:"images/鳳梨.jpg", origin:"美國", storage:"冷凍"}
        ];
        
        const recipes = [
            {id:"R1", name:"綜合蔬果沙拉", img:"images/綜合蔬果沙拉.jpg", cal:220},
            {id:"R2", name:"番茄炒高麗菜", img:"images/番茄炒高麗菜.jpg", cal:180},
            {id:"R3", name:"蜂蜜烤地瓜", img:"images/蜂蜜烤地瓜.jpg", cal:250},
            {id:"R4", name:"鳳梨蘋果汁", img:"images/鳳梨蘋果汁.jpg", cal:150},
            {id:"R5", name:"香蕉柳橙冰沙", img:"images/香蕉柳橙冰沙.jpg", cal:180},
            {id:"R6", name:"義式烤蔬菜", img:"images/義式烤蔬菜.jpg", cal:200}
        ];

        let cart = [];
        let currentPid = null;

        function init() {
            // 渲染商品
            document.getElementById('grid-products').innerHTML = products.map(p => `
                <div class="card" onclick="showDetail('${p.id}')">
                    <img src="${p.img}" class="card-img">
                    <div class="card-body">
                        <div class="card-title">${p.name}</div>
                        <div class="price">$${p.price}</div>
                    </div>
                </div>
            `).join('');

            // 渲染食譜
            document.getElementById('grid-recipes').innerHTML = recipes.map(r => `
                <div class="card" onclick="alert('食譜詳情：${r.name}')">
                    <img src="${r.img}" class="card-img" onerror="this.src='https://via.placeholder.com/300'">
                    <div class="card-body">
                        <div class="card-title">${r.name}</div>
                        <div style="color:#666;">🔥 ${r.cal} kcal</div>
                    </div>
                </div>
            `).join('');
        }

        function switchPage(page) {
            document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
            document.getElementById('nav-market').classList.remove('active');
            document.getElementById('nav-recipe').classList.remove('active');
            
            if(page === 'market') document.getElementById('nav-market').classList.add('active');
            if(page === 'recipe') document.getElementById('nav-recipe').classList.add('active');
            
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

        function findRecipe() {
            switchPage('recipe');
            alert('已為您篩選相關食譜 (模擬)');
        }

        function updateCartUI() {
            const count = cart.reduce((sum, i) => sum + i.qty, 0);
            const total = cart.reduce((sum, i) => sum + i.price*i.qty, 0);
            document.getElementById('cart-count').innerText = count;
            document.getElementById('cart-total').innerText = '$' + total;
            document.getElementById('cart-list').innerHTML = cart.length ? cart.map(i => `
                <div style="display:flex; justify-content:space-between; padding:10px; border-bottom:1px solid #eee;">
                    <span>${i.name} x ${i.qty}</span>
                    <span>$${i.price * i.qty}</span>
                </div>
            `).join('') : '<p style="text-align:center; color:#999;">購物車是空的</p>';
        }

        function openModal(id) { document.getElementById('modal-'+id).style.display = 'flex'; }
        function closeModal(id) { document.getElementById('modal-'+id).style.display = 'none'; }

        window.onload = init;
    </script>
</body>
</html>
"""

# 電腦版圖片路徑替換
final_desktop_html = html_code.replace("images/", BASE_URL)
components.html(final_desktop_html, height=1200, scrolling=True)
