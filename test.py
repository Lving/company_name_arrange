# __author__ = "Administrator"
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import jieba


# f = open('dic.txt', 'r+')
# print f.readlines()

conn = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset="utf8")
cur = conn.cursor()
cur.execute('select key_word from dict')
words = cur.fetchall()
for word in words:
    print word[0]