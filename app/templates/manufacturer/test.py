#-*-coding:utf-8-*-
from flask import Flask, request, jsonify
from flask import Blueprint,render_template,send_file
import json
import os
import pymysql
import numpy as np
from flask import send_file

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

@app.route('/')
def test():
    return '服务器正常运行'

#此方法处理用户注册

if __name__ == '__main__':
    app.run(host='127.0.0.1')
    
