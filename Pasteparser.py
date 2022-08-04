# -*- coding: utf-8 -*-
import os.path
from threading import Thread
from time import sleep

import requests
from bs4 import BeautifulSoup
from parse import *

from Repo import Repo


class Pasteparser(Thread):

    def __init__(self):
        super().__init__()
        self.token = os.environ['TELEGRAPH_TOKEN']
        self.repo = Repo(os.environ['DATABASE_URL'])
        self.api_url = 'https://api.telegra.ph/'
        self.mrakopedia_url = 'https://mrakopedia.net/wiki/Служебная:Случайная_страница'
        self.source = None

    def get_paste(self):
        html = self.get_html(self.mrakopedia_url)
        if html is None:
            return None
        paste = self.parse_paste_from_html(html)
        if paste is not None and self.repo.is_paste_exists(paste['title']) is False:
            url = self.load_to_telegraph(paste)
            if url is not None:
                paste['url'] = url
                return paste

    def get_html(self, url):
        try:
            resp = requests.get(url, timeout=30)
        except requests.ConnectionError as e:
            print('хуйня:', e)
            return None
        self.source = resp.url
        return BeautifulSoup(resp.text, features="html.parser")

    def parse_paste_from_html(self, html):
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
                        'source': self.source}

    def load_to_telegraph(self, paste):
        method = 'createPage'
        params = {"access_token": self.token,
                  "title": paste['title'],
                  "author_name": 'Mrakopedia',
                  "author_url": paste['source'],
                  "content": '["{}"]'.format(paste['content'].rstrip()),
                  }
        resp = requests.post(self.api_url + method, data=params, timeout=60)
        res = resp.json()
        if res['ok'] is True:
            return res['result']['url']
        elif res['error'] == 'CONTENT_TEXT_REQUIRED':
            print('poeli govna...')
        elif res['error'][:5] == 'FLOOD':
            secs = res['error'][-4:]
            print('waiting for', secs)
            sleep(int(secs))

    def run(self):
        print('parser started')
        while True:
            paste = self.get_paste()
            if paste is not None:
                if self.repo.save_paste(paste) is True:
                    print('saved ' + paste['title'])
                    sleep(36)
