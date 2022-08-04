# -*- coding: utf-8 -*-
import threading
from Controller import Controller
from Commands import Commands
from Repo import *
import os.path


class Bot(threading.Thread):

    def __init__(self):
        super(Bot, self).__init__()
        self.controller = Controller(os.environ['TELEGRAM_TOKEN'])
        self.repo = Repo(os.environ['DATABASE_URL'])
        self.commands = Commands(self.controller, self.repo)

        self.commands.start()
        self.commands.random()
        self.commands.count()
        self.commands.top()

        self.new_offset = None

    def run(self):
        print('bot started')
        while True:
            self.controller.get_updates(self.new_offset)
            last_update = self.controller.get_last_update()
            if last_update is not None:
                if 'message' in last_update:
                    user_command = last_update['message']['text'].lower()
                    self.commands.execute(user_command)
                    self.new_offset = last_update['update_id'] + 1
                else:
                    ...
