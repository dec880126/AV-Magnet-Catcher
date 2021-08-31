import requests
import bs4

def get_magnet(url, cookie) -> str:
    """
    return magnet
    """
    res = requests.get(url, headers={"Cookie": cookie})

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    ref = soup.find_all("input", attrs={"id": "ref"})[0].get("value")
    # print(f"{ref=}")

    magnet_request = "http://www.rmdown.com/download.php?action=magnet&ref=" + ref

    res = requests.get(magnet_request, headers={"Cookie": cookie})

    return res.text

# get_magnet(url = "http://www.rmdown.com/link.php?hash=212683e8017ade69fa7d2a161a2c411d959406d036b", cookie="PHPSESSID=p2qmskq9kgjq5qeckatlv5gsv5")