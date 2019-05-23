"""
dict项目用于处理数据
"""

import pymysql
import hashlib

# 编写功能类 提供给服务端使用
class Database:
    def __init__(self,
                 host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 database='dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db() #连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)
    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    # 注册账户验证
    def register(self,name,passwd):
        sql = "select * from user where name='%s'"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:# 如果查询到用户名，说明用户名已存在
            return False

        #加密处理
        hash = hashlib.md5((name+'the-salt').encode())
        hash.update(passwd.encode())

        sql = "insert into user (name,passwd) values (%s,%s);"
        try:
            self.cur.execute(sql,[name,hash.hexdigest()])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print("Failed:",e)
            return False