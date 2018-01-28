# -*- coding: utf-8 -*-
import sqlite3

class SQLighter:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM user').fetchall()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM user WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM user').fetchall()
            return len(result)    

    def close(self):
        self.connection.close()    