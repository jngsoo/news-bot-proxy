from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
# For read ENV variables in .env file
import environ
environ.Env.read_env()
env = environ.Env(
    DEBUG=(bool, False)
)


app = Flask(__name__)

line_bot_api = LineBotApi(env('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(env('CHANNEL_SECRET'))


@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    client = request.headers['X-Line-Request-Id']
    line_bot_api.push_message(client, TextSendMessage(text='Hello World!'))

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.route("/", methods=['GET'])
def index():
    return str(len(env('CHANNEL_ACCESS_TOKEN')))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port='443')