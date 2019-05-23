# 电子词典思路分析

### 1. 确定技术

> 通信 tcp通信

> 并发 多进程并发

> 数据库 mysql
    
### 2. 确定数据库

> 建立几个表

> 每个表作用和存储内容

> 步骤：
* 建表

`create database dict charset=utf8;`

    * 用户表 id name passwd
        `create table user (id int primary key auto_increment,name varchar(32) not null,passwd varchar(128) not null);`

    * 历史记录 id name word time
        `create table history (id int primary key auto_increment,name varchar(32) not null,word varchar(32) not null,time varchar(64) not null);`
        
    * 单词表 id word mean
        编写程序将单词本存入到数据库
        `create table words (id int primary key auto_increment,word varchar(32),mean text);`

* 编写程序将单词本存入到数据库

    `运行insert_word.py`
    
### 3. 结构设计

> 客户端

> 服务端（处理数据）
    
### 4. 功能分析

> 客户端和服务端分别需要实现哪些功能

* 网络模型
* 登录
    * 客户端
        1. 输入用户名、密码
        2. 发送请求
        3. 得到回复
       
    * 服务端
        1. 接收请求
        2. 判断是否允许登录
        3. 反馈结果
* 注册
    
    * 客户端
        1. 输入注册信息
        2. 将信息发送给服务器
        3. 等待反馈
    
    * 服务端
        1. 接收注册信息
        2. 验证用户是否存在
        3. 插入数据库
        4. 将信息反馈给客户端
* 查单词
* 历史记录

### 5.协议指定
* R name passwd 注册请求字段

    cookie: import getpass
    passwd = getpass.getpass("secret:")
    功能：隐藏输入的内容
    返回值：输入的内容字符串
    
    cookie: 数据库 passwd的字段加密
    
        import hashlib
        passwd = 'abc123'
        hash = hashlib.md5() #经过md5算法生成hash对象
        hash.update(passwd.encode()) #passwd是密码的明文字节串
        hash.hexdigest() #取返回值存入到数据库
        生成'e99a18c428cb38d5f260853678922e03'
    
    cookie：加盐
    
    方法一:
    
        passwd = 'abc123'
        passwd = passwd+'awk#%&'# 加盐处理
        hash=hashlib.update(passwd.encode())
        hash.hexdigest()
        生成'fbda237579e9e018587702daf3e90982'
        
    方法二:
    
        passwd = 'abc123'
        hash = hashlib.md5((name+'the-salt').encode())# 加盐处理
        hash.update(passwd.encode())
        hash.hexdigest()