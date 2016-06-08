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
    return exclusion   # 给列表包含‘有限公司’可能出现的所有表现形式


def clean_list():  # 取出公司中间部分关键词
    # 公司开头地域部分列表，需要完善
    region = [u'广东',u'广东省',u'广州', u'广州市', u'东莞市', u'东莞', u'深圳市', u'深圳', u'上海', u'佛山',u'佛山市',u'中山',u'中山市',u'珠海',u'珠海市'\
        , u'惠州',u'惠州市',u'无锡市',u'义乌市',u'顺德',u'顺德区',u'江门',u'江门市',u'潮州',u'潮州市',u'浙江',u'北京',u'上海',u'厦门',\
              u'山东',u'茂名',u'浙江省']
    #print region
    jieba.load_userdict('dic.txt')
    exclu_words = exclude_words()
    coname_lsts = get_name_list()
    key_name = []
    for coname in coname_lsts:
        seg_coname = list(jieba.cut(coname, cut_all=False))
        print '/'.join(seg_coname)
        exclu = [seg for seg in seg_coname if (seg not in exclu_words and seg not in region)]
        print ''.join(exclu)
        key_name.append(''.join(exclu))
    return key_name
