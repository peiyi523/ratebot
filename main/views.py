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
                    replay_message = (
                        "請輸入查詢項目編號(例:輸入1代表查詢美金):\n"
                        + "0.新聞、1.美金、2.港幣\n3.英鎊、4.澳幣、5.加拿大幣\n6.新加坡幣、7.瑞士法郎、8.日圓\n9.南非幣、10.瑞典幣、11.紐元\n12.泰幣、13.菲國比索、14.印尼幣\n15.歐元、16.韓元、17.越南盾\n18.馬來幣、19.人民幣、20.臺銀牌告匯率網站"
                    )
                    message_object = TextSendMessage(text=replay_message)

                elif message in result_data:
                    currency_info = result_data[message]
                    replay_message = f"目前參考報價如下:\n幣別: {currency_info['幣別']}\n即期買入: {currency_info['即期買入']}\n即期賣出: {currency_info['即期賣出']}\n目前中價: {currency_info['目前中價']}\n\n*資料來源:臺灣銀行>牌告匯率\n*本資料僅供參考，實際交易匯率以臺灣銀行牌價最新掛牌時間為準"
                    message_object = TextSendMessage(text=replay_message)

                #    這樣寫也可以
                # elif message in result_data:
                #     temp_str = ""
                #     for key in result_data[message]:
                #         temp_str += f"\n{key}:{result_data[message][key]}"
                #         replay_message = f"{message}\n報價如下:{temp_str}"
                #         message_object = TextSendMessage(text=replay_message)
                elif message == "0":
                    replay_message = (
                        "鉅亨網\n"
                        + "https://news.cnyes.com/news/cat/forex \n"
                        + "經濟日報\n"
                        + "https://money.udn.com/search/tagging/1001/%E5%8C%AF%E5%B8%82"
                    )
                    message_object = TextSendMessage(text=replay_message)
                elif message == "20":
                    replay_message = (
                        "臺灣銀行網站牌告匯率查詢\n" + "https://rate.bot.com.tw/xrt?Lang=zh-TW\n"
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
