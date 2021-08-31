import requests
import bs4
import concurrent.futures
import time
from datetime import datetime
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(getData.get_today_article, fourms, homeCodes, todays, pages)

import package.config as config
import package.tools as tools
from package.magnet import get_magnet

class Fourm():
    def __init__(self, fourmName, infoDict) -> None:
        self.fourmName = fourmName
        self.infoDict = infoDict

def get_todayLists(fourmName_zh: str, fourmName_en: str) -> list:
    fourmDict = {}
    urlDict = {
        "無碼": "http://t66y.com/thread0806.php?fid=2&search=2"
    }

    fourmDict[fourmName_zh] = Fourm(fourmName_zh, config.load_config(mode=fourmName_en))

    res = requests.get(urlDict[fourmName_zh], headers=t66y_headers)
    res.encoding = "gbk"
    res.content.decode('gbk').encode('utf-8')

    htmlSoup = bs4.BeautifulSoup(res.text, "html.parser")

    tbody = htmlSoup.find("tbody", attrs={"id": "tbody"})
    articles = tbody.find_all("tr", attrs={"class": "tr3 t_one tac"})
    articleURLs = []

    for article in articles:
        # <----- 檢查標籤是否為「新作」 start ----->
        ifNew = article.find("span").get("class")
        if ifNew[0] != "newworks":
            continue
        # <----- 檢查標籤是否為「新作」 end ----->

        # <----- 篩選本日文章 start ----->        
        today = datetime.now().strftime("%Y-%m-%d")
        releaseDate = article.find("div", attrs={"class": "f12"}).find("span").get("title")
        if len(releaseDate) < 6:
            releaseDate = article.find("div", attrs={"class": "f12"}).find("span").get_text()
        else:
            releaseDate = releaseDate[-10:]
            
        if releaseDate != today:
            continue
        # <----- 篩選本日文章 end ----->        


        info = article.find("a", attrs={"target": "_blank"})

        # <----- 關鍵字排除 start ----->  
        if any(
            [filter in info.get_text() for filter in fourmDict["無碼"].infoDict["exclude"]] # fourmDict["無碼"].infoDict["exclude"]: 要排除之標題關鍵字
        ):
            continue
        # <----- 關鍵字排除 end ----->

        articleURLs.append(f"http://t66y.com/{info.get('href')}")

    return articleURLs

def article_parser(url):
    """
    rtype title: str
    rtype imgLinks: list
    rtype magnet: str
    """

    res = requests.get(url, headers = t66y_headers)
    res.encoding = "gbk"
    res.content.decode('gbk').encode('utf-8')


    soup = bs4.BeautifulSoup(res.text, "html.parser")

    mainBlock = soup.find_all("td", attrs={"valign": "top"}, limit=1)[0]

    title = mainBlock.find("h4").get_text()
    downloadPage_link = mainBlock.find_all("a", attrs={"style": "cursor:pointer;color:#008000;"}, limit=1)[0].get_text()

    temp = []
    imgLinks = mainBlock.find_all("img")
    for link in imgLinks:
        temp.append(link)

    temp.reverse()
    imgLinks = temp.copy()

    # print(title)
    # print(downloadPage_link)
    temp = []
    for link in imgLinks:
        if link.get("src") == None:
            temp.append(link.get("ess-data"))
            continue
        temp.append(link.get("src"))
    imgLinks = temp.copy()
    magnet = get_magnet(
        downloadPage_link, 
        cookie=config.load_config(mode='Cookies')['FileSave2009']
    )

    return title, imgLinks, magnet

if __name__ == "__main__":
    Cookies = config.load_config(mode="Cookies")

    t66y_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html",
        "Cookie": Cookies["t66y"]
    }


    print(get_todayLists(fourmName_zh="無碼", fourmName_en="Uncensored"))

    # t, imgs, m = article_parser(url='http://t66y.com/htm_data/2108/2/4668051.html')
