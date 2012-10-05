from gevent_zeromq import zmq
import simplejson as json
import time

testdict = {'id':time.time(), 'number':'09186709817','message':'test'}
testpack = json.dumps(testdict)

class Client(object):
	
	def __init__(self,**kwargs):
		settings = {
			'host' : '*',
			'port' : ''
			}
		settings.update(kwargs)
		self.__dict__.update(settings)
		
		self.ctx = zmq.Context()
	
	def recv(self):
		out = self.socket.recv_string()
		if type(out) is unicode:
			out = out.encode()
		return out

class Receiver(Client):
	
	def __init__(self,**kwargs):
		Client.__init__(self, port='5555',**kwargs)
		
		ctx = self.ctx
		self.socket = ctx.socket(zmq.PULL)
		self.socket.bind("tcp://%s:%s" % (self.host,self.port))
		
		
class Outbox(Client):
	
	def __init__(self, **kwargs):
		Client.__init__(self,port='5557',**kwargs)
		
		self.socket = self.ctx.socket(zmq.PULL)
		self.socket.bind("tcp://%s:%s" % (self.host,self.port))
		
class Sender(Client):
	
	def __init__(self, **kwargs):
		Client.__init__(self, port='5556', **kwargs)
		
		self.socket = self.ctx.socket(zmq.PUB)
		self.socket.bind("tcp://%s:%s" % (self.host,self.port))
	
	def recv(self):
		pass
	
	def send_json(self, data=testpack):
		self.socket.send_string(data)

	def send_sms(self,number,message):
		pack_dict = {
			'id': time.time(),
			'number': number,
			'message': message	
		}

		pack_json = json.dumps(pack_dict)
		self.send_json(pack_json)
