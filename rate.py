import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 查價
chrome = ""
result_data = None


def get_middle_rate(path=r"C:\webdriver\chromedriver.exe", hide=True):
    datas = []

    try:
        global chrome
        options = webdriver.ChromeOptions()
        service = Service(executable_path=path)
        if hide:
            options.add_argument("--headless")
        chrome = webdriver.Chrome(service=service, options=options)
        chrome.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")
        chrome.maximize_window()  # 把網頁擴展到最大
        time.sleep(0.5)
        chrome.find_element(
            by=By.XPATH, value="/html/body/div[1]/main/div[4]/div/p[1]/a[1]"
        ).click()
        # time.sleep(0.5)
        soup = BeautifulSoup(chrome.page_source, "lxml")
        for tr in soup.find("tbody").find_all("tr"):
            data = []
            for i, td in enumerate(tr.find_all("td")[:5]):
                if i == 0:
                    data.append(
                        td.find(
                            "div", class_="hidden-phone print_show xrt-cur-indent"
                        ).text.strip()
                    )
                else:
                    data.append(td.text.strip())
            if data != []:
                datas.append([data[0], data[3], data[4]])
                datas = [[0 if value == "-" else value for value in i] for i in datas]
                # 把字串轉成浮點數計算中價
                datas = [
                    [
                        float(x)
                        if isinstance(x, str) and x.replace(".", "", 1).isdigit()
                        else x
                        for x in row
                    ]
                    for row in datas
                ]
                # 計算每個幣別的平均值
                averages = [round((row[1] + row[2]) / 2, 5) for row in datas]
                # 將平均值附加在各自的第三個位置
                result_data = [row + [avg] for row, avg in zip(datas, averages)]

                result_data = pd.DataFrame(
                    result_data, columns=["幣別", "即期買入", "即期賣出", "目前中價"]
                )
                # str.extract(r'(.*)\s\((.*)\)') 使用正則表達式，(.*) 代表匹配任意字符，\s 代表空格，\((.*)\)代表匹配括號內的任意字和符號。
                result_data[["幣別", "代碼"]] = result_data["幣別"].str.extract(
                    r"(.*)\s\((.*)\)"
                )
                result_data = result_data.drop(columns=["代碼"])
                result_data = result_data.to_dict("index")
                # 轉成字典之後原本是長這樣result_data={0: {'幣別': '美金', '即期買入': 31.155, '即期賣出': 31.255, '目前中價': 31.205},...}
                # 下面法法是為了把最前面的編號去掉
                result_data = {
                    info["幣別"].strip(): {
                        "即期買入": info["即期買入"],
                        "即期賣出": info["即期賣出"],
                        "目前中價": info["目前中價"],
                    }
                    for _, info in result_data.items()  # "_"表示只要值(info)本身的資料，不需要鍵(_)的資料
                }
    except Exception as e:
        print(e)
    return result_data


def get_currency_info(currency_code):
    global result_data
    message = "?"
    try:
        if currency_code in result_data:
            currency_info = result_data[currency_code]
            message = f"{currency_code} 報價如下:\n"
            for key, value in currency_info.items():
                message += f"{key}: {value}\n"
        # 另一種寫法
        # if currency_code in result_data:
        #     temp_str = ""
        #     for key in result_data[currency_code]:
        #         temp_str += f"\n{key}:{result_data[currency_code][key]}"
        #     message = f"{currency_code}\n報價如下:{temp_str}"

        else:
            message = f"輸入錯誤!請重新輸入!"

    except Exception as e:
        print(e)
        message = str(e)
    return message


if __name__ == "__main__":
    result_data = get_middle_rate()
    # print(result_data)
    print(get_currency_info("歐元"))
