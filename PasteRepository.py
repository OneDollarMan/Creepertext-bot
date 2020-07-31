import pymysql

class PasteRepository:

	def __init__(self, host, user, password, db, port, charset):
		self.connection = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset=charset)
		createTable()

	def createTable(self):
		with self.connection.cursor() as cursor:
			query = 'SHOW TABLES LIKE paste'
			cursor.execute(query)
			if cursor.fetchone() is None:
				query = "'"CREATE TABLE `paste` (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT, `title` text NOT NULL, `content` longtext NOT NULL, `rating` text NOT NULL, `source` text NOT NULL, `url` text NOT NULL, `popularity` text NOT NULL, PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4"'"
				cursor.execute(query)
				self.connection.commit()

	def isPasteExists(self, title):
		with self.connection.cursor() as cursor:
			query = 'SELECT * FROM paste WHERE title = "%s"'
			cursor.execute(query, title)
			return cursor.fetchone() is not None

	def savePaste(self, paste):
		with self.connection.cursor() as cursor:
			if not self.isPasteExists(paste['title']):
				query = 'INSERT INTO paste (title, content, rating, popularity, source, url) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(query, (paste['title'], paste['content'], paste['rating'], paste['popularity'], paste['source'], paste['url']))
				self.connection.commit()
				return True
			return False

	def getRandomPaste(self):
		with self.connection.cursor() as cursor:
			query = 'SELECT * FROM paste ORDER BY RAND() LIMIT 1'
			cursor.execute(query)
			return cursor.fetchone()