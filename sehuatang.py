import requests
import bs4
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
from rich.progress import Progress, track
from package.tools import make_html
import time

class Article():
    def __init__(self) -> None:
        self.safe = False

class Sehuatang():
    def __init__(self) -> None:
        self.articleINFO = {}        

    def get_todayList(self, URL, todayIs: str = '2021-09-28') -> list:
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
    for progress, task in zip(track(todays, description=f"[\]正在分析文章資料"), todays):
        while not progress_done:
            pass

def task_articleParser():
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(uma.get_Magnet_and_Pics, todays)

def start():
    global uma, todays
    uma = Sehuatang()
    todays = uma.get_todayList('https://sehuatang.org/forum-36-1.html')

    task_pgbar = threading.Thread(target=task_progress_bar)
    task_pgbar.start()
    task_article = threading.Thread(target=task_articleParser)
    task_article.start()
    
    task_article.join()
    task_pgbar.join()

    make_html(uma.articleINFO.values(), 'test.html')

# start()