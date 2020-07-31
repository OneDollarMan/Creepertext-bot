import pymysql

class PasteRepository:

	def __init__(self, host, user, password, db, port, charset):
		self.host=host
		self.user=user
		self.password=password
		self.db=db
		self.port=port
		self.charset=charset
		self.connect()

	def connect(self):
		self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, charset=self.charset)

	def getCursor(self):
		if not self.connection.open:
			self.connect()
		try:
			self.connection.cursor().execute('SELECT 1')
		except pymysql.err.OperationalError:
			self.connect()
		return self.connection.cursor()

	def isPasteExists(self, title):
		with self.getCursor() as cursor:
			query = 'SELECT * FROM paste WHERE title = "%s"'
			cursor.execute(query, title)
			return cursor.fetchone() is not None

	def savePaste(self, paste):
		with self.getCursor() as cursor:
			if not self.isPasteExists(paste['title']):
				query = 'INSERT INTO paste (title, content, rating, popularity, source, url) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(query, (paste['title'], paste['content'], paste['rating'], paste['popularity'], paste['source'], paste['url']))
				self.connection.commit()
				return True
			return False

	def getRandomPaste(self):
		with self.getCursor() as cursor:
			query = 'SELECT * FROM paste ORDER BY RAND() LIMIT 1'
			cursor.execute(query)
			return cursor.fetchone()

	def getPasteCount(self):
		with self.getCursor() as cursor:
			query = 'SELECT COUNT(*) FROM paste'
			cursor.execute(query)
			return cursor.fetchone()