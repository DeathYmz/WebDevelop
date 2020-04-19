import zmq
import threading
import json
from hashlib import sha256
import os
import time

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__))+"\\conf.json"))

class subscriber:
    def __init__(self, bindserver,port,pub_key):
        self.server = bindserver
        self.port = port
        self.key = pub_key

    #sub new block event
    def sub_newblock(self):
        # Prepare our context and subscriber
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://{}:{}".format(self.server,self.port))
        subscriber.setsockopt(zmq.SUBSCRIBE, bytes(self.key,'utf-8'))

        while True:
            # Read envelope with address
            [address, contents] = subscriber.recv_multipart()
            print("[%s] %s" % (address, contents))
            hash(contents)

        subscriber.close()
        context.term()

    #sub write event
    def write_newblock(self):
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://{}:{}".format(self.server, self.port))
        subscriber.setsockopt(zmq.SUBSCRIBE, bytes(self.key, 'utf-8'))

        while True:
            # Read envelope with address
            [address, contents] = subscriber.recv_multipart()
            print("[%s] %s" % (address, contents))
            write_blockfile(contents)

        subscriber.close()
        context.term()

def hash(data):
    block_object = json.loads(data)
    _data = block_object['transactions'] + list(str(block_object['nonce']))
    block_string = json.dumps(_data, sort_keys=True).encode()
    computed_hash = sha256(block_string).hexdigest()
    while not computed_hash.startswith('0' * 4):
        block_object['nonce'] +=1
        computed_hash = hash(block_object)
        print(computed_hash)
    print('最终结果是:{}, 随机数:{}'.format(computed_hash, block_object['nonce']))
    #send signal of status,FIFO
    #time.sleep(10)
    send_finish_status(block_object)
    return computed_hash

# send signal
def send_finish_status(block_object):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{}:{}".format(conf["server"], conf["signal_port"]))
    print('fdsfffffffffffffff===',type(block_object),block_object)
    block_dict = {}
    block_dict['finished'] = block_object
    block_string = json.dumps(block_dict)
    socket.send(bytes(block_string,'utf-8'))

def write_blockfile(data):
    obj_data = json.loads(data.decode(encoding="utf-8"))
    #print('the file ==================',obj_data," and index is ",json.dumps(obj_data,indent=2,ensure_ascii=False))
    with open(_basepath+'\\block'+str(obj_data['index'])+'.txt', 'w',encoding="utf-8") as f:
        f.write(json.dumps(obj_data,indent=2,ensure_ascii=False))


print('消息服务器',conf["server"])
_newblock_sub = subscriber(conf["server"],conf["port"],conf["sub_topic"])
#instead of s.sub_newblock(),we use thread fun,avoid locking
_newblock_thread = threading.Thread(target=_newblock_sub.sub_newblock)
_newblock_thread.start()


_writeblock_sub = subscriber(conf["server"],conf["write_port"],"write_block")
_writeblock_thread = threading.Thread(target=_writeblock_sub.write_newblock)
_writeblock_thread.start()