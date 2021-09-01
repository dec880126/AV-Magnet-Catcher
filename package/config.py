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
    elif mode == "Uncensored":
        temp = []
        for item in config["Uncensored"]["exclude"].replace(" ", "").split(","):
            temp.append(item)

        return {
            "exclude": tuple(temp)
        }
    elif mode == "Cookies":
        return {
            "t66y": config["Cookies"]["t66y"],
            "FileSave2009": config["Cookies"]["FileSave2009"]
        }
    else:
        print("[!]Error: 請選擇 load_config 之模式")


def make_config(path: str, showINFO = True) -> None:
    if showINFO:
        print("[/]正在生成 Config 中...")

    with open(path, "w", encoding="utf-8") as f:
        # system_config(f)
        uncensored_config(f)
        # cookie_config(f)

    if showINFO:
        print("[!] Config 已生成!")


def write_config(path, content) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def system_config(f: TextIOWrapper) -> None:
    f.write("[Setting]\n")
    f.write("Synology = \n")
    f.write("MultiThreading = \n")


def uncensored_config(f: TextIOWrapper) -> None:
    f.write("\n[Uncensored]\n")
    f.write("exclude = \n")

def cookie_config(f: TextIOWrapper) -> None:
    f.write("\n[Cookies]\n")
    f.write("t66y = \n")
    f.write("FileSave2009 = \n")


