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

st.set_page_config(page_title="食際行動家", layout="wide", initial_sidebar_state="collapsed")

html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body { font-family: "Microsoft JhengHei", sans-serif; background: #f4f6f8; margin: 0; padding-bottom: 80px; }
    :root { --primary: #d9534f; --text: #333; }

    /* RWD */
    .desktop-only { display: none !important; }
    .mobile-only { display: flex !important; }
    @media (min-width: 768px) {
        body { padding-top: 70px; padding-bottom: 0; }
        .desktop-only { display: flex !important; }
        .mobile-only { display: none !important; }
    }

    /* 卡片核心樣式 (最簡化結構，保證可點) */
    .grid { display: grid; gap: 15px; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); padding: 10px; }
    .card { 
        background: white; border-radius: 12px; overflow: hidden; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); cursor: pointer; position: relative;
        display: flex; flex-direction: column;
    }
    .card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .card-img { width: 100%; height: 140px; object-fit: cover; }
    .card-body { padding: 10px; display: flex; flex-direction: column; flex-grow: 1; }
    .card-title { font-weight: bold; margin-bottom: 5px; color: #333; }
    .price { color: var(--primary); font-weight: bold; margin-top: auto; }
    
    /* 狀態標籤 */
    .status-badge { font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; }
    .good { background: #d4edda; color: #155724; }
    .bad { background: #f8d7da; color: #721c24; }

    /* 按鈕區 (重要：stopPropagation) */
    .card-btns { display: flex; gap: 5px; margin-top: 10px; }
    .s-btn { flex: 1; padding: 6px; border-radius: 6px; border: 1px solid #ddd; background: white; cursor: pointer; }
    .p-btn { flex: 1; padding: 6px; border-radius: 6px; border: none; background: var(--primary); color: white; cursor: pointer; }
    .ai-btn-card { width: 100%; margin-top: 5px; padding: 6px; background: #e3f2fd; color: #1976d2; border: 1px solid #90caf9; border-radius: 6px; cursor: pointer; font-weight: bold; }

    /* 其他 UI */
    #splash { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white; z-index: 9999; display: flex; align-items: center; justify-content: center; transition: 0.5s; }
    .splash-img { width: 100%; height: 100%; object-fit: cover; }
    
    .banner { width: 100%; height: 160px; border-radius: 15px; overflow: hidden; margin-bottom: 15px; }
    .banner img { width: 100%; height: 100%; object-fit: cover; }
    
    .cat-bar { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 10px; }
    .cat-btn { white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid #ddd; background: white; cursor: pointer; }
    .cat-btn.active { background: var(--primary); color: white; border-color: var(--primary); }

    /* Modal */
    .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 6000; }
    .modal-box { position: absolute; bottom: 0; width: 100%; max-height: 85vh; background: white; border-radius: 20px 20px 0 0; padding: 20px; display: flex; flex-direction: column; }
    @media (min-width: 768px) { 
        .modal { align-items: center; justify-content: center; } 
        .modal-box { position: relative; width: 500px; border-radius: 15px; bottom: auto; } 
    }
    
    /* Form */
    .form-group { margin-bottom: 10px; }
    .form-input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
    .ai-gen-btn { width: 100%; padding: 12px; background: linear-gradient(45deg, #17a2b8, #2c3e50); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px; }

    /* Detail Page */
    .page { display: none; animation: fadeIn 0.3s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .detail-hero img { width: 100%; height: 300px; object-fit: cover; }
    .detail-info { padding: 20px; background: white; border-radius: 20px 20px 0 0; margin-top: -20px; position: relative; }
    
    /* Nav */
    .nav-bar { position: fixed; bottom: 0; width: 100%; height: 60px; background: white; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #eee; z-index: 5000; }
    .desktop-nav { position: fixed; top: 0; width: 100%; height: 60px; background: white; display: flex; justify-content: space-between; align-items: center; padding: 0 40px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 5000; }
</style>
</head>
<body>

    <div id="splash" onclick="this.style.opacity=0; setTimeout(()=>this.style.display='none',500)">
        <img src="images/食際行動家.png" class="splash-img">
    </div>

    <div class="desktop-nav desktop-only">
        <div onclick="location.reload()" style="cursor:pointer; font-weight:bold;">⬅ 登出</div>
        <div>
            <button onclick="showPage('market')" style="border:none; bg:none; cursor:pointer;">市集</button>
            <button onclick="showPage('recipe')" style="border:none; bg:none; cursor:pointer; margin-left:20px;">食譜</button>
            <button onclick="openModal('cart')" style="border:none; bg:none; cursor:pointer; margin-left:20px;">購物車</button>
        </div>
    </div>

    <div class="container" style="max-width:1000px; margin:0 auto; padding:15px;">
        
        <div id="page-market" class="page" style="display:block;">
             <div class="banner"><img src="images/食際行動家.png"></div>
             <div class="cat-bar">
                 <button class="cat-btn" onclick="filter('水果',this)">🍎 水果</button>
                 <button class="cat-btn" onclick="filter('蔬菜',this)">🥦 蔬菜</button>
                 <button class="cat-btn" onclick="filter('肉品',this)">🥩 肉品</button>
                 <button class="cat-btn" onclick="filter('海鮮',this)">🐟 海鮮</button>
             </div>
             <div id="grid-products" class="grid">
                 <div style="grid-column:1/-1; text-align:center; padding:50px; color:#999;">請點擊上方分類</div>
             </div>
        </div>

        <div id="page-recipe" class="page">
            <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
                <h2>食譜牆</h2>
                <button onclick="openCreate()" style="background:white; border:1px solid #333; padding:5px 15px; border-radius:15px; cursor:pointer;">＋ 自訂</button>
            </div>
            <input type="text" id="search" placeholder="搜尋食譜 (試試酪梨)..." oninput="renderRecipes()" class="form-input" style="margin-bottom:15px;">
            <div id="grid-recipes" class="grid"></div>
        </div>

        <div id="page-detail" class="page">
            <div class="detail-hero"><button onclick="showPage('market')" style="position:absolute; top:15px; left:15px; padding:5px 10px; border-radius:50%; border:none; cursor:pointer;">⬅</button><img id="d-img" src=""></div>
            <div class="detail-info">
                <h1 id="d-name"></h1>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span id="d-price" style="color:#d9534f; font-size:1.5rem; font-weight:bold;"></span>
                    <span id="d-badge" class="status-badge"></span>
                </div>
                <hr style="border:0; border-top:1px solid #eee; margin:15px 0;">
                <p style="line-height:1.6; color:#666;">產地: <span id="d-origin"></span><br>保存: <span id="d-storage"></span><br>到期: <span id="d-expiry"></span><br>外觀: <span id="d-cond"></span></p>
                <button class="ai-gen-btn" style="background:var(--primary);" onclick="addToCart()">加入購物車</button>
                <button class="ai-gen-btn" style="background:white; color:#333; border:1px solid #ccc;" onclick="autoGenFromDetail()">⚡ 生成食譜</button>
            </div>
        </div>

    </div>

    <div class="nav-bar mobile-only">
        <div class="nav-item" onclick="showPage('market')">🥦<br>市集</div>
        <div class="nav-item" onclick="showPage('recipe')">👨‍🍳<br>食譜</div>
        <div class="nav-item" onclick="openModal('cart')">🛒<br>購物車</div>
    </div>

    <div id="modal-create" class="modal" onclick="if(event.target===this)closeModal('create')">
        <div class="modal-box">
            <h3>新增私房食譜</h3>
            <input type="text" id="c-name" class="form-input" placeholder="食譜名稱">
            <div style="margin:10px 0; font-weight:bold;">選擇食材 (觸發彩蛋關鍵)：</div>
            <div id="ing-selects" style="display:flex; flex-wrap:wrap; gap:5px;"></div>
            <div id="selected-ings" style="margin-top:10px; color:var(--primary);"></div>
            
            <button class="ai-gen-btn" onclick="aiGenerate()">🎲 AI 隨機生成 (含彩蛋)</button>
            <button class="ai-gen-btn" style="background:#28a745;" onclick="publishRecipe()">發布</button>
        </div>
    </div>

    <div id="modal-cart" class="modal" onclick="if(event.target===this)closeModal('cart')">
        <div class="modal-box">
            <h3>購物車</h3>
            <div id="cart-items"></div>
            <button class="ai-gen-btn" onclick="alert('結帳成功');cart=[];renderCart();closeModal('cart')">結帳</button>
        </div>
    </div>

    <div id="modal-view" class="modal" onclick="if(event.target===this)closeModal('view')">
        <div class="modal-box">
            <h3 id="v-title"></h3>
            <div id="v-content" style="overflow-y:auto; max-height:60vh;"></div>
            <button class="ai-gen-btn" style="background:#666;" onclick="closeModal('view')">關閉</button>
        </div>
    </div>

    <script>
        function getFutureDate(d) { const date = new Date(); date.setDate(date.getDate()+d); return date.toISOString().split('T')[0]; }

        const products = [
            { id: "P1", name: "蘋果", price: 139, img: "images/蘋果.jpg", cat: "水果", origin: "美國", storage: "冷藏", date: getFutureDate(6), cond: "良好" },
            { id: "P2", name: "香蕉", price: 80, img: "images/香蕉.jpg", cat: "水果", origin: "台灣", storage: "常溫", date: getFutureDate(3), cond: "破損" },
            { id: "P3", name: "高麗菜", price: 160, img: "images/高麗菜.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(7), cond: "良好" },
            { id: "P4", name: "番茄", price: 70, img: "images/番茄.JPG", cat: "蔬菜", origin: "台灣", storage: "冷藏", date: getFutureDate(5), cond: "破損" },
            { id: "P16", name: "豬肉", price: 220, img: "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400", cat: "肉品", origin: "台灣", storage: "冷凍", date: getFutureDate(30), cond: "良好" },
            { id: "P17", name: "牛肉", price: 450, img: "https://images.unsplash.com/photo-1613482184648-47399b2df699?w=400", cat: "肉品", origin: "美國", storage: "冷凍", date: getFutureDate(30), cond: "良好" },
            { id: "P20", name: "鮭魚切片", price: 350, img: "https://images.unsplash.com/photo-1599084993091-1cb5c0721cc6?w=400", cat: "海鮮", origin: "挪威", storage: "冷凍", date: getFutureDate(15), cond: "良好" }
        ];

        let recipes = [
            { id: "R1", name: "綜合蔬果沙拉", img: "images/綜合蔬果沙拉.jpg", ings: ["蘋果", "番茄"], steps: ["切塊", "拌勻"] },
            { id: "H1", name: "奶油酪梨雞胸肉佐蒜香地瓜葉", img: "https://images.unsplash.com/photo-1606756790138-7c48643e2912?w=400", ings: ["雞胸肉", "酪梨"], steps: ["煎雞胸", "酪梨壓泥", "混合"], hidden: true }
        ];

        let cart = [];
        let tempIngs = [];
        let curPid = null;

        // 頁面切換
        function showPage(pid) {
            document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
            document.getElementById('page-'+pid).style.display = 'block';
            window.scrollTo(0,0);
            if(pid==='recipe') renderRecipes();
        }

        // 渲染商品 (卡片點擊修復核心)
        function renderProds(list) {
            const div = document.getElementById('grid-products');
            if(list.length===0) { div.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#999;">請點擊上方分類</div>'; return; }
            div.innerHTML = list.map(p => {
                let badge = p.cond==='良好' ? '<span class="status-badge good">✅ 良好</span>' : '<span class="status-badge bad">⚠️ 破損</span>';
                return `
                <div class="card" onclick="goDetail('${p.id}')">
                    <img src="${p.img}" class="card-img">
                    <div class="card-body">
                        <div class="card-title">${p.name}</div>
                        <div>${badge}</div>
                        <div class="price">$${p.price}</div>
                        <div class="card-btns">
                            <button class="s-btn" onclick="event.stopPropagation(); goDetail('${p.id}')">詳細</button>
                            <button class="p-btn" onclick="event.stopPropagation(); addCart('${p.id}')">加入</button>
                        </div>
                        <button class="ai-btn-card" onclick="event.stopPropagation(); quickGen('${p.name}')">➕ 加入食譜</button>
                    </div>
                </div>`;
            }).join('');
        }

        function filter(cat, btn) {
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderProds(products.filter(p => p.cat === cat));
        }

        // 詳情頁
        function goDetail(id) {
            curPid = id;
            const p = products.find(x => x.id === id);
            document.getElementById('d-img').src = p.img;
            document.getElementById('d-name').innerText = p.name;
            document.getElementById('d-price').innerText = '$'+p.price;
            document.getElementById('d-origin').innerText = p.origin;
            document.getElementById('d-storage').innerText = p.storage;
            document.getElementById('d-expiry').innerText = p.date;
            document.getElementById('d-cond').innerText = p.cond;
            document.getElementById('d-badge').innerText = p.cond;
            document.getElementById('d-badge').className = p.cond==='良好' ? 'status-badge good' : 'status-badge bad';
            showPage('detail');
        }

        // 購物車
        function addCart(id) {
            const t = id || curPid;
            const p = products.find(x => x.id === t);
            const exist = cart.find(x => x.id === t);
            if(exist) exist.qty++; else cart.push({...p, qty:1});
            alert('已加入購物車');
            renderCart();
        }
        function renderCart() {
            document.getElementById('cart-items').innerHTML = cart.length ? cart.map(i => 
                `<div style="display:flex;justify-content:space-between;padding:10px;border-bottom:1px solid #eee;">
                    <span>${i.name} x ${i.qty}</span><span>$${i.price*i.qty}</span>
                </div>`).join('') : '購物車是空的';
        }

        // 食譜系統
        function renderRecipes() {
            const kw = document.getElementById('search').value.trim();
            const list = recipes.filter(r => {
                if(r.hidden) return kw.includes('酪梨');
                if(!kw) return true;
                return r.name.includes(kw);
            });
            document.getElementById('grid-recipes').innerHTML = list.map(r => `
                <div class="card" onclick="viewRecipe('${r.id}')">
                    <img src="${r.img}" class="card-img" onerror="this.src='https://via.placeholder.com/300'">
                    <div class="card-body">
                        <div class="card-title">${r.name}</div>
                        <button class="s-btn">查看做法</button>
                    </div>
                </div>`).join('');
        }
        function viewRecipe(id) {
            const r = recipes.find(x => x.id === id);
            document.getElementById('v-title').innerText = r.name;
            document.getElementById('v-content').innerHTML = `<b>食材：</b><br>${r.ings.join(', ')}<br><br><b>步驟：</b><br>${r.steps.join('<br>')}`;
            openModal('view');
        }

        // 自訂食譜 & AI
        function openCreate() {
            tempIngs = [];
            document.getElementById('c-name').value = '';
            document.getElementById('ing-selects').innerHTML = products.map(p => 
                `<button class="cat-btn" onclick="toggleIng(this, '${p.name}')">${p.name}</button>`
            ).join('');
            // 手動添加觸發彩蛋的食材按鈕
            document.getElementById('ing-selects').innerHTML += 
                `<button class="cat-btn" onclick="toggleIng(this, '酪梨')">酪梨</button>
                 <button class="cat-btn" onclick="toggleIng(this, '雞胸肉')">雞胸肉</button>`;
            document.getElementById('selected-ings').innerText = '';
            openModal('create');
        }
        function toggleIng(btn, name) {
            if(tempIngs.includes(name)) {
                tempIngs = tempIngs.filter(x => x !== name);
                btn.classList.remove('active');
            } else {
                tempIngs.push(name);
                btn.classList.add('active');
            }
            document.getElementById('selected-ings').innerText = '已選: ' + tempIngs.join(', ');
        }
        function aiGenerate() {
            if(tempIngs.includes('酪梨') && tempIngs.includes('雞胸肉')) {
                document.getElementById('c-name').value = '奶油酪梨雞胸肉佐蒜香地瓜葉';
                alert('🥑 觸發隱藏菜單！');
            } else {
                document.getElementById('c-name').value = 'AI 特製' + (tempIngs[0] || '創意') + '料理';
            }
        }
        function publishRecipe() {
            const name = document.getElementById('c-name').value;
            if(name === '奶油酪梨雞胸肉佐蒜香地瓜葉') {
                const h = recipes.find(r => r.id === 'H1');
                recipes.unshift({...h, id:'U'+Date.now(), hidden:false});
            } else {
                recipes.unshift({id:'C'+Date.now(), name:name, img:'https://via.placeholder.com/300?text='+name, ings:tempIngs, steps:['AI 生成步驟...']});
            }
            closeModal('create');
            showPage('recipe');
        }
        function quickGen(name) {
            recipes.unshift({id:'Q'+Date.now(), name:name+'特餐', img:'https://via.placeholder.com/300?text='+name, ings:[name], steps:['簡單料理']});
            viewRecipe(recipes[0].id);
        }
        
        function autoGenFromDetail() {
            const p = products.find(x => x.id === curPid);
            quickGen(p.name);
        }

        function openModal(id) { document.getElementById('modal-'+id).style.display = 'flex'; }
        function closeModal(id) { document.getElementById('modal-'+id).style.display = 'none'; }
        
        window.onload = function() {
            renderProds([]); // 初始不顯示商品
            renderRecipes();
        }
    </script>
</body>
</html>
"""

final_html = html_template.replace("images/", BASE_URL)
components.html(final_html, height=1200, scrolling=True)
