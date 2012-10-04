from gevent_zeromq import zmq
import simplejson as json
import time

testdict = {'id':time.time(), 'number':'09186709817','message':'test'}
testpack = json.dumps(testdict)

ctx = zmq.Context()

receiver = ctx.socket(zmq.PULL)
receiver.bind('tcp://*:5555')

sender = ctx.socket(zmq.PUB)
sender.bind('tcp://*:5556')

outbox = ctx.socket(zmq.PULL)
outbox.bind('tcp://*:5557')

def recv():
	return receiver.recv_string()

def send(pack=testpack):
	return sender.send_string(pack)
	
def get_outbox():
	return outbox.recv_string()
