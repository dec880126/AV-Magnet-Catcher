"""
AVMC 之 Config 相關函式集
預設編碼: UTF-8
"""
import configparser
from io import TextIOWrapper
import os
from typing import Dict

def check_config_if_exist(path) -> bool:
    return bool(os.path.isfile(path))


def load_system_config(path = "./config.ini") -> Dict:
    config = configparser.ConfigParser()    
    config.read(path, encoding="utf-8")

    return {
        "Synology": config["Setting"]["Synology"],
        "MultiThreading": config["Setting"]["MultiThreading"]
    }

def load_uncensored_config(path = "./config.ini") -> Dict:
    """
    Type:
        exclude -> Tuple
    """
    config = configparser.ConfigParser()    
    config.read(path, encoding="utf-8")
    temp = []
    for item in config["Uncensored"]["exclude"].replace(" ", "").split(","):
        temp.append(item)

    return {
        "exclude": tuple(temp)
    }


def make_config(path: str) -> None:

    with open(path, "w", encoding="utf-8") as f:
        system_config(f)
        uncensored_config(f)


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

