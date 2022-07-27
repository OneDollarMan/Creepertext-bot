# -*- coding: utf-8 -*-
from time import sleep
import requests
from PostgresqlRepo import *
from parse import *
from bs4 import BeautifulSoup
import configparser
import os.path

c = configparser.ConfigParser()
if os.path.isfile('./configuration.mine.ini'):
    c.read('configuration.mine.ini')
    TOKEN = c['telegram']['telegraph_token']
    paste_repo = PostgresqlRepo(host=c['db']['host'],
                                user=c['db']['user'],
                                password=c['db']['password'],
                                db=c['db']['db'],
                                port=c['db']['port'])
else:
    TOKEN = os.environ['TELEGRAPH_TOKEN']
    paste_repo = os.environ['DATABASE_URL']
API_URL = 'https://api.telegra.ph/'


def get_paste():
    html = get_html('https://mrakopedia.net/wiki/Служебная:Случайная_страница')
    paste = parse_paste_from_html(html)
    if paste is not None:
        url = load_to_telegraph(paste)
        if url is not None:
            paste['url'] = url
            return paste


def get_html(url):
    resp = requests.get(url, timeout=30)
    global SOURCE
    SOURCE = resp.url
    return BeautifulSoup(resp.text, features="html.parser")


def parse_paste_from_html(html):
    title = html.h1
    content = html.find('div', id='mw-content-text')
    for a in content.find_all({'div', 'script'}):
        a.decompose()
    rating_raw = html.find('span', id='w4g_rb_area-1')
    if rating_raw is not None:
        rating = parse('Текущий рейтинг: {}/100 (На основе {} мнений)', rating_raw.text)
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
              "author_name": 'Mrakopedia',
              "author_url": paste['source'],
              "content": '["{}"]'.format(paste['content'].rstrip()),
              }
    resp = requests.post(API_URL + method, data=params, timeout=60)
    res = resp.json()
    print(res)
    if res['ok'] is True:
        return res['result']['url']
    elif res['error'] == 'CONTENT_TEXT_REQUIRED':
        print('poeli govna...')
    elif res['error'][:5] == 'FLOOD':
        secs = res['error'][-4:]
        print('waiting for', secs)
        sleep(int(secs))


def add_author_telegraph(paste):
    method = 'editPage'
    params = {"access_token": TOKEN,
              "title": paste[1],
              "content": '["{}"]'.format(paste[2]),
              "author_url": paste[4],
              "author_name": 'Mrakopedia'}
    url = parse('https://telegra.ph/{}', paste[5])
    resp = requests.post(API_URL + method + '/' + url[0], data=params, timeout=60)
    print(resp.url)
    print(resp.json())


def main():
    while True:
        paste = get_paste()
        if paste is not None:
            if paste_repo.save_paste(paste) is True:
                print('saved ' + paste['title'])
        sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
