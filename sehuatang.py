import requests
import bs4
from rich.progress import track
from package.tools import make_html

class Article():
    pass
    # def __init__(self, link: str, title: str, imgLinks: list, magnet: str) -> None:
    #     self.link = link
    #     self.title = title
    #     self.imgLinks = imgLinks
    #     self.magnet = magnet

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

    def getMagnets(self, todayList: list) -> dict:
        magnetDict = {}

        for progress, articleCode in zip(track(todayList, description="[\]正在抓取 Magnet "), todayList):
            response_of_pages = requests.get(
                "https://www.sehuatang.org/thread-" + articleCode + "-1-1.html"
            )
            bs_pages = bs4.BeautifulSoup(response_of_pages.text, "html.parser")

            magnet = bs_pages.find("div", "blockcode").get_text()
            magnetDict[articleCode] = magnet.removesuffix("复制代码")
            self.articleINFO[articleCode].magnet = magnetDict[articleCode]

        return magnetDict

    def getPics(self, todayList: list) -> dict:
        picsDict = {}
        picsList = []

        for progress, articleCode in zip(track(todayList, description="[\]正在抓取預覽圖片"), todayList):
            response_of_pages = requests.get(
                "https://www.sehuatang.org/thread-" + articleCode + "-1-1.html"
            )
            soup = bs4.BeautifulSoup(response_of_pages.text, "html.parser")

            img_block = soup.find_all("ignore_js_op")

            picsList.append("Head of Page")
            for block in img_block[:-1]:
                pic_link = block.find("img").get("file")
                if pic_link != None:
                    picsList.append(pic_link)                    
            picsList.append("end of page")

            picsDict[articleCode] = picsList
            self.articleINFO[articleCode].imgLinks = picsDict[articleCode]

        # path, fileName = make_html(pic_link_List, "Auto_SHT_Pic.html")
        # return path, fileName
        # return picsDict

    def showV(self):
        print(vars(vars(self)['articleINFO']['613213']))


uma = Sehuatang()

todays = uma.get_todayList('https://sehuatang.org/forum-36-1.html')
mags = uma.getMagnets(todays)
uma.getPics(todays)
# print(mags)
# uma.showV()
make_html(uma.articleINFO.values(), 'test.html')
