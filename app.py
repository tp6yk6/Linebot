import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('xWn8wQ5cjAnjfzSBfvNeWkBEAnG3yb95oZnvdiWCqaT4Hplw38RAZ7ira/Z5wdNfSt38KK4fI6IWXrYxCmDMvXenFYAdeUKGo2eGYcbcmIzM+dYR5nsuE4GIAI6wVKbXcTT/CfsMrSyHy85xcPk1zAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('35ab26821b514d995af50e30efb34ccf')

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
def function(text):
    list=['飯','麵','肉']
    if text=='hi' or text=='Hi':
        text='hello'
    elif text=='餓':
        text=random.choice(list)
    else:
        text='安安'
    return text

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(function(event.message.text))
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

