
import sqlite3 as sql
import hashlib


class Sqlite:

    __database = 'ufrpe_crud2.sqlite'       # 'private' static db file name

    def __init__(self):
        #   open or create database anew if db does not exist
        self.conn = sql.connect(self.__database)
        self.cursor = self.conn.cursor()
        #   check if table 'users' exists
        query = "SELECT NAME FROM 'sqlite_master' WHERE TYPE='table' AND NAME='users'"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row is None:
            # since table 'users' doesn't exist, we assume the database
            # doesn't exist either; so, let's create one
            self.__create_database()

    def login(self, username, password):
        # get md5 of user password
        pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        # check user credentials
        query = "SELECT * FROM 'users' WHERE login = '{}' AND md5 = '{}'".format(username, pwd)
        print("query = {}".format(query))
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        print("row = {}".format(row))
        return row

    def __create_database(self):

        #   create 'users' table
        query = '''CREATE TABLE 'users'
                   ('id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'login' VARCHAR(16) NOT NULL,
                    'md5' CHAR(32))
                '''
        self.cursor.execute(query)

        #   create classes table
        query = '''CREATE TABLE 'classes'
                   ('id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'code' CHAR(4),
                    'semester' CHAR(6),
                    'subject' CHAR(5))
                '''
        #   create subjects table
        query = '''CREATE TABLE 'subjects'
                    ('id' INTEGER PRIMARY KEY AUTOINCREMENT,
                     'code' CHAR(5)         NOT NULL,
                     'name' CHAR(30)        NOT NULL)
                '''
        self.cursor.execute(query)

        #   enter secret admin md5 hash, so that we have a first user to start with
        query = '''INSERT INTO users (login, md5) 
                   VALUES ('admin', 'f8d99de4eeefbe556a632cc6a5859898')
                '''
        self.cursor.execute(query)
        self.conn.commit()

    def __del__(self):
        self.conn.close()   # close connection to db right before object is destroyed










