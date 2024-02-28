
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from flask import Flask, request, abort

from urllib.parse import quote as url_quote
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('GBdQf63ap1BVc6Q2aG7Q7XyubnHJmcYUCsKfe2RXELDCDPhCPzvGas+8ACkGhmGNN8nYAniL/vr6k4gqhi5sVR2dX/BIf88Wa3T2NcDPg5M1t5JoU5+O1nJ3SaeBefnsyQfaL23lnqetPDQd0AoJGAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('68552136aebf1905f0eb97bb37d0a5d0')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
    if event.source.userId != "U0125668ecfcfd02241e1a305c47ab5a8":
        
        reply_text = '嗨 我在學你講話話喔~' + event.message.text

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
