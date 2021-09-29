import requests
import bs4
from concurrent.futures import ThreadPoolExecutor
import threading
from rich.progress import track
from package.tools import make_html
import webbrowser
from datetime import datetime

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
        executor.map(uma.get_Magnet_and_Pics, todays)

def start():
    global uma, todays
    uma = Sehuatang()
    URL_library = {
        1: 'https://www.sehuatang.org/forum-36-1.html',
        2: 'https://www.sehuatang.org/forum-37-1.html',
        3: 'https://www.sehuatang.org/forum-2-1.html',
        4: 'https://www.sehuatang.org/forum-38-1.html',
        5: 'https://www.sehuatang.org/forum-103-1.html'
    }

    todays = uma.get_todayList(URL_library[chooseFourm()])

    task_pgbar = threading.Thread(target=task_progress_bar)
    task_pgbar.start()
    task_article = threading.Thread(target=task_articleParser)
    task_article.start()
    
    task_article.join()
    task_pgbar.join()

    print(f"[!]共 {todays} 篇文章")
    fileName =  "AVMC-Viewer-SHT" + "無碼" + ".html"
    make_html(uma.articleINFO.values(), fileName)
    webbrowser.open_new_tab(fileName)

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