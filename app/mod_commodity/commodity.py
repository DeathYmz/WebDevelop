import datetime
import pymysql
import qrcode
from flask import Flask, request, json, jsonify
from mod_commodity.blockchain import Blockchain
import os
import config
opt =config.parse_opt()

def connect_db():
    return pymysql.connect(opt.ip,opt.sqlroot,opt.sqlpassword,opt.sqldatabase)
    

# 显示生产商已添加的商品信息
# @app.route('/commoditylist',method=['GET'])
def list_all_commodities(manufacturer_email):
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
    return data_list

# 根据货号查询商品
# @app.route('/commoditylist/item_num',method=['GET'])
def list_commoditiesByItemNum(item_num):
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from manufacturer_info where item_num='%d'" % item_num
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
    return data

#查询区块
# @app.route('blocklist')
def list_blocks():
    return Blockchain.chain

# 增加商品
# @app.route('/addCommodity',method=['POST'])
def insert_commodity(data):
    trade_name = data['trade_name']
    attribute = data['attribute']
    number = data['number']
    production_data = data['production_data']
    expiration_data= data['expiration_data']
    manufacturer = data['manufacturer']
    production_address = data['production_address']
    trade_price = data['trade_price']
    commodity_status = data['commodity_status']
    manufacturer_email = data['manufacturer_email']

    db = connect_db()
    cursor = db.cursor()
    flag = 1
    sql = """insert into manufacturer_info(trade_name, attribute, number, production_data,expiration_data,
             manufacturer,production_address,trade_price,commodity_status,manufacturer_email)
             VALUES ('%s', '%s', '%d', '%s', '%d', '%s', '%s', '%d', '%s','%s')
             """ % (trade_name, attribute, int(number), production_data, int(expiration_data), manufacturer,
                    production_address, int(trade_price), commodity_status,manufacturer_email)
    try:
        cursor.execute(sql)
        db.commit()
        flag=0
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: insert err")
    db.close()
    # 生成条形码
    return flag

# 删除商品
# @app.route('/delCommodity/item_num',method=['POST'])
def delete_commodity(item_num):
    db = connect_db()
    cursor = db.cursor()
    flag = 1
    sql = "delete from manufacturer_info where item_num='%d' " % item_num
    try:
        cursor.execute(sql)
        db.commit()
        flag= 0 #删除成果
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: delete erro")
    db.close()
    return flag

# 编辑商品
# @app.route('/editCommodity/item_num',method=['POST'])
def edit_commodity(data):
    db = connect_db()
    cursor = db.cursor()
    # 判断是否加入区块链
    trade_name = data['trade_name']
    attribute = data['attribute']
    number = data['number']
    production_data = data['production_data']
    expiration_data = data['expiration_data']
    item_num = data['item_num']
    manufacturer = data['manufacturer']
    production_address = data['production_address']
    trade_price = data['trade_price']
    commodity_status = data['commodity_status']
    manufacturer_email = data['manufacturer_email']

    flag=1
    sql = "update  manufacturer_info SET trade_name='%s',attribute='%s',number='%d'" \
          ",production_data='%s',expiration_data='%d', production_address='%s',manufacturer='%s'," \
          "trade_price='%s',commodity_status='%d', manufacturer_email='%s' where item_num='%d' " \
          % (trade_name, attribute, int(number), production_data, int(expiration_data),manufacturer, production_address,
             trade_price, int(commodity_status), manufacturer_email, int(item_num))
    try:
        cursor.execute(sql)
        db.commit()
        flag=0
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: update erro")
    db.close()
    return flag


#加入区块链
# @app.route('/addblock/item_num',method=['POST'])
def add_into_block(datas):
    #填写表单
    # datas = {}
    # datas['warehouse_email'] = "ltt@qq.com"
    # datas['manufacturer_email'] = 'xjl@qq.com'
    # datas['order_num'] = "111"
    # datas['order_state'] = 0
    warehouse_email = datas['warehouse_email']
    manufacturer_email = datas['manufacturer_email']
    item_num = datas['item_num']
    item_num = int(item_num)
    order_state = datas['order_state']
    order_state = int(order_state)
    submit_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #仓库下单
    db = connect_db()
    cursor = db.cursor()
    sql = """insert into manufacturer_order_info(warehouse_email, manufacturer_email, item_num,
            order_state, submit_data) VALUES ('%s', '%s', '%d', '%d', '%s')""" \
            % (warehouse_email,manufacturer_email, item_num, order_state,submit_data)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()  # 如果发生错误则回滚

    #修改商品状态：已加入区块链
    sql = "update manufacturer_info SET commodity_status='1' where item_num='%d'" % item_num
    try:
        cursor.execute(sql)
        db.commit()
        print("add block success")
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: update erro")
    db.close()

    #根据货号查询商品的生产日期、保质期、生产地址、产家邮箱
    data = list_commoditiesByItemNum(item_num)

    # 使用 item_num作为区块链的chian_index
    sender = "manufacturer"
    data["production_data"] = str(data["production_data"])
    tran_massage = data
    print(tran_massage)

    block_in_chain = Blockchain(int(datas['item_num']))
    print("blockchain is : " , block_in_chain)

    block_in_chain.new_transaction(sender,tran_massage)
    new_block = block_in_chain.new_block(0)
    block_in_chain.add_block(new_block,block_in_chain.proof_of_work(new_block))
    print("new_block is : " , new_block)

    #将区块信息加入 
    block_into_db(new_block,item_num)

    i = 0
    qr_data = ''
    for blockdata in block_in_chain.chain:
        i += 1
        qr_data += 'block{}:{}'.format(i,blockdata['transactions'])

    img = qrcode.make(qr_data)
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 获取上一级绝对路径
    filename = dir_path + '/static/qrcode/chain'+str(item_num) + 'block' + str(i)+'.png'
    img.save(filename)
    return 0
    # filename = '/\/img/' + 'chain' + str(num) + 'block' + str(i) + '.png'
    # img.save(filename)

def block_into_db(block,item_num):
    db = connect_db()
    cursor = db.cursor()
    # 判断是否加入区块链
    blockchain_index = block['chain_index']
    block_index = block['index'] + 1 
    current_hash = block['cur_hash']
    previous_hash = block['previous_hash']
    random_num = block['nonce']
    item_num = item_num
    submit_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """insert into block_info(blockchain_index, block_index, current_hash,
            previous_hash, random_num,item_num,submit_data) VALUES ('%d', '%d', '%s', '%s', '%s','%d','%s')""" \
            % (blockchain_index,block_index, current_hash, previous_hash,random_num,item_num,submit_data)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: update erro")
    db.close()

def show_block(index,status,item_num):
    db = connect_db()
    cursor = db.cursor()
    # 判断是否加入区块链
    sql = "select * from block_info where blockchain_index='%d' and block_index='%d' and item_num ='%d'" % (index,status,item_num)
    block = {}
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            block['blockchain_index'] = item[0]
            block['block_index'] = item[1]
            block['current_hash'] = item[2]
            block['previous_hash'] = item[3]
            block['random_num'] = item[4]
            block['item_num'] = item[5]
            block['submit_data'] = item[6]
        # db.commit()
    except:
        print("查询失败")
    db.close()
    return block
# if __name__ == "__main__":
#     show_block(1,1,1)
