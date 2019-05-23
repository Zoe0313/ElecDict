"""
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

sql = 'insert into words (word,mean) \
          VALUES (%s,%s)'
f = open("dict.txt",'rt')
for line in f:
    # 获取匹配
    tup = re.findall(r'(\w+)\s+(.*)',line)[0]
    try:
        cur.execute(sql,tup)
        db.commit()
    except Exception as e:
        db.rollback()
        print("Failed:",e)

f.close()
cur.close()
db.close()

