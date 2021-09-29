from bs4.element import Tag
import requests
import bs4
import time
from datetime import datetime
from rich.progress import track
import webbrowser
# import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(getData.get_today_article, fourms, homeCodes, todays, pages)

import package.config as config
import package.tools as tools
# from package.magnet import get_magnet



class Fourm():
    def __init__(self, fourmName, infoDict) -> None:
        self.fourmName = fourmName
        self.infoDict = infoDict

class Article():
    def __init__(self, link: str, title: str, imgLinks: list, magnet: str) -> None:
        self.link = link
        self.title = title
        self.imgLinks = imgLinks
        self.magnet = magnet

def get_todayLists(fourmName_zh: str, fourmName_en: str, scrabDate: str) -> list:
    fourmDict = {}
    urlDict = {
        "無碼": "http://t66y.com/thread0806.php?fid=2&search=2"
    }

    fourmDict[fourmName_zh] = Fourm(fourmName_zh, config.load_config(mode=fourmName_en))

    res = requests.get(urlDict[fourmName_zh], headers=t66y_headers)
    res.encoding = "gbk"
    res.content.decode('gbk').encode('utf-8')

    with open("./res.html", "w", encoding="utf-8") as f:
        f.write(res.text)

    htmlSoup = bs4.BeautifulSoup(res.text, "html.parser")

    tbody = htmlSoup.find("tbody", attrs={"id": "tbody"})
    articles = tbody.find_all("tr", attrs={"class": "tr3 t_one tac"})
    articleURLs = []
    # topMarks = []

    # show info of exclude
    print(f"[*]關鍵字排除 -> {fourmDict[fourmName_zh].infoDict}")
    for article in articles:    
        # <----- 檢查標籤是否為「新作」 start ----->
        ifNew = article.find("span").get("class")
        if ifNew[0] != "newworks":
            continue
        # <----- 檢查標籤是否為「新作」 end ----->

        # <----- 篩選本日文章 start ----->
        releaseDate = article.find("div", attrs={"class": "f12"}).find("span").get("title")
        # print(releaseDate)
        if len(releaseDate) < 6:
            releaseDate = article.find("div", attrs={"class": "f12"}).find("span").get_text()

        # !FIXME: 待觀察 t66y 網站動態 Top-Marks好像只會出現一陣子
        # elif releaseDate.startswith("置顶主题"):
        #     print(f"置顶主题: {article.find('a', attrs={'target': '_blank'}).get_text()}")
        #     url = article.find("a", attrs={"target": "_blank"})
        #     if getRidof_keyWord(url, fourmDict):
        #         continue

        #     url_base = "http://t66y.com/"
        #     url = url_base + url.get('href')
        #     articleURLs.append(f"{url}")
        #     continue

        else:
            releaseDate = releaseDate[-10:]
            
        # TODO: 測試完要重新開啟 此為挑選本日文章功能
        if releaseDate != scrabDate:
            continue
        # <----- 篩選本日文章 end ----->        


        url = article.find("a", attrs={"target": "_blank"})

        # <----- 關鍵字 start -----> 
        # 排除
        # print(f"{getRidof_keyWord(url, fourmDict)=}")
        # print(f"{len(fourmDict[fourmName_zh].infoDict.values())=}")
        if getRidof_keyWord(url, fourmDict) and fourmDict[fourmName_zh].infoDict['exclude'][0] != "":
            continue
        # <----- 關鍵字 end ----->

        url_base = "http://t66y.com/"
        url = url_base + url.get('href')
        articleURLs.append(f"{url}")

    return articleURLs

def article_parser_core(url: str):
    """
    type url: str
    rtype title: str
    rtype imgLinks: list
    rtype magnet: str
    """
    temp = []
    res = requests.get(url, headers = t66y_headers)
    res.encoding = "gbk"
    res.content.decode('gbk').encode('utf-8')

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    mainBlock = soup.find_all("td", attrs={"valign": "top"}, limit=1)[0]

    title = mainBlock.find("h4").get_text()
    downloadPage_link = mainBlock.find_all("a", attrs={"style": "cursor:pointer;color:#008000;"}, limit=1)[0].get_text()

    imgLinks = mainBlock.find_all("img")
    # _class_image_big = mainBlock.find_all("div", attrs={"class": "image-big"})
    # imgLinks = mainBlock.find_all("img")

    temp.append("Head of Page")
    # for block in _class_image_big:
    #     try:
    #         if block.get("src") == None:
    #             t = block.get("ess-data")
    #             temp.append(t)
    #             continue
    #         t = block.get("src")
    #     except AttributeError:
    #         pass
    #     if "contents-thumbnail2.fc2.com/w240/" in t:
    #         # 將fc2小圖換成大圖
    #         t = t.replace("contents-thumbnail2.fc2.com/w240/", "")
    #     if "s.jpg" in t:
    #         t = t.replace("s.jpg", ".jpg")
    #     temp.append(t)
    for image in imgLinks:
        img_link = image.get("ess-data")
        if img_link == None:
            continue
        if "thumbnail" in img_link:
            # img_link = img_link.replace("contents-thumbnail2.fc2.com/w240/", "")
            continue
        temp.append(img_link)
    temp.append("end of page")
    imgLinks = temp.copy()    
    
    articleDict[url] = Article(url, title, imgLinks, downloadPage_link)

def article_parser_executor(urls: list):
    print("[*]正在分析文章資訊...")
    start_time = time.time()
    for progress, url in zip(track(urls, description='[>]正在分析文章'), urls):
        article_parser_core(url)
    end_time = time.time()
    print(f"[*]一共花了 {end_time - start_time:2.2f} 秒來分析 {len(urls)} 篇文章")

def getRidof_keyWord(url: Tag, fourmDict: dict) -> bool:
    """
    fourmDict["無碼"].infoDict["exclude"]: 要排除之標題關鍵字
    """
    return any([filter in url.get_text() for filter in fourmDict["無碼"].infoDict["exclude"]])

def start(scrabDate: str):
    _session = requests.session()
    _session.get(
        "http://t66y.com/thread0806.php?fid=2&search=2", 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
        }
    )
    Cookies = {
        "t66y": _session.cookies.values()[0]
    }

    global t66y_headers
    t66y_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html",
        "Cookie": Cookies["t66y"]
    }

    links = get_todayLists(fourmName_zh="無碼", fourmName_en="Uncensored", scrabDate=scrabDate)

    global articleDict
    articleDict = {}
    article_parser_executor(links)

    fileName = "AVMC-Viewer-T66Y-" + "無碼" + ".html"
    tools.make_html(articleDict.values(), fileName)
    webbrowser.open_new_tab(fileName)

