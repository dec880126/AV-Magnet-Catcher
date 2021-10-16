"""
AVMC 之 Config 相關函式集
預設編碼: UTF-8
"""
import configparser
from io import TextIOWrapper
import os

def check_config_if_exist(path) -> bool:
    return bool(os.path.isfile(path))


def load_config(path = "./config.ini", mode=None) -> dict:
    """
    MODE LIST
     - Setting
     - Uncensored
     - Cookies
    """
    config = configparser.RawConfigParser()   
    config.read(path, encoding="utf-8")

    if mode == "Setting":
        return {
            "Synology": config["Setting"]["Synology"],
            "MultiThreading": config["Setting"]["MultiThreading"]
        }
    elif mode == "t66y":
        temp = []
        for item in config["t66y"]["exclude"].replace(" ", "").split(","):
            temp.append(item)

        return {
            "exclude": tuple(temp)
        }
    elif mode == "Cookies":
        return {
            "t66y": config["Cookies"]["t66y"],
            "FileSave2009": config["Cookies"]["FileSave2009"]
        }
    elif mode == 'Synology':
        return {
            "upload": config["Synology"]["upload"] == '1',
            "IP": config["Synology"]["IP"] if config["Synology"]["IP"] else None,
            "PORT": config["Synology"]["PORT"] if config["Synology"]["PORT"] else None,
            "PATH": config["Synology"]["PATH"] if config["Synology"]["PATH"] else None,
            "SECURE": config["Synology"]["SECURE"] == 1,
            "USER": config["Synology"]["USER"] if config["Synology"]["USER"] else None,
            "PASSWORD": config["Synology"]["PASSWORD"] if config["Synology"]["PASSWORD"] else None,
        }
    elif mode == "Sehuatang":
        return {
            "exclude": config["Sehuatang"]["exclude"],
            'jav_no_shirouto': True if config["Sehuatang"]["jav_no_shirouto"] == '1' else False
        }
    else:
        print("[!]Error: 請選擇 load_config 之模式")


def make_config(path: str, showINFO = True) -> None:
    if showINFO:
        print("[/]正在生成 Config 中...")

    with open(path, "w", encoding="utf-8") as f:
        # system_config(f)
        t66y_config(f)
        # cookie_config(f)
        synology_config(f)
        sht_config(f)

    if showINFO:
        print("[!] Config 已生成!")


def write_config(path, content) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def system_config(f: TextIOWrapper) -> None:
    f.write("[Setting]\n")
    f.write("Synology = \n")
    f.write("MultiThreading = \n")


def t66y_config(f: TextIOWrapper) -> None:
    f.write("\n[t66y]\n")
    f.write("exclude = \n")

def cookie_config(f: TextIOWrapper) -> None:
    f.write("\n[Cookies]\n")
    f.write("t66y = \n")
    f.write("FileSave2009 = \n")

def synology_config(f: TextIOWrapper) -> None:
    f.write("\n[Synology]\n")
    f.write("; 若要開啟 Synology 自動上傳，將 upload 設為1\n")
    f.write("upload = 0\n")
    f.write("IP = \n")
    f.write("PORT = 5000\n")
    f.write("; BT 下載之路徑\n")
    f.write("PATH = \n")
    f.write("; SECURE 預設為0\n")
    f.write("SECURE = 0\n")
    f.write("USER = \n")
    f.write("PASSWORD = \n")

def sht_config(f: TextIOWrapper) -> None:
    f.write("\n[Sehuatang]\n")
    f.write("exclude = \n")
    f.write("jav_no_shirouto = \n")