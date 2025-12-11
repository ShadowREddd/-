const express = require('express');
const line = require('@line/bot-sdk');

const config = {
  channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.CHANNEL_SECRET,
};

const client = new line.Client(config);
const app = express();

// Webhook 入口
app.post('/callback', line.middleware(config), (req, res) => {
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result) => res.json(result))
    .catch((err) => {
      console.error(err);
      res.status(500).end();
    });
});

// 事件處理邏輯
function handleEvent(event) {
  if (event.type !== 'message' || event.message.type !== 'text') {
    return Promise.resolve(null);
  }

  const userMsg = event.message.text;
  let replyText = '';

  // --- 機器人回應邏輯 ---
  
  if (userMsg.includes('超市') || userMsg.includes('買') || userMsg.includes('逛')) {
      // 當使用者想買東西，回傳您的 Streamlit 連結
      return client.replyMessage(event.replyToken, {
          type: 'text',
          text: '歡迎光臨食際行動家！\n點擊下方連結開始選購：\n\nhttps://h72tshhkoqxip2jprjlb3q.streamlit.app'
      });
  } 
  else if (userMsg.includes('營業時間')) {
      replyText = '我們 24 小時全天候為您服務！';
  }
  else if (userMsg.includes('地址')) {
      replyText = '我們位於雲端之上，隨時隨地都能送達！';
  }
  else {
      replyText = '您好！您可以輸入「超市」來逛逛我們的商店，或是詢問「營業時間」。';
  }
replyText = replyText.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');
  // 回傳文字訊息
  return client.replyMessage(event.replyToken, {
    type: 'text',
    text: replyText
  });
}

// 啟動伺服器
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`listening on ${port}`);

});

