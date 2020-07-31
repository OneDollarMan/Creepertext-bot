import requests
from PasteRepository import *
from parse import *
from urllib.parse import quote
from bs4 import BeautifulSoup


class PasteParser:

	def __init__(self, token):
		self.token = token
		self.api_url = 'https://api.telegra.ph/'

	def getPaste(self):
		resp = requests.get('https://mrakopedia.net/wiki/Служебная:Случайная_страница', timeout=30)
		soup = BeautifulSoup(resp.text, features="html.parser")
		title = soup.h1
		content = soup.find('div', id = 'mw-content-text')
		for div in content.find_all({'div', 'script'}):
			div.decompose()

		rating = soup.find('span', id = 'w4g_rb_area-1')
		if title is not None and content is not None and rating is not None:
			method = 'createPage'
			params = {"access_token": self.token, "title": title.text, "content": '["{}"]'.format(content.text), "author_url": resp.url, "author_name": 'Mrakopedia'}
			resp2 = requests.post(self.api_url + method, data = params, timeout = 60)
			print(resp2.json())
			if resp2.json()['ok'] is True:
				ratingint = parse('Текущий рейтинг: {}/100 (На основе {} мнений)', rating.text)
				return {'title': title.text, 'content': content.text, 'rating': ratingint[0], 'popularity': ratingint[1],'source': resp.url, 'url': resp2.json()['result']['url']}


def main():
	telegraph_token = '11cfcc993a67db3565657e5c4c4b0fd1f265604f2d384fdae584641ea13a'
	pasteParser = PasteParser(telegraph_token)
	pasteRepo = PasteRepository('localhost', 'root', 'gmfk2ASD', 'Pastes', 3306, 'utf8mb4')

	while True:
		paste = pasteParser.getPaste()
		if paste is not None:
			if pasteRepo.savePaste(paste) is True:
				print('saved ' + paste['title'])


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()