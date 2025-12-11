const express = require('express');
const line = require('@line/bot-sdk');

// 設定參數
const config = {
  channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.CHANNEL_SECRET,
};

const client = new line.Client(config);
const app = express();

// 您的網站連結
const MY_WEBSITE_URL = 'https://cycubigdata.zeabur.app'; 

// === 機器人劇本庫 (完全無表情符號版) ===
const botRules = [
  // 1. 歡迎與引導
  { 
    keywords: ['你好', '哈囉', 'hi', '開始', '功能'], 
    response: "您好，歡迎來到食際行動家。我是您的惜食小幫手。\n\n您可以輸入以下指令：\n「逛超市」：進入線上商城\n「食譜」：查詢料理靈感\n「營業時間」：查看服務資訊" 
  },
  
  // 2. 購物與連結
  { 
    keywords: ['逛超市', '買', '下單', '商品', '連結'], 
    response: `沒問題，今日架上有許多新鮮貨。\n\n請點擊下方連結進入線上超市：\n${MY_WEBSITE_URL}` 
  },
  { 
    keywords: ['優惠', '特價', '折扣'], 
    response: `今日特價中。目前蘋果和地瓜正在做折扣，雖然外表有些許瑕疵，但甜度很高。\n\n請前往搶購：\n${MY_WEBSITE_URL}` 
  },
  { 
    keywords: ['即期品', '壞掉'], 
    response: "請放心，即期品是指接近最佳賞味期但尚未變質的良品，營養價值不變，價格更優惠。" 
  },

  // 3. 配送與資訊
  { 
    keywords: ['營業時間', '幾點開'], 
    response: "我們網站 24小時 皆可下單。真人客服時間為：週一至週日 09:00 - 18:00。" 
  },
  { 
    keywords: ['地址', '店面'], 
    response: "我們目前以線上配送為主，倉庫位於：台北市信義區快樂路 123 號。" 
  },
  { 
    keywords: ['運費', '免運'], 
    response: "配送規則：全館滿 500 元免運費，未滿酌收 80 元運費。" 
  },
  { 
    keywords: ['電話', '客服', '真人'], 
    response: "客服專線：02-1234-5678\n或者您可以直接留言，店長看到會盡快回覆您。" 
  },

  // 4. 食譜推薦
  { 
    keywords: ['食譜', '煮什麼', '推薦'], 
    response: "今晚想吃點什麼？\n您可以輸入食材名稱，例如：「地瓜」、「蘋果」、「高麗菜」，我將提供料理建議。" 
  },
  { 
    keywords: ['地瓜'], 
    response: "地瓜推薦做法：\n1. 蜂蜜烤地瓜：氣炸 200度 30分鐘，淋上蜂蜜。\n2. 地瓜稀飯：古早味早餐首選。" 
  },
  { 
    keywords: ['蘋果'], 
    response: "蘋果推薦吃法：\n1. 蘋果優格沙拉：清爽低卡。\n2. 蘋果咖哩：加入咖哩燉煮更溫潤。" 
  },
  { 
    keywords: ['香蕉'], 
    response: "香蕉推薦：\n1. 香蕉牛奶：早餐飲品。\n2. 香蕉煎餅：適合當下午茶點心。" 
  },
  { 
    keywords: ['高麗菜'], 
    response: "高麗菜推薦：\n1. 培根炒高麗菜：油香下飯。\n2. 大阪燒：切絲做成日式煎餅。" 
  }
];

// LINE Webhook 入口
app.post('/callback', line.middleware(config), (req, res) => {
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result) => res.json(result))
    .catch((err) => {
      console.error(err);
      res.status(500).end();
    });
});

// 處理訊息的核心邏輯
function handleEvent(event) {
  if (event.type !== 'message' || event.message.type !== 'text') {
    return Promise.resolve(null);
  }

  const userMsg = event.message.text.toLowerCase();
  let replyText = "抱歉，我不太懂您的意思。\n您可以試試輸入：「逛超市」、「營業時間」或「食譜」。";

  // 搜尋符合的規則
  const match = botRules.find(rule => 
    rule.keywords.some(keyword => userMsg.includes(keyword))
  );

  if (match) {
    replyText = match.response;
  }

  // 強制移除所有可能殘留的表情符號 (以防萬一)
  replyText = replyText.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');

  return client.replyMessage(event.replyToken, {
    type: 'text',
    text: replyText
  });
}

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`LINE Bot server running on port ${port}`);
});
