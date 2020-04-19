import datetime
import pymysql
import qrcode
from flask import Flask, request, json, jsonify
from mode_manufacturer.blockchain import Blockchain

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

def connect_db():
    return pymysql.connect('localhost', 'root', 'root', 'blockchain')
    # return pymysql.connect('192.168.101.13','root','wsymz44','blockchain')

# 显示生产商已添加的商品信息
@app.route('/commoditylist',method=['GET'])
def list_all_commodities():
    datas=request.get_data()
    manufacturer_email=json.loads(datas)
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from manufacturer_info where manufacturer_email='%s'" % manufacturer_email
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['trade_name'] = item[0]
            data['attribute'] = item[1]
            data['number'] = item[2]
            data['production_data'] = item[3]
            data['expiration_data']=item[4]
            data['item_num'] = item[5]
            data['manufacturer'] = item[6]
            data['production_address'] = item[7]
            data['trade_price'] = item[8]
            data['commodity_status'] = item[9]
            data['manufacturer_email']=item[10]
            data_list.append(data)
        # db.commit()
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: insert erro")
    db.close()
    return jsonify(result)

# 根据货号查询商品
@app.route('/commoditylist/item_num',method=['GET'])
def list_commoditiesByItemNum(item_num):
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from manufacturer_info where item_num='%s'" % item_num
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['trade_name'] = item[0]
            data['attribute'] = item[1]
            data['number'] = item[2]
            data['production_data'] = item[3]
            data['expiration_data']=item[4]
            data['item_num'] = item[5]
            data['manufacturer'] = item[6]
            data['production_address'] = item[7]
            data['trade_price'] = item[8]
            data['commodity_status'] = item[9]
            data['manufacturer_email']=item[10]
            data_list.append(data)
        # db.commit()
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: insert erro")
    db.close()
    return jsonify(result)

#查询区块
@app.route('blocklist')
def list_blocks():
    return Blockchain.chain

# 增加商品
@app.route('/addCommodity',method=['POST'])
def insert_commodity():
    trade_name = request.form.get['trade_name']
    attribute = request.form.get['attribute']
    number = request.form.get['number']
    production_data = request.form.get['production_data']
    expiration_data=request.form.get['expiration_data']
    item_num = request.form.get['item_num']
    manufacturer = request.form.get['manufacturer']
    production_address = request.form.get['production_address']
    trade_price = request.form.get['trade_price']
    commodity_status = request.form.get['commodity_status']
    manufacturer_email=request.form.get['manufacturer_email']

    db = connect_db()
    cursor = db.cursor()
    flag="save failed!"
    sql = """insert into manufacturer_info(trade_name, attribute, number, production_data,expiration_data,item_num,
             manufacturer,production_address,trade_price,commodity_status,manufacturer_email)
             VALUES ('%s', '%s', '%d', '%s', '%s', '%s','%s', '%s', '%d', '%s','%s')
             """ % (trade_name, attribute, number, production_data, expiration_data, item_num, manufacturer,
                    production_address, trade_price, commodity_status,manufacturer_email)
    try:
        cursor.execute(sql)
        db.commit()
        flag="save success!"
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: insert err")
    db.close()
    # 生成条形码
    return jsonify(flag)

# 删除商品
@app.route('/delCommodity/item_num',method=['POST'])
def delete_commodity(item_num):
    db = connect_db()
    cursor = db.cursor()
    flag = "delete failed!"

    #判断是否已加入区块  又或者将已加入区块的商品的按钮设置为不可点击？
    sql = "select commodity_status from manufacturer_info where item_num='%s'"%item_num
    cursor.execute(sql)
    commodity_status = cursor.fetchall()
    if commodity_status:
        return jsonify(flag)

    sql = "delete from manufacturer_info where item_num='%s' " % item_num
    try:
        cursor.execute(sql)
        db.commit()
        flag="delete success!" #删除
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: delete erro")
    db.close()
    return jsonify(flag)

