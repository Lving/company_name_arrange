# __author__ = "Administrator"
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import jieba


def get_name_list():
    conn = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset="utf8")
    cur = conn.cursor()
    cur.execute('select user_company from kw_user')
    company_names = cur.fetchall()
    names = [name[0] for name in company_names if name[0] not in [None, '', ' ']]
    names_dist = list(names)
    conn.close()
    return names_dist  # 返回公司名称列表，返回值类型为list


def exclude_words():   # 将公司名称分为三部分，该函数返回值包含第三部分的所有关键词
    conn1 = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset="utf8")
    cur1 = conn1.cursor()
    cur1.execute('select key_word from dict')
    words = cur1.fetchall()
    exclusion = [word[0] for word in words]
    conn1.close()
    return exclusion   # 给列表包含‘公司’可能出现的所有表现形式

jieba.load_userdict('dic.txt')
lsts = list(set(get_name_list()))  # 公司名称去重
for i in lsts:
    seg_list = jieba.cut(i, cut_all=False)
    print '/'.join(list(seg_list))