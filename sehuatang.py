import requests
import bs4
from concurrent.futures import ThreadPoolExecutor
import threading
from rich.progress import track
import webbrowser
from datetime import datetime

from package.tools import make_html
import package.Synology_Web_API as Synology_Web_API
import package.config as config


class Article():
    def __init__(self) -> None:
        self.safe = False

class Sehuatang():
    def __init__(self) -> None:
        self.articleINFO = {}        

    def get_todayList(self, URL, todayIs: str = datetime.now().strftime("%Y-%m-%d")) -> list:
        res = requests.get(URL)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        tbodys = soup.find_all('tbody')

        todayList = []
        for progress, tbody in zip(track(tbodys, description="[\]正在抓取本日文章"), tbodys):
            try:
                date = tbody.find('span', attrs = {'title': todayIs})
                id = str(tbody.get('id'))
                if 'normalthread' not in id or date is None:
                    continue
                articleCode = id[-6:]
                todayList.append(articleCode)  # extract article_Code
                tag = tbody.find('em').get_text()
                title = tbody.find('a', attrs = {'class': 's xst'}).get_text()

                self.articleINFO[articleCode] = Article()
                article = self.articleINFO[articleCode]
                article.link = f'https://sehuatang.org/thread-{articleCode}-1-1.html'
                article.title = title
                article.tag = tag

                # print(f"{tag} -> {title}")
            except TypeError:
                pass    

        return todayList

    def get_Magnet_and_Pics(self, articleCode: str) -> None:
        global progress_done
        progress_done = False
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + articleCode + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text, "html.parser")

        # Get Magnet
        magnet = bs_pages.find("div", "blockcode").get_text()
        self.articleINFO[articleCode].magnet = magnet.removesuffix("复制代码")

        # Get Pics
        img_block = bs_pages.find_all("ignore_js_op")

        picsList = []
        picsList.append("Head of Page")
        for block in img_block[:-1]:
            pic_link = block.find("img").get("file")
            if pic_link != None:
                picsList.append(pic_link)                    
        picsList.append("end of page")

        self.articleINFO[articleCode].imgLinks = picsList
        progress_done = True

def task_progress_bar():
    for progress in zip(track(todays, description=f"[\]正在分析文章資料"), todays):
        while not progress_done:
            pass

def task_articleParser():
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(currentFourm.get_Magnet_and_Pics, todays)

def start(scrabDate: str):
    global currentFourm, todays
    currentFourm = Sehuatang()
    typeList = ("無碼", "有碼", "國產", "歐美", "中文")
    magnetSelected = []
    URL_library = {
        1: 'https://www.sehuatang.org/forum-36-1.html',
        2: 'https://www.sehuatang.org/forum-37-1.html',
        3: 'https://www.sehuatang.org/forum-2-1.html',
        4: 'https://www.sehuatang.org/forum-38-1.html',
        5: 'https://www.sehuatang.org/forum-103-1.html'
    }

    fourmIdx = chooseFourm()
    todays = currentFourm.get_todayList(URL_library[fourmIdx], todayIs=scrabDate)

    task_pgbar = threading.Thread(target=task_progress_bar)
    task_pgbar.start()
    task_article = threading.Thread(target=task_articleParser)
    task_article.start()
    
    task_article.join()
    task_pgbar.join()

    if todays:
        print(f"[!]共 {len(todays)} 篇文章")    
        fileName =  "AVMC-Viewer-SHT-" + typeList[fourmIdx] + ".html"
        make_html(currentFourm.articleINFO.values(), fileName)
        webbrowser.open_new_tab(fileName)

        magnetSelected = select_article(workFourm = currentFourm)

        syno_info = config.load_config(mode = 'Synology')
    else:
        print(f"[!]日期: {scrabDate} 尚未有文章更新 ! ")
        return

    if magnetSelected:
        # Synology Web API
        if syno_info["upload"]:
            print("[*]" + "Synology Web API".center(50, "="))
            ds = Synology_Web_API.SynologyDownloadStation(
                ip=syno_info["IP"], port=syno_info["PORT"], secure=syno_info["SECURE"]
            )
            ds.login(syno_info["USER"], syno_info["PASSWORD"])
            for magnet_to_download in magnetSelected:
                ds.uploadTorrent(magnet_to_download, syno_info["PATH"])
            print("[*]" + "Synology Web API 作業完成".center(50, "="))
    else:
        print("[*]未選取任何文章 ! ")


def chooseFourm() -> int:
    typeList = ("無碼", "有碼", "國產", "歐美", "中文")
    print('[*]===============================================') 
    print("[*]                 1. 無碼")
    print("[*]                 2. 有碼")
    print("[*]                 3. 國產")
    print("[*]                 4. 歐美")
    print("[*]                 5. 中文")
    print('[*]===============================================') 
    while True:     
        typeChoose = int(input(f"[?]請選擇分區(1~5):"))
        if typeChoose >= 1 and typeChoose <= 5:
            print(f'[*]選擇的是 {typeChoose}. {typeList[typeChoose-1]} 分區')
            print('[*]===============================================') 
            return typeChoose

def select_article(workFourm: Sehuatang) -> list:
    titleList = [workFourm.articleINFO[articleCode].title for articleCode in todays]
    magList = [workFourm.articleINFO[articleCode].magnet  for articleCode in todays]
    magnetSelected = []

    avList = {}

    for idx in range(1, len(titleList)+1):
        avList[idx] = [
            titleList[idx-1],
            magList[idx-1]
        ]
        # ex: 123: ['MIAD-891 時間が止まる女子便所 無意識に失禁するオンナ達', 'magnet:?xt=urn:btih:235F0BE6E769D13D1F59F335AD26A9C1C6C9ADDC'] ... and so on

    idx = 1
    while idx < len(titleList)+1:
        print("[*]" + '*'*50)
        print("[*]目前選擇的是:")
        action = input(f"[>]{idx}. {avList[idx][0]}: ")
        if action == '-1' and idx == 1:
            print("[!]目前還不能取消操作 ! ")
            continue
                
        if action == '-1':
            idx -= 1
            continue
        elif action == '':
            print('[*]不要這部 ! ')
        else:
            print(f'[>]已選擇 {avList[idx][0]} 之 magnet: {avList[idx][1]}')
            if avList[idx][1]:
                print("[!]這部已經選取過了喔~ 已在清單內")
            else:
                magnetSelected.append(avList[idx][1])
        idx += 1

    return magnetSelected

# start()