from bs4 import BeautifulSoup
import requests


def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text

