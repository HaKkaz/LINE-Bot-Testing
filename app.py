# import os
# from dotenv import load_dotenv
# load_dotenv()
# LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
# LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = 'qO/9KWNS7EcQnI/CLYo6FeaouIA/4+5QcYDjwrm8Oxi5nwtyGXLXRQqsd5cRq4xHqLOWCe5UjrNmJqsjNAUQUOo43LrIg3a2Aew3Azp89pNCB2T3/z2o2wrexO6PSutaUQaFd1TmEt16qvML5rYfPQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'e0d5a3480a25f89749f6097f94b4a135'

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

configuration = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    if request.headers.get('X-Line-Signature') is None:
        abort(404)
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info( ReplyMessageRequest( reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8787)