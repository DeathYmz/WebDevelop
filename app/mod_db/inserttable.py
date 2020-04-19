import pymysql
import datetime
import numpy as np
from flask import Flask, request, jsonify
opt = config.parse_opt()

def connect_db():
    return pymysql.connect(opt.ip,opt.sqlroot,opt.sqlpassword,opt.sqldatabase)

def insert_user_info(data):
    username = data['username']
    receive_address = data['receive_address']
    telephone = data['telephone']
    password = data['password']
    email = data['email']
    status = data['status']

    db = connect_db()
    cursor = db.cursor()
    sql = """insert into user_info(username, receive_address, telephone, password, email, status)
         VALUES ('%s', '%s', '%s', '%s','%s', '%d')""" % (username, receive_address, telephone, password, email, status)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback() # 如果发生错误则回滚
        print("Error: insert erro")
    db.close()



def list_all():
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from user_info "
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['username'] = item[0]
            data['receive_address'] = item[1]
            data['telephone'] = item[2]
            data['password'] = item[3]
            data['email'] = item[4]
            data['status'] = item[5]
            data_list.append(data)
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: insert erro")
    db.close()
    return data_list

# if __name__ == "__main__":
#     # data = {}
#     # data['username'] = 'test'
#     # data['receive_address'] = 'test'
#     # data['telephone'] = 'test'
#     # data['password'] = 'test'
#     # data['email'] = 'test'
#     # data['status'] = 1
#     # insert_user_info(data)
#     print(list_all())

