# -*- coding: utf-8 -*-
import requests
from PostgresqlRepo import *
import configparser
import os.path


class TelegramBot:

    def __init__(self, token):
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.get_result = None

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        self.get_result = resp.json()['result']

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        if len(self.get_result) > 0:
            return self.get_result[-1]

    def send_paste(self, chat_id, paste):
        self.send_message(chat_id=chat_id, text=paste[1] + ' \n' + paste[3])


def main():
    c = configparser.ConfigParser()
    if os.path.isfile('./configuration.mine.ini'):
        c.read('configuration.mine.ini')
        bot = TelegramBot(c['telegram']['telegram_token'])
        paste_repo = PostgresqlRepo(host=c['db']['host'],
                                    user=c['db']['user'],
                                    password=c['db']['password'],
                                    db=c['db']['db'],
                                    port=c['db']['port'])
    else:
        bot = TelegramBot(os.environ['TELEGRAM_TOKEN'])
        paste_repo = PostgresqlRepo(os.environ['DATABASE_URL'])

    startCommand = '/start'
    newPasteCommand = '/new'
    howmuchCommand = '/howmuch'
    startMessage = 'Здравствуйте! Это бот крипипаст. Чтобы получить пасту введите ' + newPasteCommand
    howmuchMessage = 'В базе {} крипипаст'
    new_offset = None
    print('bot started')

    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()

        if last_update is not None and 'message' in last_update:
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            if 'username' in last_update['message']['from']:
                username = last_update['message']['from']['username']
            else:
                username = str(last_update['message']['from']['id'])

            if last_chat_text.lower() == startCommand:
                paste_repo.save_user(username=username)
                bot.send_message(last_chat_id, startMessage)

            elif last_chat_text.lower() == newPasteCommand:
                paste = paste_repo.get_random_paste()
                if paste is not None:
                    bot.send_paste(chat_id=last_chat_id, paste=paste)
                    paste_repo.save_user(username=username)
                    print('sent ' + paste[1] + ' to @' + username)
                else:
                    bot.send_message(chat_id=last_chat_id, text='Паст нет')

            elif last_chat_text.lower() == howmuchCommand:
                bot.send_message(last_chat_id, howmuchMessage.format(paste_repo.get_paste_count()))

            new_offset = last_update['update_id'] + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
