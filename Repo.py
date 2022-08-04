# -*- coding: utf-8 -*-
import psycopg2


class Repo:

    def __init__(self, url=None, host=None, user=None, password=None, db=None, port=None):
        self.url = url
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        if self.url is not None:
            self.connection = psycopg2.connect(self.url)
        else:
            self.connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.db,
                                               port=self.port)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        query = """CREATE TABLE IF NOT EXISTS paste (
                                    id serial PRIMARY KEY,
                                    title varchar(100) UNIQUE NOT NULL,
                                    rating varchar(100) NOT NULL,
                                    url varchar(100) UNIQUE NOT NULL,
                                    popularity varchar(100) NOT NULL
                                    );"""
        self.cursor.execute(query)
        self.connection.commit()

        query = """CREATE TABLE IF NOT EXISTS fbi (
                                            id serial PRIMARY KEY,
                                            username varchar(100) UNIQUE NOT NULL,
                                            count integer NOT NULL,
                                            last_read timestamp NOT NULL
                                            );"""
        self.cursor.execute(query)
        self.connection.commit()

    def is_paste_exists(self, title):
        query = 'SELECT * FROM paste WHERE title = %s'
        self.cursor.execute(query, (title,))
        return self.cursor.fetchone() is not None

    def save_paste(self, paste):
        query = 'INSERT INTO paste (title, rating, popularity, url) VALUES (%s, %s, %s, %s)'
        self.cursor.execute(query, (paste['title'], paste['rating'], paste['popularity'], paste['url']))
        self.connection.commit()
        return True

    def get_random_paste(self):
        query = 'SELECT * FROM paste ORDER BY random() LIMIT 1'
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_paste_count(self):
        query = 'SELECT COUNT(*) FROM paste'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_all(self):
        query = 'SELECT * FROM paste'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_top(self):
        query = 'SELECT * FROM paste ORDER BY Rating DESC LIMIT 10'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def save_user(self, username):
        query = 'SELECT * FROM fbi WHERE username=%s'
        self.cursor.execute(query, (username,))
        res = self.cursor.fetchone()
        if res is None:
            query = 'INSERT INTO fbi (username, count, last_read) VALUES (%s, 0, CURRENT_TIMESTAMP)'
            self.cursor.execute(query, (username,))
            self.connection.commit()
        else:
            query = 'UPDATE fbi SET count = count + 1, last_read = CURRENT_TIMESTAMP WHERE username = %s'
            self.cursor.execute(query, (username,))
            self.connection.commit()

    def get_saved_users(self):
        query = 'SELECT * FROM fbi'
        self.cursor.execute(query)
        return self.cursor.fetchall()
