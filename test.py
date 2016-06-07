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
    names_dist = list(set(get_name_list()))
    return names_dist     # 返回名称不重复的公司名称，返回值类型为list

jieba.load_userdict('dic.txt')
lsts = get_name_list()
for i in lsts:
    seg_list = jieba.cut(i, cut_all=False)
    print '/'.join(list(seg_list))
