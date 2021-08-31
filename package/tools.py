import os

def make_html(input_list, fileName, titleList, magnetList, article_Code_List):
    '''
    Read the url in the input_list, and make the HTML file
    type input_list: list
    '''
    path = "./" + fileName

    print(f"[/]{fileName} 產生中...")
    f = open(path, 'w', encoding="utf-8")

    # HTML declaration
    f.write(f"""<!doctype html>\n<html>\n\t<head>\n\t\t<title>Auto SHT Picture Viewer</title>\n\t</head>\n""")

    # CSS declaration
    f.write("""\t<style>\n\t\tbody{\n\t\t\tbackground: #ebe9f9; /* Old browsers */\n\t\t\tbackground: -moz-linear-gradient(top, #ebe9f9 0%, #d8d0ef 50%, #cec7ec 51%, #c1bfea 100%); /* FF3.6-15 */\n\t\t\tbackground: -webkit-linear-gradient(top, #ebe9f9 0%,#d8d0ef 50%,#cec7ec 51%,#c1bfea 100%); /* Chrome10-25,Safari5.1-6 */\n\t\t\tbackground: linear-gradient(to bottom, #ebe9f9 0%,#d8d0ef 50%,#cec7ec 51%,#c1bfea 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */\n\t\t\tfilter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ebe9f9', endColorstr='#c1bfea',GradientType=0 ); /* IE6-9 */\n\t\t}\n\t</style>\n""")

    # HTML body writing
    f.write("""\t<body>\n\t\t<div style="text-align:center;">\n""")
    pageNum = 0
    for url in input_list:
        title = titleList[pageNum]
        article_Code = article_Code_List[pageNum]
        article_URL = "https://www.sehuatang.org/thread-" + article_Code + "-1-1.html"
        if url == "None":
            continue
        elif url == "end of page":
            to_write = "\t\t\t\t<br>\n\t\t\t\t<h3>" + magnetList[pageNum] + "</h3>\n"
            f.write(to_write)
            f.write("\t\t\t<hr />\n")
            pageNum += 1
        elif url == "Head of Page":
            f.write(f"""\t\t\t<h2><a href="{article_URL}"  target="_blank">{title}</a></h2>\n""")
        else:
            # 可擴充: loading="lazy"
            f.write("\t\t\t\t<img src = " + str(url) + """ width=auto""" + """ height=auto class="center">\n""")

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