import pymysql

class PasteRepository:

	def __init__(self, host, user, password, db, port, charset):
		self.host=host
		self.user=user
		self.password=password
		self.db=db
		self.port=port
		self.charset=charset
		connect()

	def connect(self):
		self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, charset=self.charset)

	def isPasteExists(self, title):
		if self.connection.open is not True:
			self.connect()
		with self.connection.cursor() as cursor:
			query = 'SELECT * FROM paste WHERE title = "%s"'
			cursor.execute(query, title)
			return cursor.fetchone() is not None

	def savePaste(self, paste):
		if self.connection.open is not True:
			self.connect()
		with self.connection.cursor() as cursor:
			if not self.isPasteExists(paste['title']):
				query = 'INSERT INTO paste (title, content, rating, popularity, source, url) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(query, (paste['title'], paste['content'], paste['rating'], paste['popularity'], paste['source'], paste['url']))
				self.connection.commit()
				return True
			return False

	def getRandomPaste(self):
		if self.connection.open is not True:
			self.connect()
		with self.connection.cursor() as cursor:
			query = 'SELECT * FROM paste ORDER BY RAND() LIMIT 1'
			cursor.execute(query)
			return cursor.fetchone()