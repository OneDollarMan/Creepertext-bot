import messages


# decorator with arg for command assignment
# all functions with this decorator are being stored in dict and then executed by call from bot thread
def command(command):
    def decorator(func):
        def wrapped(self):
            self.commands[command] = func
            return func

        return wrapped

    return decorator


class Commands:

    def __init__(self, controller, repo):
        self.commands = {}
        self.controller = controller
        self.repo = repo

    def execute(self, com):
        if com in self.commands:
            self.commands[com](self)

    @command('/start')
    def start(self):
        self.repo.save_user(username=self.controller.username)
        self.controller.send_message(self.controller.id, messages.start_message)

    @command('/random')
    def random(self):
        paste = self.repo.get_random_paste()
        if paste is not None:
            self.controller.send_message(self.controller.id, '[{}]({})'.format(paste[1], paste[3]), 'markdown')
            self.repo.save_user(self.controller.username)
            print('sent ' + paste[1] + ' to @' + self.controller.username)
        else:
            self.controller.send_message(self.controller.id, 'Паст нет')

    @command('/count')
    def count(self):
        self.controller.send_message(self.controller.id, messages.count_message.format(self.repo.get_paste_count()))

    @command('/top')
    def top(self):
        top_ten = self.repo.get_top()
        res = ''
        for i in range(len(top_ten)):
            res += '[{}. {}]({}) - {}\n'.format(i + 1, top_ten[i][1], top_ten[i][3], top_ten[i][2])
        self.controller.send_message_with_keyboard(self.controller.id, res, 'markdown',
                                                   {'inline_keyboard':
                                                        [[{'text': 'Назад', 'callback_data': '1'},
                                                          {'text': 'Вперед', 'callback_data': '2'}]]
                                                    })
