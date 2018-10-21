#!C:/Python27
#coding=utf-8

import MySQLdb

# MySQL相关设置
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_passwd = 'pMy297451@'
mysql_port = '3306'
mysql_database = 'bbs'


def my_connect():
    """链接数据库"""
    
    global conn, cursor
    
    #print MySQLdb.version_info
    
    try:
        conn = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd,charset='utf8',autocommit=True, db=mysql_database)
        print u"\nMessage:Connect to MySQL successfully"
    except Exception:
        print(u"\nMessage:MySQL Connection failed")
        exit(20)
    cursor = conn.cursor()

def add(title, update_time):
    #add
    try:
        sql = "insert into post(post_title, last_updated_time) values(%s,%s)"
        print sql
        param = (title, update_time)
        my_connect()#打开链接
        cursor.execute(sql,param)
        cursor.close()
        conn.close()
    except StandardError as e:
        print "错误在这里》》》》》",e,"《《《《《错误在这里"
        #conn.rollback()

def update():
    #更新
    my_connect()
    sql = "update user set name='%s' where id='%d'" %("ken",15)
    print  sql
    try:
        cursor.execute(sql)
        cursor.close()
        conn.close()
    except StandardError as e:
        print "更新数据异常",e

def Select():
    #查询
    try:
        n = cursor.execute("SELECT t.id,t.post_title,t.last_updated_time,t.* from post t  ORDER BY t.id DESC LIMIT 10")
        data = cursor.fetchall()
        for row in data:
            #注意int类型需要使用str函数转义
            print ('id: ',row[0], '  title: ',row[1],' last updated time ',row[2])
        #提交事务
        cursor.close()#关闭游标
        conn.close()#释放数据库资源
    except  Exception :
        #异常情况下，进行事务回滚
        conn.rollback()
        print(u"\n操作失败,数据已回滚")

def delete():
    #删除
    my_connect()
    sql = "delete from post where title='%s'"%("tom1")
    #parama =("tom")
    cursor.execute(sql)
    cursor.close()
    conn.close()
