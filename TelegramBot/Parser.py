import requests
from bs4 import BeautifulSoup

from TelegramBot.Proxy import getProxy


def getHtml(url):
    proxy_list = getProxy()
    for proxy in proxy_list:
        r = requests.get(url, proxy)
        return r.text


def getPrice(html, name_coin):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find("tbody").find_all("tr")
    for tr in trs:
        name = tr.find("td", class_="no-wrap currency-name").text.split('\n')[4]
        if name == name_coin:
            price = tr.find_all("td")[4].text.split('\n')[1]
            return price


def getData(name_coin):
    """ Функция возвращает цену name_coin"""
    url = 'https://coinmarketcap.com/all/views/all/'
    html = getHtml(url)
    price = getPrice(html, name_coin)
    return price



