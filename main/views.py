from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot.models import FlexSendMessage


# Create your views here.
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from rate import get_middle_rate

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)
# result_data = None


@csrf_exempt
def callback(request):
    global result_data
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
                # if result_data == None:
                result_data = get_middle_rate()
                message_object = None
                if message == "報價":
                    replay_message = "您好!\n" + "請輸入欲查詢之幣別:\n" + "美金、港幣、日圓、人民幣...等"
                    message_object = TextSendMessage(text=replay_message)

                elif message in result_data:
                    currency_info = result_data[message]
                    replay_message = f"{message}\n報價如下:\n即期買入: {currency_info['即期買入']}\n即期賣出: {currency_info['即期賣出']}\n目前中價: {currency_info['目前中價']}"
                    message_object = TextSendMessage(text=replay_message)

                #    這樣寫也可以
                # elif message in result_data:
                #     temp_str = ""
                #     for key in result_data[message]:
                #         temp_str += f"\n{key}:{result_data[message][key]}"
                #         replay_message = f"{message}\n報價如下:{temp_str}"
                #         message_object = TextSendMessage(text=replay_message)
                elif message == "新聞":
                    replay_message = (
                        "鉅亨網\n"
                        + "https://news.cnyes.com/news/cat/forex \n"
                        + "經濟日報\n"
                        + "https://money.udn.com/search/tagging/1001/%E5%8C%AF%E5%B8%82"
                    )
                    message_object = TextSendMessage(text=replay_message)

                else:
                    message_object = TextSendMessage(text="請重新輸入!")

                line_bot_api.reply_message(
                    event.reply_token,
                    message_object,
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<h1>現在時刻:{now}</h1>")
