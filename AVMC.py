import sys
import os

from package.tools import clearConsole

info = {
    "author": "CyuanHunag",
    "version": "1.0.0",
    "email": "dec880126@icloud.com",
    "official_site": "https://github.com/dec880126/AV-Magnet-Catcher",
}

class Endding(Exception):
    def __init__(self):
        sys.exit()


def Auto_sht_function(functionChoose):
    """
    功能清單
    type functionChoose: str
    """
    
    method = functionDefined.get(functionChoose, print("請重新選擇功能"))

    return method()

def exit_Auto_sht():
    """
    刪除 HTML files 並關閉程式
    """
    # TODO
    # remove_html_if_exist()
    input("[*]按一下鍵盤上的「Enter」來結束程式...")
    raise Endding

def choose_fourmMode():
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
        print("sehuatang")
    elif fourmChoose == "2":
        print("t66y.com")

    input("[*]請按一下鍵盤上的「Enter」以回到主畫面...")

functionDefined = {
    "1": choose_fourmMode,
    "EXIT": exit_Auto_sht,
}




if __name__ == "__main__":
    while True:
        print("[*]==================== AVMC =====================")
        print("[*]" + info["version"].center(46))
        print("[*]")
        print("[*]" + "↓ Official Site ↓".center(46))
        print("[*]" + info["official_site"].center(46))
        print("[*]===============================================")
        print("[*]               1. 開始抓取")
        print("[*]               2. 修改日期")
        print("[*]               3. 資料查詢")
        print("[*]               4. 重製資料")
        print("[*]               EXIT. 結束程式")
        print("[*]          隨時可按 Ctrl + C 回到此頁面")
        print("[*]===============================================")
        functionChoose = input(f"[?]請選擇功能(1~{len(functionDefined)-1}):")

        if functionChoose == "exit":
            functionChoose = "EXIT"

        # 檢查 functionChoose 是否在功能清單中 否則重複選擇直到成功
        if functionChoose not in functionDefined:
            print("[*]===============================================")
            print("[?]請重新輸入功能選單中之數字(1~5)...")
            os.system("pause")
            continue

        try:
            # 根據所選擇之功能開始作業
            Auto_sht_function(functionChoose)
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