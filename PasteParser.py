from time import sleep
import requests
from PasteRepository import *
from parse import *
from bs4 import BeautifulSoup
import configparser

c = configparser.ConfigParser()
c.read('configuration.ini')
TOKEN = c['telegram']['telegraph_token']
API_URL = 'https://api.telegra.ph/'


def get():
    html = get_html('https://mrakopedia.net/wiki/Служебная:Случайная_страница')
    paste = parse_html(html)
    url = load_to_telegraph(paste)
    if url is not None:
        paste['url'] = url
        return paste


def get_html(url):
    resp = requests.get(url, timeout=30)
    global SOURCE
    SOURCE = resp.url
    return BeautifulSoup(resp.text, features="html.parser")


def parse_html(html):
    title = html.h1
    content = html.find('div', id='mw-content-text')
    for a in content.find_all({'div', 'script'}):
        a.decompose()

    rating = parse('Текущий рейтинг: {}/100 (На основе {} мнений)', html.find('span', id='w4g_rb_area-1').text)
    if title is not None and content is not None and rating is not None:
        return {'title': title.text,
                'content': content.text,
                'rating': rating[0],
                'popularity': rating[1],
                'source': SOURCE}


def load_to_telegraph(paste):
    method = 'createPage'
    params = {"access_token": TOKEN,
              "title": paste['title'],
              "content": '["{}"]'.format(paste['content']),
              "author_url": paste['source'],
              "author_name": 'Mrakopedia'}
    resp = requests.post(API_URL + method, data=params, timeout=60)
    print(resp.json())
    if resp.json()['ok'] is True:
        return resp.json()['result']['url']


def main():
    paste_repo = PasteRepository(host=c['db']['host'],
                                 user=c['db']['user'],
                                 password=c['db']['password'],
                                 db=c['db']['db'],
                                 port=c['db']['port'])

    while True:
        paste = get()
        if paste is not None:
            if paste_repo.savePaste(paste) is True:
                print('saved ' + paste['title'])

            sleep(10)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
