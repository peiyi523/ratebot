import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 查價
chrome = ""


def get_middle_rate():
    datas = []

    try:
        global chrome
        chrome = webdriver.Chrome(service=Service(r"C:\webdriver\chromedriver.exe"))
        chrome.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")
        chrome.maximize_window()
        time.sleep(1)
        chrome.find_element(
            by=By.XPATH, value="/html/body/div[1]/main/div[4]/div/p[1]/a[1]"
        ).click()
        time.sleep(1)
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
                # 把字串轉成浮點數
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
                result_data = {
                    info["幣別"].strip(): {
                        "即期買入": info["即期買入"],
                        "即期賣出": info["即期賣出"],
                        "目前中價": info["目前中價"],
                    }
                    for _, info in result_data.items()
                }

                input_key = "美金"
                temp_str = ""
                if input_key in result_data:
                    for key in result_data[input_key]:
                        temp_str += f"\n{key}:{result_data[input_key][key]}"
                    message = f"{input_key}{temp_str}"
                else:
                    message = "輸入錯誤!"

    except Exception as e:
        print(e)

    return message


if __name__ == "__main__":
    result = get_middle_rate()
    print(result)
