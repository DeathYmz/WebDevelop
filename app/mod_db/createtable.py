import pymysql
import datetime
import numpy as np
import config
opt = config.parse_opt()

def connect_db():
    return pymysql.connect(opt.ip,opt.sqlroot,opt.sqlpassword,opt.sqldatabase)
def create_manufacturer_info():
    db = connect_db()
    cursor = db.cursor()
    # sql_drop = '''drop table if exists `manufacturer_info`
    # '''
    # cursor.execute(sql_drop)
    sql =''' CREATE TABLE IF NOT EXISTS `manufacturer_info`(
        `trade_name` VARCHAR(30) NOT NULL,
        `attribute` VARCHAR(30) NOT NULL,
        `number` int NOT NULL,
        `production_data` DATETIME,
        `expiration_data` int NOT NULL,
        `item_num` int AUTO_INCREMENT,
        `manufacturer` VARCHAR(50) NOT NULL,
        `production_address` VARCHAR(50) NOT NULL,
        `trade_price` int NOT NULL,
        `commodity_status` bool NOT NULL,
        `manufacturer_email` VARCHAR(30) NOT NULL,
        PRIMARY KEY ( `item_num` )
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()
def create_forwarder_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `forwarder_info`(
        `item_num` int NOT NULL,
        `transport_num` VARCHAR(30) NOT NULL,
        `start_time` DATETIME,
        `destination` VARCHAR(30) NOT NULL,
        `transporter_name` VARCHAR(30) NOT NULL,
        `transporter_tel` VARCHAR(30) NOT NULL,
        `item_address` VARCHAR(30) NOT NULL,
        `forwarder _email` VARCHAR(30) NOT NULL,
        PRIMARY KEY ( `transport_num` ),
        foreign key (`item_num`) references manufacturer_info (`item_num`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()

def create_warehouse_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `warehouse_info`(
        `item_num` int NOT NULL,
        `transport_num` VARCHAR(30) NOT NULL,
        `warehouse_id` int NOT NULL,
        `input_time` DATETIME,
        `extra_price` int NOT NULL,
        `warehouse_address` VARCHAR(50) NOT NULL,
        `clerk_name` VARCHAR(30) NOT NULL,
        `clerk_tel` VARCHAR(30) NOT NULL,
        `warehouse_email` VARCHAR(30) NOT NULL,
        PRIMARY KEY ( `warehouse_id` ),
        foreign key (`item_num`) references manufacturer_info (`item_num`),
        foreign key (`transport_num`) references forwarder_info (`transport_num`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()

def create_retailer_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `retailer_info`(
        `warehouse_email` VARCHAR(30) NOT NULL,
        `extra_price` int NOT NULL,
        `dealer_name` VARCHAR(30) NOT NULL,
        `retailer_email` VARCHAR(30) NOT NULL
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()

def create_user_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `user_info`(
        `username` VARCHAR(30) NOT NULL,
        `telephone` VARCHAR(30) NOT NULL,
        `password` VARCHAR(30) NOT NULL,
        `email` VARCHAR(30) NOT NULL,
        `status` int NOT NULL,
        `register_data` datetime,
        PRIMARY KEY (`status`,`email`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()
def create_cooperation_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `cooperation_info`(
        `id` int NOT NULL,
        `warehouse_email` VARCHAR(30) NOT NULL,
        `dealer_email` VARCHAR(30) NOT NULL,
        PRIMARY KEY ( `id`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()

def create_manufacturer_order_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `manufacturer_order_info`(
        `warehouse_email` VARCHAR(30) NOT NULL,
        `manufacturer_email`  VARCHAR(30) NOT NULL,
        `item_num` int NOT NULL,
        `order_num` int AUTO_INCREMENT,
        `order_state` bool NOT NULL,
        `submit_data` datetime,
        PRIMARY KEY ( `order_num`),
        foreign key (`item_num`) references manufacturer_info (`item_num`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()
def create_forwarder_order_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `forwarder_order_info`(
        `warehouse_email` VARCHAR(30) NOT NULL,
        `forworder_email`  VARCHAR(30) NOT NULL,
        `item_num` int NOT NULL,
        `order_num` int AUTO_INCREMENT,
        `warehouse_id` int NOT NULL,
        `order_state` bool NOT NULL,
        `input_state` bool NOT NULL,
        `submit_data` datetime,
        PRIMARY KEY ( `order_num`),
        foreign key (`item_num`) references manufacturer_info (`item_num`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()

def create_block_info():
    db = connect_db()
    cursor = db.cursor()
    sql =''' CREATE TABLE IF NOT EXISTS `block_info`(
        `blockchain_index` int NOT NULL,
        `block_index` int NOT NULL,
        `current_hash` VARCHAR(100) NOT NULL,
        `previous_hash` VARCHAR(100) NOT NULL,
        `random_num` VARCHAR(100) NOT NULL,
        `item_num` int NOT NULL,
        `submit_data` datetime,
        foreign key (`item_num`) references manufacturer_info (`item_num`)
        )ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;'''
    cursor.execute(sql)
    db.close()

def drop():
    db = connect_db()
    cursor = db.cursor()
    sql_drop = ["drop table if exists block_info","drop table if exists forwarder_order_info","drop table if exists manufacturer_order_info","drop table if exists order_info","drop table if exists cooperation_info", "drop table if exists user_info",
    "drop table if exists retailer_info","drop table if exists warehouse_info","drop table if exists forwarder_info","drop table if exists manufacturer_info",]    
    for item in sql_drop:
        cursor.execute(item)
    db.close()
    # cursor.execute(sql_drop)

if __name__ == "__main__":
    drop()
    create_manufacturer_info()
    create_forwarder_info()
    create_warehouse_info()
    create_retailer_info()
    create_user_info()
    create_cooperation_info()
    create_manufacturer_info()
    create_forwarder_order_info()
    create_block_info()
    
