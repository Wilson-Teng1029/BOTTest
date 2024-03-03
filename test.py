
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from flask import Flask, request, abort

from urllib.parse import quote as url_quote
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('iXJBod96rwgnlN5LxreVqy1aIPnMJYgcEMh7Tw3T9+P8f7uvhnjtgcoCcPT+lkPjk1j+KNvvjqONXD2d1eW+MjjkWFogA0FfP4pF3dXG8RekQPzVLhiJveAxnt9yM+JRE1BU6ykdg9gS7PWEHfQAbgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7e9447f9ba4b1177f70c5d8b61bb71ec')

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
    reply_text = '嗨 我在學你講話話喔~' + event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

import os
if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run()
