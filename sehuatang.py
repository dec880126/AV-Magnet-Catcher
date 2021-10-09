from datetime import datetime
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor
import requests
import bs4
import threading
import webbrowser
import time

from package.tools import changeDate, is_shirouto, make_html, get_proxy_in_multi_threading
import package.Synology_Web_API as Synology_Web_API
import package.config as config

class Article():
    def __init__(self) -> None:
        self.title = ""
        self.tag = ""
        self.link = ""
        self.magnet = ""
        self.imgLinks = []

class Sehuatang():
    def __init__(self, auto_proxy: bool = False) -> None:
        self.articleINFO = {}
        self.auto_proxy = auto_proxy
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
        }

    def get_todayList(self, URL: str, todayIs: str = datetime.now().strftime("%Y-%m-%d")) -> list:
        todayList = []
        temp = range(30)
        pageNum = URL[-6]
        urlBase = URL[:-6]

        while len(temp) == 30:
            temp = []

            response = requests.get(URL, headers=self.header)
            s = bs4.BeautifulSoup(response.text, 'html.parser')
            tbodys = s.find_all('tbody')

            for progress, tbody in zip(track(tbodys, description=f"[\]正在抓取第{pageNum}頁"), tbodys):
                try:
                    date = tbody.find('span', attrs = {'title': todayIs})
                    id = str(tbody.get('id'))
                    if 'normalthread' not in id or date is None:
                        continue

                    shtConfig =  config.load_config(mode = "Sehuatang")
                    tag = tbody.find('em').get_text().replace('[', '').replace(']', '')
                    if shtConfig['exclude'] in tag:
                        continue

                    title = tbody.find('a', attrs = {'class': 's xst'}).get_text()
                    articleCode = id[-6:]
                    temp.append(articleCode)  # extract article_Code
                    self.articleINFO[articleCode] = Article()

                    if is_shirouto(title):
                        self.articleINFO[articleCode].title = title
                        self.articleINFO[articleCode].tag = '素人已排除'
                    else:
                        self.articleINFO[articleCode].link = f'https://sehuatang.org/thread-{articleCode}-1-1.html'
                        self.articleINFO[articleCode].title = title
                        self.articleINFO[articleCode].tag = tag
                except TypeError:
                    pass
            todayList.extend(temp)

            if len(temp) == 30:
                pageNum = str(int(pageNum) + 1)
                URL = urlBase + pageNum + '.html'

        return todayList

    def get_Magnet_and_Pics(self, articleCode: str) -> None:
        global progress_done
        if self.articleINFO[articleCode].tag == '素人已排除':
            print(f"[>]{self.articleINFO[articleCode].title}: 素人已排除")
            progress_done = True
            return
        if self.auto_proxy:
            while True:
                try:
                    time.sleep(0.5)
                    response_of_pages = requests.get("https://www.sehuatang.org/thread-" + articleCode + "-1-1.html", timeout = 3, proxies=self.proxy, headers=self.header)
                    break
                except requests.exceptions.RequestException:
                    next_idx = self.validProxys.index(self.proxy) + 1

                    if next_idx == len(self.validProxys):
                        self.proxy_setting()
                    else:
                        self.proxy = self.validProxys[next_idx]
        else:
            response_of_pages = requests.get("https://www.sehuatang.org/thread-" + articleCode + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text, "html.parser")

        # Get Magnet
        magnet = bs_pages.find("div", "blockcode").get_text().removesuffix("复制代码")
        self.articleINFO[articleCode].magnet = magnet

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
        print(f"[>]{self.articleINFO[articleCode].title}: 完成")
        progress_done = True

    def proxy_setting(self):
        self.validProxys = get_proxy_in_multi_threading()       

        self.proxy = {
            'http':"http://" + self.validProxys[0],
            'https':"http://" + self.validProxys[0]
        }


def task_progress_bar():
    global progress_done, currentFourm

    for progress in zip(track(todays, description=f"[*]目前使用之代理為: {currentFourm.proxy['https']}\n[\]正在分析文章資料"), todays):
        progress_done = False
        while not progress_done:
            pass


