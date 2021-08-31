import requests
import bs4

import magnet
import package.config

url = 'http://t66y.com/htm_data/2108/2/4668051.html'

req_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
    "Accept": "text/html",
    "Cookie": "227c9_lastvisit=0%091630325666%09%2Fthread0806.php%3Ffid%3D15%26search%3D2"
}

res = requests.get(url, headers=req_headers)
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

print(title)
print(downloadPage_link)
for link in imgLinks:
    if link.get("src") == None:
        print(link.get("ess-data"))
        continue
    print(link.get("src"))

print(f"magnet: {magnet.get_magnet(downloadPage_link, cookie=package.config.load_config(mode='Cookies')['FileSave2009'])}")
    