#-*-coding:utf-8-*-
from flask import Flask, request, jsonify
from flask import Blueprint,render_template,send_file
import json
import base64
from mod_user import usermodel
from mod_commodity import commodity
from datetime import timedelta
import os
import pymysql
import numpy as np
from flask import send_file,session
# from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key='607ya'


dict_status=["生产商","运输商","仓库管理员","经销商","客户"]
@app.route('/')
def test():
    return '服务器正常运行'

#此方法处理用户注册
@app.route('/register', methods=['POST','GET'])
def register(): 
    if request.method == 'GET':       
        return render_template('register.html')
    else:
        datas = request.get_data()
        datas = json.loads(datas)
        register = usermodel.register(datas[0])
        return jsonify(register)


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        datas = request.get_data()
        datas = json.loads(datas)
        status = datas[0]['status']
        email = datas[0]['email']
        password = datas[0]['password']
        login = usermodel.login(int(status),email,password)
        print(login)
        if(login["login"]==0):
            session.permanent=True
            app.permanent_session_lifetime = timedelta(minutes=10)
            session['email']=email
            session['status']=status
        return jsonify(login)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success":0})

@app.route('/manufacturer', methods=['POST','GET'])
def manufacturer(): 
    if request.method == 'GET':     
        email = session.get('email')
        status = session.get('status')
        status = dict_status[int(status)-1] 
        return render_template('manufacturer/manufacturer.html',email=email,status=status)
    else:
        #点击加入区块链
        datas = request.get_data()
        print(datas)
        datas = json.loads(datas)
        item_num = datas[0]['item_num']
        session['item_num'] = item_num
        return jsonify({"success":0})

@app.route('/manufacturer_add_new', methods=['POST','GET'])
def manufacturer_add_new(): 
    if request.method == 'GET':      
        email = session.get('email')
        status = session.get('status') 
        status = dict_status[int(status)-1]
        print(email,status)
        return render_template('manufacturer/manufacturer_add_new.html',email=email,status=status)
    else:
        return "jsonify(data)"


@app.route('/save_manufacturer', methods=['POST','GET'])
def save_manufacturer():
    datas = request.get_data()
    data=json.loads(datas)
    print(data)
    result = commodity.insert_commodity(data[0])
    return jsonify({"success":result})

@app.route('/manufacturer_list', methods=['GET'])
def manufacturer_list():
    email = session.get('email')
    return jsonify(commodity.list_all_commodities(email))

@app.route('/manufacturer_select_warehouse_email', methods=['GET','POST'])
def manufacturer_select_warehouse_email():
    return jsonify(usermodel.select_warehouse())

@app.route('/manufacturer_add_blockchain', methods=['GET','POST'])
def manufacturer_add_blockchain():
    if request.method=='GET':
        email = session.get('email')
        item_num = session.get('item_num')
        status = session.get('status')
        status = dict_status[int(status)-1]
        return render_template('manufacturer/manufacturer_add_blockchain.html',email=email,item_num=item_num,status=status)
    else:
        datas = request.get_data()
        datas = json.loads(datas)
        result = commodity.add_into_block(datas[0])
        if result == 0:
            session.pop("item_num")
        return jsonify({"success":result})


@app.route('/manufacturer_delete_goods', methods=['POST'])
def manufacturer_delete_goods():
    datas = request.get_data()
    datas = json.loads(datas)
    result = commodity.delete_commodity(int(datas[0]['item_num']))
    return jsonify({"success":result})

@app.route('/manufacturer_edit_goods', methods=['POST','GET'])
def manufacturer_edit_goods():
    if request.method == 'GET':
        email = session['email']
        status = session['status']
        status = dict_status[int(status)-1]
        item_num = session['item_num']
        data = commodity.list_commoditiesByItemNum(int(item_num))
        trade_name = data['trade_name']
        attribute = data['attribute']
        number = data['number']
        production_data = data['production_data']
        expiration_data = data['expiration_data']
        manufacturer = data['manufacturer']
        production_address = data['production_address']
        trade_price = data['trade_price']
        commodity_status = data['commodity_status']
        manufacturer_email = data['manufacturer_email']
        session.pop('item_num')
        return render_template('manufacturer/manufacturer_edit_goods.html',
        email=email, status=status, item_num=item_num,trade_name=trade_name,attribute=attribute,\
            production_data=production_data,number=number,expiration_data=expiration_data,\
                manufacturer_email=manufacturer_email,production_address=production_address,\
                    manufacturer=manufacturer,commodity_status=commodity_status,trade_price=trade_price)
    else :
        datas = request.get_data()
        datas = json.loads(datas)
        session['item_num'] = int(datas[0]['item_num'])
        return jsonify({"success":0})

@app.route('/save_edit_manufacturer',methods=['POST','GET'])
def save_edit_manufacturer():
    datas = request.get_data()
    data=json.loads(datas)
    print(data)
    result = commodity.edit_commodity(data[0])
    return jsonify({"success":result})

#返回区块信息页面
@app.route('/manufacturer_showblock',methods=['POST','GET'])
def manufacturer_showblock():
    if request.method == 'GET':
        email = session.get('email')
        item_num = session.get('item_num')
        status = session.get('status')
        filename = 'qrcode/chain'+str(item_num) + 'block' + str(int(status))+'.png'
        status = dict_status[int(status)-1]
        return render_template('manufacturer/manufacturer_showblock.html',email=email,item_num=item_num,status=status,filename=filename)
    else :
        datas = request.get_data()
        datas = json.loads(datas)
        item_num = datas[0]['item_num']
        session["item_num"] = item_num
        return jsonify({"success":0}) 

#返回区块信息
@app.route('/manufacturer_goods_block',methods=['GET'])
def manufacturer_goods_block():
    item_num = session.get('item_num')
    status = session.get('status')
    print(item_num,status,item_num)
    result = commodity.show_block(int(item_num),int(status),int(item_num))
    print(result)
    return jsonify(result)


@app.route('/forwarder', methods=['POST','GET'])
def forwarder(): 
    if request.method == 'GET':       
        return render_template('forwarder/forwarder.html')
    else:
        return "1"

@app.route('/warehouse', methods=['POST','GET'])
def warehouse(): 
    if request.method == 'GET':       
        return render_template('warehouse/warehouse.html')
    else:
        return "1"

@app.route('/retailer', methods=['POST','GET'])
def retailer(): 
    if request.method == 'GET':       
        return render_template('retailer/retailer.html')
    else:
        return "1"

@app.route('/user', methods=['POST','GET'])
def user(): 
    if request.method == 'GET':       
        return render_template('user/user.html')
    else:
        return "1"



if __name__ == '__main__':
    # CORS(app, supports_credentials=True)
    app.run(debug=True,host='0.0.0.0',port=5000)
    
