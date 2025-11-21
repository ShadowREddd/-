import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 👇 您的 GitHub 資訊
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
<title>食際行動家</title>
<style>
* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
body { font-family: "Microsoft JhengHei", sans-serif; background: #f4f6f8; margin: 0; padding-bottom: 80px; overflow-x: hidden; }
:root { --primary: #d9534f; --text: #333; --bg: #fff; }
.desktop-only { display: none !important; } .mobile-only { display: flex !important; }
@media (min-width: 768px) { body { padding-top: 70px; padding-bottom: 0; } .desktop-only { display: flex !important; } .mobile-only { display: none !important; } }
#splash { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: white; z-index: 99999; display: flex; justify-content: center; align-items: center; transition: opacity 0.5s; cursor: pointer; }
.splash-logo { width: 100%; height: 100%; object-fit: cover; animation: breathe 3s infinite; }
@keyframes breathe { 0%,100% { transform: scale(1); opacity: 0.95; } 50% { transform: scale(1.02); opacity: 1; } }
#login-page { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #fff; z-index: 8000; flex-direction: column; justify-content: center; align-items: center; padding: 20px; }
.login-card { width: 100%; max-width: 400px; text-align: center; }
.login-input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; background: #f9f9f9; }
.login-btn { width: 100%; padding: 15px; background: var(--primary); color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
#main-app { display: none; opacity: 0; transition: opacity 0.5s; }
.bottom-nav { position: fixed; bottom: 0; width: 100%; height: 65px; background: white; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #eee; z-index: 5000; }
.nav-item { flex: 1; text-align: center; font-size: 0.75rem; background:none; border:none; cursor: pointer; }
.nav-item.active { color: var(--primary); font-weight: bold; }
.nav-icon { font-size: 1.4rem; display: block; }
.top-nav { position: fixed; top: 0; width: 100%; height: 70px; background: white; display: flex; justify-content: space-between; align-items: center; padding: 0 50px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); z-index: 5000; }
.container { max-width: 1200px; margin: 0 auto; padding: 15px; }
.banner-container { width: 100%; height: 180px; border-radius: 15px; overflow: hidden; position: relative; margin-bottom: 20px; }
.banner-img { width: 100%; height: 100%; object-fit: cover; }
.category-bar { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 15px; }
.category-bar::-webkit-scrollbar { display: none; }
.cat-btn { white-space: nowrap; padding: 8px 16px; border-radius: 20px; border: 1px solid #ddd; background: white; color: #666; cursor: pointer; }
.cat-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
.grid { display: grid; gap: 15px; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); }
.card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; flex-direction: column; position: relative; cursor: pointer; }
.card-top-click { cursor: pointer; flex-grow: 1; }
.card-img { width: 100%; height: 150px; object-fit: cover; pointer-events: none; }
.card-body { padding: 10px; flex-grow: 1; display: flex; flex-direction: column; pointer-events: none; }
.card-title { font-weight: bold; margin-bottom: 5px; font-size: 1.05rem; color: #333; }
.price { color: var(--primary); font-weight: bold; font-size: 1.2rem; float: right; }
.card-info-list { font-size: 0.85rem; color: #666; margin: 8px 0; border-top: 1px dashed #eee; padding-top: 8px; }
.status-badge { display: inline-block; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; vertical-align: middle; }
.status-good { background: #d4edda; color: #155724; } .status-bad { background: #f8d7da; color: #721c24; }
.card-bottom-actions { padding: 10px; background: white; display: flex; flex-direction: column; gap: 8px; pointer-events: auto; }
.btn-add-cart { width: 100%; padding: 8px; background: var(--primary); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
.btn-gen-recipe { width: 100%; padding: 8px; background: #e3f2fd; border: 1px solid #90caf9; color: #1976d2; border-radius: 6px; cursor: pointer; font-weight: bold; }
.detail-wrapper { display: flex; flex-direction: column; background: white; }
@media(min-width:768px){ .detail-wrapper{flex-direction:row; padding:40px; gap:40px;} .detail-hero{flex:1;} .detail-info{flex:1;} }
.detail-hero img { width: 100%; height: 300px; object-fit: cover; }
.detail-info { padding: 20px; }
.back-btn { position: absolute; top: 20px; left: 20px; padding: 10px 20px; border-radius: 30px; background: rgba(255,255,255,0.9); border: none; font-weight: bold; cursor: pointer; z-index: 10; }
.modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 6000; align-items: center; justify-content: center; }
.modal-content { width: 90%; max-width: 500px; max-height: 85vh; background: white; border-radius: 15px; padding: 20px; display: flex; flex-direction: column; overflow-y: auto; }
.chat-fab { position: fixed; bottom: 80px; right: 20px; z-index: 5500; padding: 12px 20px; border-radius: 30px; background: #2c3e50; color: white; border: none; font-weight: bold; cursor: pointer; }
#chat-widget { display: none; position: fixed; bottom: 150px; right: 20px; width: 320px; height: 450px; background: #fff; border-radius: 15px; box-shadow: 0 5px 25px rgba(0,0,0,0.2); z-index: 5600; flex-direction: column; }
.form-input, .form-select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; }
.ai-magic-btn { width: 100%; padding: 12px; background: linear-gradient(45deg, #17a2b8, #2c3e50); color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-bottom: 10px; }
</style>
</head>
<body>
    <div id="splash" onclick="goToLogin()"><img src="images/食際行動家.png" class="splash-logo"></div>
    <div id="login-page"><div class="login-card"><img src="images/食際行動家.png" style="width:120px;margin-bottom:20px;"><div class="login-title">歡迎回來</div><input type="text" class="login-input" placeholder="使用者帳號"><input type="password" class="login-input" placeholder="密碼"><button class="login-btn" onclick="performLogin()">登入</button></div></div>
    
    <div id="main-app">
        <button class="chat-fab" onclick="toggleChat()">[客服]</button>
        <div id="chat-widget">
            <div style="background:#2c3e50;color:white;padding:15px;display:flex;justify-content:space-between;"><span>線上客服</span><span onclick="toggleChat()" style="cursor:pointer;">[關閉]</span></div>
            <div id="chat-body" style="flex:1;padding:15px;overflow-y:auto;"><div style="background:#eee;padding:10px;border-radius:10px;width:fit-content;">您好！請問有什麼需要幫忙的嗎？</div></div>
            <div style="padding:10px;border-top:1px solid #eee;display:flex;gap:5px;"><input type="text" id="chat-input" class="form-input" style="margin:0;" placeholder="輸入訊息..." onkeypress="if(event.key==='Enter')sendChat()"><button onclick="sendChat()" style="background:#d9534f;color:white;border:none;padding:0 15px;border-radius:8px;">傳送</button></div>
        </div>

        <div class="top-nav desktop-only">
            <div style="font-weight:bold;cursor:pointer;" onclick="location.reload()">[返回/登出]</div>
            <div><button onclick="switchPage('market')" style="border:none;background:none;cursor:pointer;margin-left:20px;">首頁</button><button onclick="switchPage('recipe')" style="border:none;background:none;cursor:pointer;margin-left:20px;">食譜</button><button onclick="openModal('cart')" style="border:none;background:none;cursor:pointer;margin-left:20px;">購物車(<span class="cart-count">0</span>)</button></div>
        </div>

        <div class="container">
            <div id="page-market" class="page" style="display:block;">
                <div class="mobile-top-bar mobile-only" style="padding:10px;"><div style="font-weight:bold;" onclick="location.reload()">[返回/登出]</div></div>
                <div class="banner-container"><img src="images/食際行動家.png" class="banner-img"></div>
                <div class="category-bar">
                    <button class="cat-btn" onclick="filterCat('水果',this)">[水果]</button>
                    <button class="cat-btn" onclick="filterCat('蔬菜',this)">[蔬菜]</button>
                    <button class="cat-btn" onclick="filterCat('菇類',this)">[菇類]</button>
                    <button class="cat-btn" onclick="filterCat('肉品',this)">[肉品]</button>
                    <button class="cat-btn" onclick="filterCat('海鮮',this)">[海鮮]</button>
                </div>
                <div id="grid-products" class="grid"><div style="grid-column:1/-1;text-align:center;padding:50px;color:#888;">[請選擇分類]</div></div>
            </div>

            <div id="page-recipe" class="page">
                <div style="display:flex;justify-content:space-between;margin-bottom:15px;"><h2>食譜牆</h2><button onclick="openCreate()" style="border:1px solid #ddd;background:white;padding:5px 15px;border-radius:20px;cursor:pointer;">[自訂食譜]</button></div>
                <input type="text" id="r-search" class="form-input" placeholder="搜尋食譜..." oninput="renderRecipes()">
                <div id="grid-recipes" class="grid"></div>
            </div>

            <div id="page-detail" class="page">
                <button class="back-btn" onclick="switchPage('market')">[返回列表]</button>
                <div class="detail-wrapper">
                    <div class="detail-hero"><img id="dt-img" src=""></div>
                    <div class="detail-info">
                        <h1 id="dt-name"></h1>
                        <div style="margin:10px 0;"><span id="dt-badge" style="padding:5px 10px;border-radius:4px;color:white;"></span><span id="dt-price" style="float:right;color:#d9534f;font-size:1.5rem;font-weight:bold;"></span></div>
                        <div style="line-height:1.8;color:#666;">[產地]: <span id="dt-org"></span><br>[保存]: <span id="dt-sto"></span><br>[到期]: <span id="dt-exp"></span><br>[外觀]: <span id="dt-cond"></span></div>
                        <div style="margin-top:20px;display:flex;gap:10px;"><button class="login-btn" onclick="addCart()">[加入購物車]</button><button class="login-btn" style="background:#e3f2fd;color:#1976d2;border:1px solid #90caf9;" onclick="quickGen()">[推薦做法]</button></div>
                    </div>
                </div>
            </div>

            <div id="page-backend" class="page">
                <div style="display:flex;justify-content:space-between;margin-bottom:20px;"><h2>後台管理</h2><button onclick="switchPage('market')" style="border:1px solid #ddd;background:white;padding:5px 10px;border-radius:5px;">返回</button></div>
                <table class="admin-table"><thead><tr><th>名稱</th><th>狀態</th><th>價格</th></tr></thead><tbody id="admin-list"></tbody></table>
            </div>
        </div>

        <div class="bottom-nav mobile-only">
            <button class="nav-item active" id="mb-market" onclick="switchPage('market')">首頁</button>
            <button class="nav-item" id="mb-recipe" onclick="switchPage('recipe')">食譜</button>
            <button class="nav-item" onclick="openModal('cart')">購物車(<span class="cart-count">0</span>)</button>
        </div>
    </div>

    <div id="modal-cart" class="modal" onclick="if(event.target===this)closeModal('cart')">
        <div class="modal-content">
            <div style="display:flex;justify-content:space-between;margin-bottom:15px;"><h3>購物車</h3><span onclick="closeModal('cart')" style="cursor:pointer;">[關閉]</span></div>
            <div id="cart-list" style="flex:1;overflow-y:auto;"></div>
            <div style="padding-top:10px;border-top:1px solid #eee;margin-top:10px;"><div style="display:flex;justify-content:space-between;font-weight:bold;"><span>總計</span><span id="cart-total">$0</span></div><button class="login-btn" style="margin-top:10px;" onclick="alert('結帳成功');cart=[];updCart();closeModal('cart')">前往結帳</button></div>
        </div>
    </div>

    <div id="modal-step" class="modal" onclick="if(event.target===this)closeModal('step')">
        <div class="modal-content">
            <div style="display:flex;justify-content:space-between;margin-bottom:15px;"><h3>料理步驟</h3><span onclick="closeModal('step')" style="cursor:pointer;">[關閉]</span></div>
            <div id="step-body" style="flex:1;overflow-y:auto;"></div>
        </div>
    </div>

    <div id="modal-create" class="modal" onclick="if(event.target===this)closeModal('create')">
        <div class="modal-content">
            <div style="display:flex;justify-content:space-between;margin-bottom:15px;"><h3>自訂食譜</h3><span onclick="closeModal('create')" style="cursor:pointer;">[關閉]</span></div>
            <button class="ai-magic-btn" onclick="aiGen()">[推薦做法]</button>
            <input type="text" id="new-name" class="form-input" placeholder="食譜名稱">
            <input type="number" id="new-cal" class="form-input" placeholder="卡路里">
            <div class="form-group"><label>選擇食材</label><div class="add-row"><select id="sel-ing" class="form-select"><option value="">--請選擇--</option></select><button class="add-btn-small" onclick="addIng()">+</button></div></div>
            <div class="form-group"><label>手動輸入</label><div class="add-row"><input type="text" id="man-ing" class="form-input" style="margin:0;" placeholder="食材..."><button class="add-btn-small" onclick="addMan()">+</button></div></div>
            <div id="ing-list" class="tag-container"></div>
            <button class="login-btn" style="margin-top:10px;" onclick="pubRecipe()">[發布食譜]</button>
        </div>
    </div>

    <script>
        const getDates=d=>{const t=new Date();t.setDate(t.getDate()+d);return t.toISOString().split('T')[0]};
        const products=[
            {id:"P1",name:"蘋果",price:139,img:"images/蘋果.jpg",cat:"水果",origin:"美國",storage:"冷藏",date:getDates(6),cond:"良好"},
            {id:"P2",name:"香蕉",price:80,img:"images/香蕉.jpg",cat:"水果",origin:"台灣",storage:"常溫",date:getDates(3),cond:"破損"},
            {id:"P7",name:"柳橙",price:120,img:"images/柳橙.JPG",cat:"水果",origin:"美國",storage:"冷藏",date:getDates(10),cond:"良好"},
            {id:"P10",name:"鳳梨",price:155,img:"images/鳳梨.jpg",cat:"水果",origin:"美國",storage:"冷凍",date:getDates(5),cond:"良好"},
            {id:"P3",name:"高麗菜",price:160,img:"images/高麗菜.JPG",cat:"蔬菜",origin:"台灣",storage:"冷藏",date:getDates(7),cond:"良好"},
            {id:"P4",name:"番茄",price:70,img:"images/番茄.JPG",cat:"蔬菜",origin:"台灣",storage:"冷藏",date:getDates(5),cond:"破損"},
            {id:"P5",name:"洋蔥",price:50,img:"images/洋蔥.jpg",cat:"蔬菜",origin:"美國",storage:"常溫",date:getDates(20),cond:"良好"},
            {id:"P6",name:"地瓜",price:190,img:"images/地瓜.jpg",cat:"蔬菜",origin:"台灣",storage:"常溫",date:getDates(14),cond:"良好"},
            {id:"P8",name:"菠菜",price:90,img:"images/菠菜.JPG",cat:"蔬菜",origin:"台灣",storage:"冷藏",date:getDates(2),cond:"破損"},
            {id:"P9",name:"胡蘿蔔",price:60,img:"images/胡蘿蔔.jpg",cat:"蔬菜",origin:"韓國",storage:"冷藏",date:getDates(8),cond:"良好"},
            {id:"P11",name:"花椰菜",price:55,img:"https://images.unsplash.com/photo-1568584711075-3d021a7c3d54?w=400",cat:"蔬菜",origin:"台灣",storage:"冷藏",date:getDates(5),cond:"良好"},
            {id:"P12",name:"甜玉米",price:40,img:"https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400",cat:"蔬菜",origin:"台灣",storage:"冷藏",date:getDates(7),cond:"良好"},
            {id:"P14",name:"彩椒",price:45,img:"https://images.unsplash.com/photo-1563565375-f3fdf5ecfae9?w=400",cat:"蔬菜",origin:"荷蘭",storage:"冷藏",date:getDates(12),cond:"良好"},
            {id:"P15",name:"馬鈴薯",price:35,img:"https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400",cat:"蔬菜",origin:"美國",storage:"常溫",date:getDates(30),cond:"破損"},
            {id:"P13",name:"鮮香菇",price:65,img:"https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400",cat:"菇類",origin:"台灣",storage:"冷藏",date:getDates(10),cond:"良好"},
            {id:"P16",name:"豬肉",price:220,img:"https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400",cat:"肉品",origin:"台灣",storage:"冷凍",date:getDates(30),cond:"良好"},
            {id:"P17",name:"牛肉",price:450,img:"https://images.unsplash.com/photo-1613482184648-47399b2df699?w=400",cat:"肉品",origin:"美國",storage:"冷凍",date:getDates(30),cond:"良好"},
            {id:"P20",name:"鮭魚切片",price:350,img:"https://images.unsplash.com/photo-1599084993091-1cb5c0721cc6?w=400",cat:"海鮮",origin:"挪威",storage:"冷凍",date:getDates(15),cond:"良好"}
        ];
        const recipes=[
            {id:"R1",name:"綜合蔬果沙拉",cal:220,img:"images/綜合蔬果沙拉.jpg",steps:["洗淨切塊","拌勻"],ings:["蘋果","番茄"]},
            {id:"R2",name:"番茄炒高麗菜",cal:180,img:"images/番茄炒高麗菜.jpg",steps:["爆香","炒熟"],ings:["番茄","高麗菜"]},
            {id:"R3",name:"蜂蜜烤地瓜",cal:250,img:"images/蜂蜜烤地瓜.jpg",steps:["洗淨","烤40分"],ings:["地瓜"]},
            {id:"R4",name:"鳳梨蘋果汁",cal:150,img:"images/鳳梨蘋果汁.jpg",steps:["切塊","打汁"],ings:["鳳梨","蘋果"]},
            {id:"R5",name:"香蕉柳橙冰沙",cal:180,img:"images/香蕉柳橙冰沙.jpg",steps:["加冰","打成冰沙"],ings:["香蕉","柳橙"]},
            {id:"R6",name:"義式烤蔬菜",cal:200,img:"images/義式烤蔬菜.jpg",steps:["切塊","烤熟"],ings:["胡蘿蔔","洋蔥"]},
            {id:"H1",name:"奶油酪梨雞胸肉佐蒜香地瓜葉",cal:450,img:"https://images.unsplash.com/photo-1606756790138-7c48643e2912?w=400",hidden:true,ings:["雞胸肉","酪梨","地瓜葉"],steps:["煎雞肉","酪梨壓泥","煨煮"]}
        ];
        let cart=[], curPid=null, tempIngs=[];

        function init(){ renderRecs(recipes.filter(r=>!r.hidden)); document.getElementById('sel-ing').innerHTML='<option value="">--請選擇--</option>'+products.map(p=>`<option value="${p.name}">${p.name}</option>`).join(''); }
        
        function goToLogin(){ document.getElementById('splash').style.display='none'; document.getElementById('login-page').style.display='flex'; }
        function performLogin(){ document.getElementById('login-page').style.display='none'; document.getElementById('main-app').style.display='block'; setTimeout(()=>document.getElementById('main-app').style.opacity=1,50); }
        
        function switchPage(p){ 
            document.querySelectorAll('.page').forEach(x=>x.style.display='none'); 
            document.getElementById('page-'+p).style.display='block'; 
            document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));
            if(document.getElementById('mb-'+p))document.getElementById('mb-'+p).classList.add('active');
            if(p==='market') filterCat('all',document.querySelectorAll('.cat-btn')[0]);
            window.scrollTo(0,0);
        }

        function renderProds(list){
            const d=document.getElementById('grid-products');
            if(!list.length){ d.innerHTML='<div style="grid-column:1/-1;text-align:center;padding:50px;color:#888;">[請選擇分類]</div>'; return; }
            d.innerHTML=list.map(p=>`
                <div class="card" onclick="goDetail('${p.id}')">
                    <div class="card-top-click">
                        <img src="${p.img}" class="card-img">
                        <div class="card-body">
                            <div class="card-title">${p.name}</div>
                            <div style="display:flex;justify-content:space-between;"><span class="status-badge ${p.cond==='良好'?'status-good':'status-bad'}">[狀態: ${p.cond}]</span><span class="price">$${p.price}</span></div>
                            <div class="card-info-list">[產地]: ${p.origin} | [保存]: ${p.storage}<br>[到期]: ${p.date}</div>
                        </div>
                    </div>
                    <div class="card-bottom-actions">
                        <button class="btn-add-cart" onclick="event.stopPropagation();addCart('${p.id}')">[加入購物車]</button>
                        <button class="btn-gen-recipe" onclick="event.stopPropagation();quickGen('${p.name}')">[加入食譜]</button>
                    </div>
                </div>`).join('');
        }

        function filterCat(c,b){ 
            document.querySelectorAll('.cat-btn').forEach(x=>x.classList.remove('active')); 
            if(b)b.classList.add('active');
            if(c==='all') renderProds([]); else renderProds(products.filter(p=>p.cat===c));
        }

        function goDetail(id){
            curPid=id; const p=products.find(x=>x.id===id);
            document.getElementById('dt-img').src=p.img;
            document.getElementById('dt-name').innerText=p.name;
            document.getElementById('dt-price').innerText='$'+p.price;
            document.getElementById('dt-org').innerText=p.origin;
            document.getElementById('dt-sto').innerText=p.storage;
            document.getElementById('dt-exp').innerText=p.date;
            document.getElementById('dt-cond').innerText='[狀態: '+p.cond+']';
            document.getElementById('dt-badge').innerText=p.cond==='良好'?'[良好]':'[破損]';
            document.getElementById('dt-badge').style.background=p.cond==='良好'?'#28a745':'#dc3545';
            switchPage('detail');
        }

        function addCart(id){ const t=id||curPid; const p=products.find(x=>x.id===t); const ex=cart.find(x=>x.id===t); if(ex)ex.qty++;else cart.push({...p,qty:1}); updCart(); alert('[已加入購物車]'); }
        function updCart(){ 
            const c=cart.reduce((a,b)=>a+b.qty,0); const t=cart.reduce((a,b)=>a+b.price*b.qty,0);
            document.querySelectorAll('.cart-count').forEach(x=>x.innerText=c); document.getElementById('cart-total').innerText='$'+t;
            document.getElementById('cart-list').innerHTML=cart.map(i=>`<div style="padding:10px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;"><div>${i.name}</div><div>$${i.price} x ${i.qty} <span onclick="delCart('${i.id}')" style="color:red;cursor:pointer;margin-left:5px;">[刪除]</span></div></div>`).join('');
        }
        function delCart(id){ cart=cart.filter(x=>x.id!==id); updCart(); }

        function quickGen(n){ 
            const nr={id:'Q'+Date.now(),name:'特製'+n,img:'https://via.placeholder.com/300?text='+n,cal:300,ings:[n],steps:['簡單料理']};
            recipes.unshift(nr); switchPage('recipe'); showStep(nr.id);
        }
        function quickGenerateRecipeDetail(){ quickGen(products.find(x=>x.id===curPid).name); }

        function renderRecs(l){ document.getElementById('grid-recipes').innerHTML=l.map(r=>`<div class="card" onclick="showStep('${r.id}')"><img src="${r.img}" class="card-img"><div class="card-body"><div class="card-title">${r.name}</div><div>[熱量]: ${r.cal}</div><button style="margin-top:10px;width:100%;padding:5px;" onclick="showStep('${r.id}')">[查看做法]</button></div></div>`).join(''); }
        function showStep(id){ const r=recipes.find(x=>x.id===id); document.getElementById('step-body').innerHTML=`<h4>[食材]</h4>${r.ings.join(', ')}<br><h4>[步驟]</h4><ol>${r.steps.map(s=>`<li>${s}</li>`).join('')}</ol>`; openModal('step'); }
        
        function openCreate(){ tempIngs=[]; document.getElementById('new-name').value=''; updPre(); openModal('create'); }
        function addIng(){ const v=document.getElementById('sel-ing').value; if(v&&!tempIngs.includes(v)){tempIngs.push(v);updPre();} }
        function addMan(){ const v=document.getElementById('man-ing').value; if(v){tempIngs.push(v);document.getElementById('man-ing').value='';updPre();} }
        function updPre(){ document.getElementById('ing-list').innerHTML=tempIngs.map((x,i)=>`<span class="ing-tag">${x} <b onclick="tempIngs.splice(${i},1);updPre()">X</b></span>`).join(''); }
        
        function aiGen(){
             if(tempIngs.includes('酪梨')&&tempIngs.includes('雞胸肉')){
                 document.getElementById('new-name').value='奶油酪梨雞胸肉佐蒜香地瓜葉';
                 alert('🥑 觸發隱藏食譜！');
             } else {
                 document.getElementById('new-name').value='AI特製'+(tempIngs[0]||'')+'料理';
             }
        }
        function pubRecipe(){
             const n=document.getElementById('new-name').value;
             if(n.includes('酪梨雞胸肉')){
                 const h=recipes.find(r=>r.id==='Hidden1');
                 recipes.unshift({...h,id:'U'+Date.now(),hidden:false});
             } else {
                 recipes.unshift({id:'C'+Date.now(),name:n,img:'https://via.placeholder.com/300',cal:500,ings:tempIngs,steps:['AI步驟']});
             }
             closeModal('create'); switchPage('recipe');
        }

        function toggleChat(){ const w=document.getElementById('chat-widget'); w.style.display=w.style.display==='flex'?'none':'flex'; }
        function sendChat(){ 
            const i=document.getElementById('chat-input'); const m=i.value; if(!m)return; 
            document.getElementById('chat-body').innerHTML+=`<div class="msg msg-user">${m}</div>`; i.value='';
            if(m==='[後台]'){ setTimeout(()=>{ toggleChat(); switchPage('backend'); renderAdmin(); },500); }
        }
        function renderAdmin(){ document.getElementById('admin-list').innerHTML=products.map(p=>`<tr><td>${p.name}</td><td>${p.cond}</td><td>${p.price}</td></tr>`).join(''); }

        function openModal(id){ document.getElementById('modal-'+id).style.display='flex'; }
        function closeModal(id){ document.getElementById('modal-'+id).style.display='none'; }

        window.onload=init;
    </script>
</body>
</html>
"""

final_html = html_template.replace("images/", BASE_URL)
components.html(final_html, height=1200, scrolling=True)
