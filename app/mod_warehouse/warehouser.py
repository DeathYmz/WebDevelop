import threading

import pymysql
import qrcode
import datetime
from flask import Flask, request, json, jsonify
from mode_manufacturer.blockchain import Blockchain
from mode_zmq.zmqpublisher import publisher,conf

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

def connect_db():
    return pymysql.connect('localhost', 'root', 'root', 'blockchain')
    # return pymysql.connect('192.168.101.13','root','wsymz44','blockchain')

#查看经销商合作请求列表
@app.route('/list',method=['GET'])
def list_request(warehouse_email):
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from cooperation_info where warehouse_email='%s' "% warehouse_email
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['id'] = item[0]
            data['warehouse_email'] = item[1]
            data['dealer_email'] = item[2]
            data['request_status'] = item[3]
            data_list.append(data)
        # db.commit()
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: select erro")
    db.close()
    return jsonify(data_list)

#接受合作请求
@app.route('/accept/id',method=['POST'])
def accept_cooperation(id):
    db = connect_db()
    cursor = db.cursor()
    sql = "update cooperation_info SET request_status='1' where id='%d'"%id
    flag = False
    try:
        cursor.execute(sql)
        db.commit()
        flag="update success!"
    except:
        db.rollback()  # 如果发生错误则回滚
        print("Error: update erro")
    db.close()
    return jsonify(flag)

#查看订单列表
@app.route('/list')
def list_orders(warehouse_email):
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from manufacturer_order_info where warehouse_email='%s' " % warehouse_email
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['warehouse_email'] = item[0]
            data['manufacturer_email'] = item[1]
            data['item_num'] = item[2]
            data['order_num'] = item[3]
            data['order_state'] = item[4]
            data['submit_data'] = item[5]
            data_list.append(data)
        # db.commit()
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: select erro")
    db.close()
    return jsonify(data_list)

#接受订单填写表单
@app.route('/accept/order_num',method=['POST'])
def accept_order(datas):
    db = connect_db()
    cursor = db.cursor()
    warehouse_email = datas['warehouse_email']
    forwarder_email = datas['forwarder_email']
    item_num = datas['item_num']
    order_num = datas['order_num']
    warehouse_id = datas['warehouse_id']
    order_state = 1
    input_state = 0
    submit_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """insert into forwarder_order_info(warehouse_email, forwarder_email, item_num, order_num, 
                warehouse_id, order_state, input_state, submit_data) VALUES ('%s', '%s', '%d', '%s', 
                '%d', %d', '%d', '%s' )""" % (warehouse_email, forwarder_email, item_num, order_num,
                warehouse_id, order_state, input_state, submit_data)
    flag = False
    try:
        cursor.execute(sql)
        db.commit()
        flag = True
    except:
        db.rollback()

    return jsonify(flag)

#查看库内商品
@app.route('/list')
def list_commodities(warehouse_id):
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from warehouse_info where warehouse_id='%d' "%warehouse_id
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['item_num'] = item[0]
            data['transport_num'] = item[1]
            data['warehouse_id'] = item[2]
            data['input_time'] = item[3]
            data['extra_price'] = item[4]
            data['warehouse_address'] = item[5]
            data['clerk_name'] = item[6]
            data['clerk_tel'] = item[7]
            data['warehouse_email'] = item[8]
            data_list.append(data)
        # db.commit()
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: select erro")
    db.close()
    return jsonify(data_list)

#查看未入库商品
@app.route('/list')
def list_unstorage_commodity():
    db = connect_db()
    cursor = db.cursor()
    sql = "select * from forwarder_order_info where input_state='0' "
    data_list = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            data['warehouse_email'] = item[0]
            data['forwarder_email'] = item[1]
            data['item_num'] = item[2]
            data['order_num'] = item[3]
            data['warehouse_id'] = item[4]
            data['order_state'] = item[5]
            data['input_state'] = item[6]
            data['submit_data'] = item[7]
            data_list.append(data)
        # db.commit()
    except:
        # db.rollback()  # 如果发生错误则回滚
        print("Error: select erro")
    db.close()
    return jsonify(data_list)

#未入库商品入库，加入区块
@app.route('/warehousing/item_num',method=['POST'])
def storage_commodity(item_num):
    db = connect_db()
    cursor = db.cursor()
    sql = "select transport_num from forwarder_info where item_num='%s'"% item_num
    transport_num = cursor.execute(sql)
    #填写入库表单
    datas = request.get_data()
    datas = json.loads(datas)
    item_num = datas['item_num']
    transport_num = transport_num
    warehouse_id = datas['warehouse_id']
    input_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    extra_price = datas['extra_price']
    warehouse_address = datas['warehouse_address']
    clerk_name = datas['clerk_name']
    clerk_tel = datas['clerk_tel']
    warehouse_email = datas['warehouse_email']
    sql = """insert into warehouse_info(item_num, transport_num, warehouse_id, input_time, 
                    extra_price, warehouse_address, clerk_name, clerk_tel, warehouse_email) 
                    VALUES ('%d', '%s', '%d', '%s','%d', '%s', '%s', '%s', '%s' )""" % \
                    (item_num, transport_num, warehouse_id, input_time,extra_price, warehouse_address,
                     clerk_name, clerk_tel, warehouse_email)

    flag = False
    try:
        cursor.execute(sql)
        db.commit()
        flag = True
    except:
        db.rollback()

    #加入区块链
    #根据chain_index/item_num 找到表中同一个链上的区块，按block序号排序
    sql = "select * from blocks_info where chain_index='%d' order by 'block_index' asc"% item_num
    block_in_chain = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            data = {}
            pass
            block_in_chain.append(data)
    except:
        print("Error: select erro")
    db.close()

    # block_in_chain = blocks_list.deepcopy()
    sender = "warehouser"
    tran_message = datas
    print(tran_message)

    # qr_list = block_in_chain.deepcopy()

    block_in_chain.new_transaction(sender,tran_message)
    pre_hash = block_in_chain[-1].cur_hash
    new_block = block_in_chain.new_block(pre_hash)

    # pub-sub pattern
    pub = publisher(conf['private_server'], conf['port'], 'new_block')
    # pub.publish_newblock(new_block)
    _pub_thread = threading.Thread(target=pub.publish_newblock, kwargs={'data': new_block})
    _pub_thread.start()

    # get finished status
    _status = publisher(conf['private_server'], conf['signal_port'], '')
    _status_thread = threading.Thread(target=_status.req_rep)
    _status_thread.start()

    block_in_chain.add_block(new_block, block_in_chain.proof_of_work(new_block))
    print("new_block is : ", new_block)

    # 修改订单状态
    sql = "update manufacturer_info SET commodity_status='1' where item_num='%d'" % item_num
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
        qr_data += 'block{}:{}'.format(i, blockdata['transactions'])

    img = qrcode.make(qr_data)
    img.show()




