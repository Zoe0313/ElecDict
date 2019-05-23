"""
我写的
导入单词到数据库
"""

import pymysql
import re

# 创建连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='dict',
                     charset='utf8')

# 创建游标
cur = db.cursor()

#存储文件
with open("dict.txt",'rt') as fd:
    for line in fd:
        word = re.match(r'\S+', line).group()
        mean = line[len(word):].strip()
        try:
            sql = "insert into words (word,mean) values (%s,%s);"
            cur.execute(sql,[word,mean])
        except Exception as e:
            db.rollback()
            print(e)
    db.commit()

cur.close()
db.close()