import os
import re
import time
import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

def make_html(pageINFOs: list, fileName: str):
    '''
    Read the url in the imgLinks, and make the HTML file

    pageINFOs is list of Article() in sehuatang.py

    type imgLinks: list
    '''
    path = "./" + fileName

    print(f"[/]{fileName} 產生中...")
    f = open(path, 'w', encoding="utf-8")

    # HTML declaration
    f.write("""<!doctype html>\n<html>\n\t<head>\n\t\t<title>AVMC Picture Viewer</title>\n\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bxslider/4.2.15/jquery.bxslider.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bxslider/4.2.15/jquery.bxslider.min.css" rel="stylesheet" />
    <script>
        $(document).ready(function(){
            $('.bxslider').bxSlider();
        });
    </script></head>\n""")

    # CSS declaration
    f.write("""\t<style>\n\t\tbody{\n\t\t\tbackground: #ebe9f9; /* Old browsers */\n\t\t\tbackground: -moz-linear-gradient(top, #ebe9f9 0%, #d8d0ef 50%, #cec7ec 51%, #c1bfea 100%); /* FF3.6-15 */\n\t\t\tbackground: -webkit-linear-gradient(top, #ebe9f9 0%,#d8d0ef 50%,#cec7ec 51%,#c1bfea 100%); /* Chrome10-25,Safari5.1-6 */\n\t\t\tbackground: linear-gradient(to bottom, #ebe9f9 0%,#d8d0ef 50%,#cec7ec 51%,#c1bfea 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */\n\t\t\tfilter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ebe9f9', endColorstr='#c1bfea',GradientType=0 ); /* IE6-9 */\n\t\t}\n\t</style>\n""")

    # HTML body writing
    f.write("""\t<body>\n\t\t<div style="text-align:center;">\n""")

    for page in  pageINFOs:
        if page.tag == '素人已排除':
            continue
        link = page.link
        title = page.title
        imgLinks = page.imgLinks
        magnet = page.magnet

        for imgLink in imgLinks:
            if imgLink == "Head of Page":
                # 標題
                f.write(f"""\t\t\t<h2><a href="{link}"  target="_blank">{title}</a></h2>\n\t\t\t\t<ul class="bxslider">\n""")
            elif imgLink == "end of page":
                # 頁尾
                if 'magnet:?xt=urn:btih:' in magnet:
                    to_write = f"\t\t\t\t</ul>\t\t\t\t<br>\n\t\t\t\t<h3><a>{magnet}</a></h3>\n"
                else:
                    to_write = f"\t\t\t\t</ul>\t\t\t\t<br>\n\t\t\t\t<h3><a href = '{magnet}'>下載連結</a></h3>\n"
                f.write(to_write)
                f.write("\t\t\t<hr />\n")
            else:
                # 圖片
                # 可擴充: loading="lazy"
                f.write("\t\t\t\t<li><img src = " + imgLink + """ class="center" /></li>\n""") #  width=50%""" + """ height=50%

    f.write("""\t\t\t<a>Copyright © 2021.</a><a href = "https://github.com/dec880126" target="_blank">Cyuan</a><a>&nbsp&nbspAll rights reserved. </a>\n\t\t</div>\n\t</body>\n</html>""")
    f.close()
    path = f"{os.getcwd()}\{path[2:]}"
    
    print(f"[*]{fileName} 產生成功! -> 檔案路徑: {path} 系統將自動開啟檔案...")
    return path, fileName

def clearConsole() -> None:
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"
    os.system(command)

def changeDate(today: str) -> datetime:
    """
    In this function can input the days you want to change
    rtype: datetime
    """
    print('[*]===============================================')
    print(f"[*]今天是 {today}")
    print(f"[*]操作方式:\n[*]\t昨天: -1, 前天: -2... 最多到-5\n[*]\t若要重置為今日日期，請輸入 'reset'")
    print('[*]===============================================')
    date = input("[?]請問日期要更改為?:")
    if date in ('reset', 'RESET'):
        new_date = str(time.strftime("%Y-%m-%d", time.localtime()))
        print(f"[*]日期已重置為今日日期: {new_date}")
        input('[*]請按 Enter 鍵回到主選單...')
        return new_date

    if int(date) < 0 and int(date) > -6:
        new_date = getYesterday(abs(int(date)))
    else:
        new_date = today

    print(f"[*]日期已更新為: {new_date}")
    input('[*]請按 Enter 鍵回到主選單...')
    return new_date

def getYesterday(how_many_day_pre) -> datetime: 
    """
    Get date you want by input parameter
    type how_many_day_pre: int
    rtype: datetime
    """
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=how_many_day_pre) 
    yesterday=today-oneday  
    return yesterday

def is_shirouto(title):
    number_from_shirouto = re.compile(r"\d+\D+-\d+")
    # number_from_studio = re.compile(r'\D+-\d+')

    try:
        # 先檢查是否為素人 ex: 498DDH-023(數字英文-數字)
        is_shirouto = True
        video_num = number_from_shirouto.search(title).group()
    except AttributeError:
        # 否則為一般番號 ex: STARS-401(英文-數字)
        is_shirouto = False
    return is_shirouto and 'FC2PPV' not in title

def remove_html_if_exist():
    typeList = ("無碼", "有碼", "國產", "歐美", "中文")
    for fourm in typeList:
        path_HTML = "./" + "AVMC-Viewer-SHT-" + fourm + ".html"
        if os.path.isfile(path_HTML):
            os.remove(path_HTML)
            print("[*]" + path_HTML + " -> HTML files 已刪除")

        path_HTML = "./" + "AVMC-Viewer-T66Y-" + fourm + ".html"
        if os.path.isfile(path_HTML):
            os.remove(path_HTML)
            print("[*]" + path_HTML + " -> HTML files 已刪除")            

def get_proxy(proxy ,timeout = 2, extract_maximum = 10, good_proxy_define: float = 2.0):

    # if not validProxy:
    try:
        begin = time.time()
        requests.get(
            url = 'https://api.ipify.org?format=json',
            proxies={
                'http':"http://" + proxy,
                'https':"http://" + proxy
            },
            timeout = timeout
        )
        spend_time = time.time() - begin
        good_proxy = spend_time < good_proxy_define
        text = f'延遲小於 {good_proxy_define} 秒: 採用' if good_proxy else f'延遲大於 {good_proxy_define} 秒: 不採用'
        print(f"[>]{proxy} -> 有效 / 耗時: {spend_time: 2.2f}s / {text}")
        if good_proxy:
            validProxy.append(proxy)
    except requests.exceptions.ConnectTimeout:
        print(f"[!] {proxy} -> 失敗 ! ")


def get_proxy_in_multi_threading(extract_maximum = 10) -> list:    
    global validProxy
    validProxy = []

    res = requests.get('https://free-proxy-list.net/')
    freeProxys = re.findall('\d+\.\d+\.\d+\.\d+:\d+', res.text)

    print(f"[*]這次共有 {len(freeProxys)} 個免費代理待測")

    executor = ThreadPoolExecutor(max_workers=20)

    # submit()的參數： 第一個為函數， 之後為該函數的傳入參數，允許有多個
    future_tasks = [executor.submit(get_proxy, freeProxy) for freeProxy in freeProxys]

    # 等待所有的線程完成，才進入後續的執行
    wait(future_tasks, return_when=ALL_COMPLETED)

    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     executor.map(get_proxy, freeProxys)
    
    print(f"[>]從 {len(freeProxys)} 個免費代理中取得了 {len(validProxy)} 個有效代理")
    return validProxy


# print(get_proxy_in_multi_threading())