def task_articleParser():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(currentFourm.get_Magnet_and_Pics, todays)
    global progress_done
    progress_done = True


def start(scrabDate: str, auto_proxy: bool = True):
    global currentFourm, todays
    currentFourm = Sehuatang()
    typeList = ("無碼", "有碼", "國產", "歐美", "4K", "中文")
    magnetSelected = []
    URL_library = {
        1: 'https://www.sehuatang.org/forum-36-1.html',
        2: 'https://www.sehuatang.org/forum-37-1.html',
        3: 'https://www.sehuatang.org/forum-2-1.html',
        4: 'https://www.sehuatang.org/forum-38-1.html',
        5: 'https://www.sehuatang.org/forum-151-1.html',
        6: 'https://www.sehuatang.org/forum-103-1.html'
    }

    fourmIdx = chooseFourm()
    todays = currentFourm.get_todayList(URL_library[fourmIdx], todayIs=scrabDate)    

    if auto_proxy:
        currentFourm.proxy_setting()
        print(f"[*]已開啟自動代理模式: {currentFourm.proxy}")

    task_pgbar = threading.Thread(target=task_progress_bar)
    task_pgbar.start()
    task_article = threading.Thread(target=task_articleParser)
    task_article.start()
    
    task_pgbar.join()
    task_article.join()

    if todays:
        fileName =  "AVMC-Viewer-SHT-" + typeList[fourmIdx - 1] + ".html"
        make_html(currentFourm.articleINFO.values(), fileName)
        webbrowser.open_new_tab(fileName)

        magnetSelected = select_article(workFourm = currentFourm)

        syno_info = config.load_config(mode = 'Synology')
    else:
        print(f"[!]日期: {scrabDate} 無文章更新 ! ")
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
            for idx, magnet in enumerate(magnetSelected):
                print(f"[>] {idx + 1}. {magnet}")
    else:
        print("[*]未選取任何文章 ! ")


def chooseFourm() -> int:
    typeList = ("無碼", "有碼", "國產", "歐美", "4K", "中文")
    print('[*]===============================================') 
    print("[*]                 1. 無碼")
    print("[*]                 2. 有碼")
    print("[*]                 3. 國產")
    print("[*]                 4. 歐美")
    print("[*]                 5. 4K")
    print("[*]                 6. 中文")
    print('[*]===============================================') 
    while True:     
        typeChoose = int(input(f"[?]請選擇分區(1~{len(typeList)}):"))
        if typeChoose >= 1 and typeChoose <= len(typeList):
            print(f'[*]選擇的是 {typeChoose}. {typeList[typeChoose-1]} 分區')
            print('[*]===============================================') 
            return typeChoose

def select_article(workFourm: Sehuatang) -> list:
    titleList = [workFourm.articleINFO[articleCode].title for articleCode in todays if workFourm.articleINFO[articleCode].tag != '素人已排除']
    magList = [workFourm.articleINFO[articleCode].magnet  for articleCode in todays if workFourm.articleINFO[articleCode].tag != '素人已排除']
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
        title = avList[idx][0]
        magnet = avList[idx][1]
        print("[*]" + '*'*50)
        print("[*]目前選擇的是:")
        action = input(f"[>]{idx}. {title}: ")
        if action == '-1' and idx == 1:
            print("[!]目前還不能取消操作 ! ")
            continue
                
        if action == '-1':
            idx -= 1
            continue
        elif action == '':
            if magnet in magnetSelected:                
                magnetSelected.remove(magnet)
                print(f'[*]已取消 {title} 的 magnet 選取 ! ')
            else:
                print('[*]不要這部 ! ')
        else:
            print(f'[>]已選擇 {title} 之 magnet: {magnet}')
            if magnet in magnetSelected:
                print("[!]這部已經選取過了喔~ 已在清單內")
            else:
                print("[*]添加成功 ! ")
                magnetSelected.append(magnet)
        idx += 1

    return magnetSelected

# test = Sehuatang()

# print(test.get_todayList('https://www.sehuatang.org/forum-37-1.html'))
