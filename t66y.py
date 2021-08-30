import requests
import bs4
import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(getData.get_today_article, fourms, homeCodes, todays, pages)

import package.config as config
import package.tools as tools

class Fourm():
    def __init__(self, fourmName, infoDict) -> None:
        self.fourmName = fourmName
        self.infoDict = infoDict

urlDict = {
    "無碼": "http://t66y.com/thread0806.php?fid=2&search=2"
}
fourmDict = {}

req_headers = {
    "Host": "t66y.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-TW,zh;q=0.9,ja;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5,zh-CN;q=0.4",
    "Cookie": "227c9_lastvisit=0%091630325666%09%2Fthread0806.php%3Ffid%3D15%26search%3D2"
}

fourmDict["無碼"] = Fourm("無碼", config.load_uncensored_config())

res = requests.get(urlDict["無碼"], headers=req_headers)
res.encoding = "gbk"
res.content.decode('gbk').encode('utf-8')

htmlSoup = bs4.BeautifulSoup(res.text, "html.parser")

tbody = htmlSoup.find("tbody", attrs={"id": "tbody"})
articles = tbody.find_all("tr", attrs={"class": "tr3 t_one tac"})
articleURLs = []

for article in articles:
    ifNew = article.find("span").get("class")
    if ifNew[0] != "newworks":
        continue   

    info = article.find("a", attrs={"target": "_blank"})

    
    if any(
        [filter in info.get_text() for filter in fourmDict["無碼"].infoDict["exclude"]]
    ):
        continue
    articleURLs.append(f"http://t66y.com/{info.get('href')}")

print(fourmDict["無碼"].infoDict["exclude"])