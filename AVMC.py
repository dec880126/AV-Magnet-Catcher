import sys
import os
import time

from package.tools import clearConsole, changeDate
from package.config import check_config_if_exist, load_config, make_config
from t66y import start as t66y_start
from sehuatang import start as sht_start

info = {
    "author": "CyuanHunag",
    "version": "2.0.0-dev",
    "email": "dec880126@icloud.com",
    "official_site": "https://github.com/dec880126/AV-Magnet-Catcher",
}
today = str(time.strftime("%Y-%m-%d", time.localtime()))

class Endding(Exception):
    def __init__(self):
        sys.exit()


def AVMC_function(functionChoose):
    """
    功能清單
    type functionChoose: str
    """
    
    method = functionDefined.get(functionChoose, print("請重新選擇功能"))

    return method()

def exit_AVMC():
    """
    刪除 HTML files 並關閉程式
    """
    # TODO
    # remove_html_if_exist()
    input("[*]按一下鍵盤上的「Enter」來結束程式...")
    raise Endding

def choose_fourmMode():
    global today
    while True:
        clearConsole()
        print("[*]================== 選擇論壇 ==================")
        print("[*]目前支援之論壇有: ")
        print("[*]\t1. 色花堂 (sehuatang.org)")
        print("[*]\t2. 草榴社區 (t66y.com)")
        print("[*]=============================================")
        fourmChoose = input("[?]請輸入選擇的論壇之編號: ")
        
        if fourmChoose not in ("1", "2"):
            input("[!]警告: 請輸入正確的論壇編號! \n[*]請按一下鍵盤上的「Enter」以繼續...")
            continue
        break

    if fourmChoose == "1":
        sht_start(scrabDate = today)
    elif fourmChoose == "2":
        t66y_start(scrabDate = today)

    input("[*]請按一下鍵盤上的「Enter」以回到主畫面...")

def edit_date():
    """
    rtype: str <- today's info
    """
    global today
    today = changeDate(today)

functionDefined = {
    "1": choose_fourmMode,
    "2": edit_date,
    "EXIT": exit_AVMC
}

if __name__ == "__main__":
    #  Load config
    if check_config_if_exist("config.ini"):
        pass
    else:
        print("[!]若為初次運行 AVMC ，請先至檔案目錄下配置 config.ini")
        make_config("./config.ini")
        os.system("pause")
        sys.exit()

    while True:
        print("[*]==================== AVMC =====================")
        print("[*]" + info["version"].center(46))
        print("[*]")
        print("[*]" + "↓ Official Site ↓".center(46))
        print("[*]" + info["official_site"].center(46))
        print("[*]===============================================")
        print("[*]               1. 開始抓取")
        print("[*]               2. 日期設定")
        print("[*]               EXIT. 結束程式")
        print("[*]          隨時可按 Ctrl + C 回到此頁面")
        print("[*]===============================================")
        functionChoose = input(f"[?]請選擇功能(1~{len(functionDefined)-1}):")

        functionChoose = 'EXIT' if functionChoose == 'exit' else functionChoose

        # 檢查 functionChoose 是否在功能清單中 否則重複選擇直到成功
        if functionChoose not in functionDefined:
            print("[*]===============================================")
            print("[?]請重新輸入功能選單中之數字(1~5)...")
            os.system("pause")
            continue

        try:
            # 根據所選擇之功能開始作業
            AVMC_function(functionChoose)
        except Endding:
            print("\n程式結束...")
        except KeyboardInterrupt:
            # """
            # 輸入 Ctrl + C 的狀況
            # """
            print("\n[*]===============================================")
            print("[!]已偵測到強制中斷...將回到主選單...")
        except ValueError:
            print("\n[*]===============================================")
            print("[!]ValueError")
            print("[!]將回到主選單...")
        finally:
            # 結束每階段任務後清除 Console
            clearConsole()
