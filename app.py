import random
import string
import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('c2evFAGICqUJHssSolgeTP1c+FJOC/up+zxqSBnuTMgcxiC6LS5NGqivDdS+T+jv85045Z2udt+OD9H/Y1CG8TpR3s257zNIO7kZofSvMCeyt/sRe8BBhg2FlQTmSKrQxUeIlVEUI+PLrh/Ctt8qqAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bfb7c602056292ca553e3455b3b91a07')

@app.route("/callback", methods=['POST'])
def callback():
    # 处理 LINE 的 Webhook 请求
    # ...
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def callback(event):
    message_text = event.message.text
    reply_text = "你發送的消息是：" + message_text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

@handler.add(MessageEvent, message=[ImageMessage])
def callback(event):
    image_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + '.jpg'
    image_content = line_bot_api.get_message_content(event.message.id)
    path = os.path.join(static_tmp_path, image_name)

    with open(path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)

    reply_text = '圖片已保存為 ' + image_name
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)