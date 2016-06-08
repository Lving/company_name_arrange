# __author__ = "Administrator"
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import jieba


# f = open('dic.txt', 'r+')
# print f.readlines()


conn1 = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset="utf8")
cur1 = conn1.cursor()
cur1.execute('select key_word from dict')
words = cur1.fetchall()
exclusion = [word[0] for word in words]
for i in exclusion:
    print i
conn1.close()
