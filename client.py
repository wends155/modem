try:
	import zmq.green as zmq
except ImportError:
	from gevent_zeromq import zmq
import simplejson as json
import time

testdict = {'id':time.time(), 'number':'09186709817','message':'test'}
testpack = json.dumps(testdict)

class BaseClient(object):
	
	def __init__(self,**kwargs):
		settings = {
			'host' : '184.164.136.144',
			'port' : ''
			}
		settings.update(kwargs)
		self.__dict__.update(settings)
		
		self.ctx = zmq.Context()

class RClient(BaseClient):
	
	def recv(self):
		out = self.socket.recv_string()
		if type(out) is unicode:
			out = out.encode()
		return out
		
	def recv_json(self):
		out = self.recv()
		return json.loads(out)

class SClient(BaseClient):
	
	def send(self,data):
		if type(data) is str:
			self.socket.send_string(data)
		else:
			raise AttributeError("Data must be a string type.")
			
	def send_json(self,**kwargs):
		pack = json.dumps(kwargs)
		self.send(pack)
			
class Receiver(RClient):
	
	def __init__(self,**kwargs):
		RClient.__init__(self, port='5565',**kwargs)
		
		ctx = self.ctx
		self.socket = ctx.socket(zmq.SUB)
		self.socket.setsockopt(zmq.SUBSCRIBE, "")
		self.socket.connect("tcp://%s:%s" % (self.host,self.port))
		
		
class Outbox(RClient):
	
	def __init__(self, **kwargs):
		RClient.__init__(self,port='5567',**kwargs)
		
		self.socket = self.ctx.socket(zmq.SUB)
		self.socket.setsockopt(zmq.SUBSCRIBE,"")
		self.socket.connect("tcp://%s:%s" % (self.host,self.port))
		
class Sender(SClient):
	
	def __init__(self, **kwargs):
		SClient.__init__(self, port='5566', **kwargs)
		
		self.socket = self.ctx.socket(zmq.PUSH)
		self.socket.connect("tcp://%s:%s" % (self.host,self.port))
	
	
	def send_sms(self,number='09186709817',message='test from sender'):
		pack_dict = {
			'id': time.time(),
			'number': number,
			'message': message	
		}
			
		self.send_json(**pack_dict)
		return pack_dict['id']
