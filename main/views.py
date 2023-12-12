from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                message = event.message.text
                print(message)
                if message == "你好":
                    replay_message = "您好!請輸入欲查詢之幣別"
                # elif message=='美金':
                #     reply_message=get_rate()

                else:
                    replay_message = "請重新輸入"

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=replay_message),
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# 寫函式區
# def get_rate():