# 编辑商品
@app.route('/editCommodity/item_num',method=['POST'])
def edit_commodity(item_num):
    db = connect_db()
    cursor = db.cursor()
    # 判断是否加入区块链
    trade_name = request.form.get['trade_name']
    attribute = request.form.get['attribute']
    number = request.form.get['number']
    production_data = request.form.get['production_data']
    expiration_data = request.form.get['expiration_data']
    # item_num = request.form.get['item_num']
    manufacturer = request.form.get['manufacturer']
    production_address = request.form.get['production_address']
    trade_price = request.form.get['trade_price']
    commodity_status = request.form.get['commodity_status']
    manufacturer_email=request.form.get['manufacturer_email']

    flag="update failed!"
    sql = "update  manufacturer_info SET trade_name='%s',attribute='%s',number='%s'" \
          ",production_data='%s',expiration_data='%s', production_address='%s',manufacturer='%s'," \
          "trade_price='%s',commodity_status='%s', manufacturer_email='%s' where item_num='%s' " \
          % (trade_name, attribute, number, production_data, expiration_data,manufacturer, production_address,
             trade_price, commodity_status, manufacturer_email,item_num)
    try:
        cursor.execute(sql)
        db.commit()
        flag="update success!"
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: update erro")
    db.close()
    return jsonify(flag)

#加入区块链
@app.route('/addblock/item_num',method=['POST'])
def add_into_block(item_num):
    #填写表单
    warehouse_email = request.form.get['warehouse_email']
    manufacturer_email = request.form.get['manufacturer_email']
    # item_num = request.form.get['item_num']
    order_num = request.form.get['order_num']
    order_state = request.form.get['order_state']
    submit_data = request.form.get['submit_data']

    db = connect_db()
    cursor = db.cursor()
    sql = """insert into manufacturer_order_info(warehouse_email, manufacturer_email, item_num, order_num, 
            order_state, submit_data) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" \
            % (warehouse_email,manufacturer_email,item_num,order_num, order_state,submit_data)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()  # 如果发生错误则回滚

    #根据货号查询商品的生产日期、保质期、生产地址、产家邮箱
    sql = "select * from manufacturer_info where item_num='%s'" % item_num
    data = {}
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data['trade_name'] = item[0]
            data['attribute'] = item[1]
            data['number'] = item[2]
            data['production_data'] = item[3]
            data['expiration_data'] = item[4]
            data['item_num'] = item[5]
            data['manufacturer'] = item[6]
            data['production_address'] = item[7]
            data['trade_price'] = item[8]
            data['commodity_status'] = item[9]
            data['manufacturer_email'] = item[10]
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: check erro")

    #查询加入区块的商品个数==链数
    sql = "select COUNT(*) from manufacturer_order_info where commodity_status='1"
    num = cursor.execute(sql)
    print(num)
    num = num + 1
    sender = "manufacturer"
    tran_massage="{},{},{},{},{}".format(data['trade_name'],data['production_address'],data['manufacturer_email'],
                                     data['production_data'],data['expiration_data'])
    print(tran_massage)

    block_in_chain = Blockchain(num)
    print("blockchain is : " + block_in_chain)

    block_in_chain.new_transaction(sender,tran_massage)
    new_block = block_in_chain.new_block(0)
    block_in_chain.add_block(new_block,block_in_chain.proof_of_work(new_block))
    print("new_block is : " + new_block)

    #修改订单状态
    sql = "update manufacturer_order_info SET commodity_status='1' where item_num='%s'" % item_num
    try:
        cursor.execute(sql)
        db.commit()
        print("add block success")
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: update erro")
    db.close()

    i = 0
    qr_data = ''
    for blockdata in block_in_chain.chain:
        i += 1
        qr_data += 'block{}:{}'.format(i,blockdata['transactions'])

    img = qrcode.make(qr_data)
    img.save('/img/' + 'chain' + str(num) + 'block' + str(i) + '.png')

if __name__ == "__main__":

    app.run(host='127.0.0.1')
