import requests
import bs4
import time
import webbrowser
import re
from datetime import datetime
import rich
from rich.progress import track
# import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(getData.get_today_article, fourms, homeCodes, todays, pages)

import package.config as config
from package.tools import make_html as html_maker
# from package.magnet import get_magnet


class Article():
    def __init__(self) -> None:
        self.title = ""
        self.number = ""   
        self.link = ""
        self.magnet = ""
        self.imgLinks = []
        self.tag = ""
        self.VR = False

class T66Y():
    def __init__(self) -> None:
        self.todayList = []
        self.articleINFO = {}
        self.headers = {}

    def get_cookie(self) -> None:
        _session = requests.session()
        _session.get(
            "http://t66y.com/thread0806.php?fid=2&search=2", 
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
            }
        )
        cookie = _session.cookies.values()[0]
        
        self.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
        self.headers["Accept"] = "text/html"
        self.headers["Cookie"] = cookie

    def get_todayList(self, fourmType: str, today: str = datetime.now().strftime("%Y-%m-%d")) -> None:
        """
        無碼: http://t66y.com/thread0806.php?fid=2&search=2&page=1
        有碼: http://t66y.com/thread0806.php?fid=15&search=2&page=1
        """
        today = "2021-10-02"
        if fourmType == "無碼":
            urlBase = "http://t66y.com/thread0806.php?fid=2&search=2"
        elif fourmType == "有碼":
            urlBase = "http://t66y.com/thread0806.php?fid=15&search=2"

        urlList = []

        for pageNum in range(1, 10):
            res = requests.get(
                url = f'{urlBase}&page={pageNum}',
                headers = self.headers
            )
            res.encoding = "gbk"
            res.content.decode('gbk').encode('utf-8')

            soup = bs4.BeautifulSoup(res.text, "html.parser")
            tbody = soup.find(
                "tbody",
                attrs={
                    "style": "table-layout:fixed;",
                    "id": "tbody"
                }
            )
            trs = tbody.find_all("tr", attrs = {"class": "tr3 t_one tac"})

            articleNums_of_current_page = len(trs)

            temp = []
            for tr in trs:
                try:
                    releaseDate = tr.find("span", attrs = {"class": "s3"}).get("title")
                except AttributeError:
                    try:
                        releaseDate = tr.find("span", attrs = {"class": "s5"}).get("title")
                    except AttributeError:
                        div = tr.find("div", attrs = {"class": "f12"})
                        releaseDate = div.find("span").get_text()
                if today not in releaseDate:
                    urlList.extend(temp)
                    self.todayList = urlList
                    print(f"總共抓了 {len(urlList)} 部本日文章")
                    return

                title_link = tr.find("a", attrs={"target": "_blank"})
                title = title_link.get_text()
                link = "http://t66y.com/" + title_link.get("href")

                temp.append(link)                             

                if title[0] == "[":
                    (resolution, dataSize) = title.split("]")[0].replace("[", "").split("/")
                elif title[0] == "【":
                    (resolution, dataSize) = title.split("】")[0].replace("【", "").split("/")

                numberParser = re.compile(r"\w+-\d+")
                number = numberParser.search(title).group()
                title = title.split(number)[1]
                if "】" in title:
                    title = title.split("】")[-1]
                elif "]" in title:
                    title = title.split("]")[-1]
                
                if "VR" in title:
                    VR = True
                    title = title = title.split("】")[-1]
                else:
                    VR = False
                # print(f"{number}\n\t{title}")

                self.articleINFO[link] = Article()
                self.articleINFO[link].title = title
                self.articleINFO[link].number = number
                self.articleINFO[link].link = link
                if number[0] in [str(integer) for integer in range(10)]:
                    print("新增tag -> 素人已排除")
                    self.tag = "素人已排除"
                if VR:
                    print("已偵測到VR作品")
                    self.VR = True
                # if tr is trs[articleNums_of_current_page - 1]:
                #     print(f"這是第 {pageNum} 頁的最後一篇\n\t以上共 {articleNums_of_current_page} 篇文章")
            
            urlList.extend(temp)

    def articleParser(self, url: str) -> None:
        res = requests.get(url, headers = self.headers)
        res.encoding = "gbk"
        res.content.decode('gbk').encode('utf-8')

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        mainBlock = soup.find("td", attrs={"valign": "top"})

        downloadPage_link = mainBlock.find("a", attrs={"style": "cursor:pointer;color:#008000;"}).get("href")        

        temp = []
        temp.append("Head of Page")

        imgs = mainBlock.find_all("img")
        for image in imgs:
            imgLink = image.get("src")
            if imgLink == None:
                continue
            temp.append(imgLink)

        try:
            gallery = mainBlock.find("div", attrs={"class": "cl-gallery"})
            picblocks = gallery.find_all("a")
            for picBlock in picblocks:
                imgLink = picBlock.get("href")
                temp.append(imgLink)
        except AttributeError:
            print(f"AttributeError -> {url}")
        temp.append("end of page")
        imgLinks = temp.copy()

        self.articleINFO[url].magnet = downloadPage_link
        self.articleINFO[url].imgLinks = imgLinks

    def parse_article_in_todayList(self):
        print("Parser Start")
        for url in self.todayList:
            print(f"正在分析: {url}")
            self.articleParser(url)

    def make_html(self, fileName: str) -> None:
        html_maker(self.articleINFO.values(), fileName)

    def show(self):
        print(f"{self.todayList=}")
        # for article in self.articleINFO.values():
        #     print(f"{article.title}")
        #     print(f"{article.link}")
        #     print(f"{article.magnet}")
        #     print(f"{article.imgLinks}")

test = T66Y()

test.get_cookie()

test.get_todayList(fourmType = "有碼")

test.parse_article_in_todayList()

# test.show()

test.make_html("測試.html")

# test.get_cookie()
# test.articleParser("http://t66y.com/htm_data/2110/15/4719933.html")
# test.make_html("./測試.html")