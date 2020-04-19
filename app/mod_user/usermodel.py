import pymysql
import datetime
from flask import Flask, request, jsonify
import config
opt =config.parse_opt()

def connect_db():
    return pymysql.connect(opt.ip,opt.sqlroot,opt.sqlpassword,opt.sqldatabase)
def register(data):
    db = connect_db()
    cursor = db.cursor()
    status = data['status']
    email = data['email']
    redata = {}
    sql = "select * from user_info where status=%d and email='%s'" % (int(status),email)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            redata['register'] = 1 #(0注册成功，1账户已注册）
        else :
            insert_user_info(data)
            redata['register'] = 0
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: unable to fetch data")
    db.close()
    return redata

def login(status,email,password):
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from user_info where status='%d'" % status
    data = {} #login= int (0 登陆成功，1账户不存在，2密码错误)
    data['login'] = 1
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            sql_password = item[2]
            sql_email = item[3]
            if sql_email == email and sql_password == password:
               data['login'] = 0
               data['username'] = item[0]
               data['status'] = status
               data['register'] = 1
               break
            elif sql_email == email:
                data['login'] = 2  
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: unable to fetch data")
    db.close()
    return data

def insert_user_info(data):
    username = data['username']
    telephone = data['telephone']
    password = data['password']
    email = data['email']
    status = data['status']
    register_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = connect_db()
    cursor = db.cursor()
    sql = """insert into user_info(username, telephone, password, email, status, register_data)
         VALUES ('%s', '%s', '%s', '%s','%d', '%s')""" % (username, telephone, password, email, int(status), register_data)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback() # 如果发生错误则回滚
        print("Error: insert erro")
    db.close()

def select_warehouse():
    db = connect_db()
    cursor = db.cursor()
    sql = "select email from user_info where status= 3 "
    datas = [] #login= int (0 登陆成功，1账户不存在，2密码错误)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['email'] = item[0]
            datas.append(data)
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: unable to fetch data")
    db.close()
    return datas

# if __name__ == "__main__":
    # data = {}
    # data['username'] = 'test'
    # data['telephone'] = 'test'
    # data['password'] = 'test'
    # data['email'] = 'test'
    # data['status'] = 2
    # d = register(data)
    # print(d)
    # data = login(1,'test','test')
    # print(select_warehouse())