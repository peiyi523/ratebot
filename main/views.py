from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from rate import get_middle_rate

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
                message_object = None
                # print(message)
                if message == "你好":
                    replay_message = "您好!請輸入欲查詢之幣別:例如美金、港幣、英鎊...等"
                    message_object = TextSendMessage(text=replay_message)

                elif message == "美金":
                    reply_message = result
                    message_object = TextSendMessage(text=replay_message)

                else:
                    message_object = TextSendMessage(text="請重新輸入!")

                line_bot_api.reply_message(
                    event.reply_token,
                    message_object,
                    # TextSendMessage(text=replay_message),
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
