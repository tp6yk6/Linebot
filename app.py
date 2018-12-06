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



def keyword(text):
    KeyWordDict = {"你好":"你也好啊"}
    for k in KeyWordDict.keys():
        if text.find(k)!=-1:
            return[True,KeyWordDict[k]]
    return[False]
def Reply(event):
    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = Ktemp[1]))

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text))

def Button(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='來算術吧',
            text='1+1=?',
            actions=[
                PostbackTemplateAction(
                    label='4',
                    text='4',
                    data=''
                ),
                PostbackTemplateAction(
                    label='2',
                    text='2',
                    data=''
                ),
                PostbackTemplateAction(
                    label='3',
                    text='3',
                    data=''
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Button(event)
        #Reply(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(e)))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

