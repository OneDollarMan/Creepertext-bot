import requests  
from PasteRepository import *


class TelegramBot:

	def __init__(self, token, messageLength):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)
		self.messageLength = messageLength

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

	def send_paste(self, chat_id, paste, username):
		print('sent ' + paste[1] + ' to @' + username)
		self.send_message(chat_id = chat_id, text = paste[1] + ' \n' + paste[5])


def main():

	token = '1392358861:AAFI0wi2OBxT3dpdKZa-CL_koafqiUpiwi4'
	bot = TelegramBot(token, 4096)
	pasteRepo = PasteRepository('localhost', 'root', 'gmfk2ASD', 'Pastes', 3306, 'utf8mb4')

	startCommand = '/start'
	newPasteCommand = '/new'
	startMessage = 'Здравствуйте! Это бот крипипаст. Чтобы получить пасту введите ' + newPasteCommand
	new_offset = None

	while True:
		bot.get_updates(new_offset)
		last_update = bot.get_last_update()

		if last_update is not None:

			last_update_id = last_update['update_id']
			last_chat_text = last_update['message']['text']
			last_chat_id = last_update['message']['chat']['id']

			if last_chat_text.lower() == startCommand:
				bot.send_message(last_chat_id, startMessage)

			elif last_chat_text.lower() == newPasteCommand:
				bot.send_paste(chat_id = last_chat_id, paste = pasteRepo.getRandomPaste(), username = last_update['message']['from']['username'])

			new_offset = last_update_id + 1


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()