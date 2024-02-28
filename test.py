from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from flask import Flask, request, abort

#from linebot import (
#    LineBotApi, WebhookHandler
#)
#from linebot.exceptions import (
#    InvalidSignatureError
#)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('GBdQf63ap1BVc6Q2aG7Q7XyubnHJmcYUCsKfe2RXELDCDPhCPzvGas+8ACkGhmGNN8nYAniL/vr6k4gqhi5sVR2dX/BIf88Wa3T2NcDPg5M1t5JoU5+O1nJ3SaeBefnsyQfaL23lnqetPDQd0AoJGAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('68552136aebf1905f0eb97bb37d0a5d0')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
