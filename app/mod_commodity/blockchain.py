import hashlib
import json
import datetime
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request

class Blockchain:  #类负责管理链式数据，它会存储交易并且还有添加新的区块到链式数据的Method
    zero_num = 4
    def __init__(self,_index):
        self.current_transactions = []
        self.chain = []
        self.chain_index = _index

    def new_block(self, previous_hash):#一个区块包含索引、事务列表、时间戳、校验、前哈希
        block = {
            'chain_index' : self.chain_index,
            'index': len(self.chain) ,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'transactions': self.current_transactions,
            'nonce': 0,
            'previous_hash': previous_hash,
            'cur_hash':'0',
        }
        self.current_transactions = []  #改成累加
        return block

    def add_block(self,block,proof):
        if (len(self.chain)==0):
            previous_hash = 0
        else :
            previous_hash = self.last_block()['cur_hash']
            print("last_block_hash = " ,self.last_block['cur_hash'])

        print("block_pre_hash = " , block['previous_hash'])
        
        if previous_hash != block['previous_hash']:
            return False
        print("proof = " + proof)
        if not self.valid_proof(block,proof):
            return False

        block['cur_hash']=proof
        print("block_hash = ", block['cur_hash'])
        self.chain.append(block)
        return True

    @staticmethod
    def hash(block):
        _data = block['transactions'] + list(str(block['nonce']))
        block_string = json.dumps(_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, contents):  #添加交易到区块
        self.current_transactions.append({
            'sender': sender,
            'contents': contents,
        })
        # return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block['nonce']=0

        compute_hash = self.hash(block)
        while not compute_hash.startswith('0' * self.zero_num):
            block['nonce'] += 1
            compute_hash=self.hash(block)
        return compute_hash

    # @staticmethod
    def valid_proof(self,block,block_hash):
        return (block_hash.startswith('0' * self.zero_num ) and
                block_hash == self.hash(block))

    def list_chain(self):
        return self.chain
