import json

import requests


class Controller:

    def __init__(self, token):
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.get_result = None

        self.id = None
        self.username = None

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        self.get_result = resp.json()['result']

    def send_message(self, chat_id, text, parse_mode=None):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        if len(self.get_result) > 0:
            last_update = self.get_result[-1]
            if 'message' in last_update:
                self.id = last_update['message']['chat']['id']
                if 'username' in last_update['message']['from']:
                    self.username = last_update['message']['from']['username']
                else:
                    self.username = str(last_update['message']['from']['id'])
                return last_update

    def send_message_with_keyboard(self, chat_id, text, parse_mode, reply_markup):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode, 'reply_markup': json.dumps(reply_markup), 'disable_web_page_preview': True}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
