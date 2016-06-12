# __author__ = "Administrator"
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def get_name_list():
    conn = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset="utf8")
    cur = conn.cursor()
    cur.execute('select user_company from kw_user')
    company_names = cur.fetchall()
    names = [name[0].strip() for name in company_names if name[0] not in [None, '', ' ']]
    #names_dist = list(names)
    conn.close()
    return names  # 返回公司名称列表，返回值类型为list


def seg_company_name():  # 将每个公司名称进行拆分
    co_name = []
    jieba.load_userdict('dic.txt')
    temp1 = get_name_list()
    for lst in temp1:
        seg_coname = list(jieba.cut(lst, cut_all=False))
        co_name.append(seg_coname)
    return co_name


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
    region = [u'广东',u'广东省', u'广州', u'广州市', u'东莞市', u'东莞', u'深圳市', u'深圳', u'宝安区',u'上海', u'佛山',u'佛山市',u'中山',u'中山市',u'珠海',u'珠海市'\
        , u'惠州', u'惠州市', u'无锡市', u'义乌市', u'顺德', u'顺德区', u'江门', u'江门市',u'潮州',u'潮州市',u'浙江', u'北京', u'上海', u'厦门',\
              u'山东', u'茂名', u'浙江省', u'天津',u'青岛', u'哈尔滨', u'南宁', u'苍南县', u'龙港', u'南海区',u'高埗',u'南海'\
              ,u'湖南', u'廊坊市', u'杭州']
    #print region
    jieba.load_userdict('dic.txt')
    exclu_words = exclude_words()
    coname_lsts = get_name_list()
    key_name_temp = []  # 未去重列表
    for coname in coname_lsts:
        seg_coname = list(jieba.cut(coname, cut_all=False))
        #print '/'.join(seg_coname)
        exclu = [seg for seg in seg_coname if (seg not in exclu_words and seg not in region)]
        #print ''.join(exclu)
        #key_name.append(exclu)
        key_name_temp.append(''.join(exclu))
    #temp_list = list(set(key_name_temp))   # 对列表去重， 然后再次分词
    # key_name = list(jieba.cut(temp_list, cut_all=False))  # 再次分词
    return key_name_temp # 返回嵌套表，公司名称关键词


def duplication():  # 对clean_list 的返回列表进行去重后并再次分词
    jieba.load_userdict('dic.txt')
    dup_key = []
    raw_key = list(set(clean_list()))   # 去重
    for temp in raw_key:
        temp1 = list(jieba.cut(temp, cut_all=False))
        new_temp = [i for i in temp1 if i != [' ', ')']]  # 删除分词后的空格
        dup_key.append(new_temp)
       # print '/'.join(temp1)

    # new_dup_key = [i for i in dup_key if i != ' ']  # delete space ' '
    return dup_key


# print duplication()

# def isinclude(list1, list2):  # 判断list1和list2是否有相同的元素
#     if len(set(list1) & set(list2)) == len(list1):
#         return True
#     else:
#         return False
#
co_names = seg_company_name()  # 公司名称
co_key_names = duplication()   # 公司名称关键词列表
f = open('name.txt', 'w')
#seg = ''
for co_key in co_key_names:
    for co_name in co_names:
        if set(co_key).issubset(set(co_name)) and len(set(co_key) & set(co_name)) >= 1:
            key_name = ''.join(co_key)
            company_name = ''.join(co_name)
            f.write(key_name)
            f.write(',')
            f.write(company_name)
            f.write('\n')


            #print '/'.join(co_key), '|', '/'.join(co_name)
f.close()

