from gevent import monkey
monkey.patch_all()

import modem
import gevent
from gevent_zeromq import zmq
import simplejson as json
from gevent.queue import Queue

class Gateway(object):
	
	message_queue = Queue()

	def __init__(self,modem,**kwargs):
		
		self.__modem = modem

		settings = {
			'server': "*",
			'push_port' : '5555',
			'sub_port'  : '5556',
			'outbox_port': '5557',
			'subscribe_topic' : ""
		}
		settings.update(kwargs)

		server = {
			'push' : "tcp://%s:%s" % (settings['server'],settings['push_port']),
			'sub' : "tcp://%s:%s" % (settings['server'],settings['sub_port']),
			'outbox' : "tcp://%s:%s" % (settings['server'],settings['outbox_port'])
		}
		settings.update(server)
		self.server = settings['server']

		self.ctx = zmq.Context()

		self.__push = self.ctx.socket(zmq.PUSH)
		self.__push.connect(settings['push'])

		self.__sub = self.ctx.socket(zmq.SUB)
		self.__sub.connect(settings['sub'])
		self.__sub.setsockopt(zmq.SUBSCRIBE,settings['subscribe_topic'])
 		
 		self.__outbox = self.ctx.socket(zmq.PUSH)
 		self.__outbox.connect(settings['outbox'])

		self.__queue = Queue()

	def recv(self):
		while True:
			for msg in self.__modem.unread():
				pack_str = json.dumps(msg)
				print pack_str
				self.__push.send_string(pack_str)
				self.__modem.sms_del(msg['index'])
			gevent.sleep(0.2)

	def queue(self):
		while True:
			msg = self.__sub.recv_string()
			print msg
			if msg is unicode:
				msg = msg.encode()

			self.message_queue.put_nowait(msg)
			gevent.sleep(0.2)

	def send_outbox(self,msgpack):
		print "type: %s, msg: %s" % (type(msgpack),msgpack)
		self.__outbox.send_string(msgpack)

	def send(self):
		while True:
			if not self.message_queue.empty():
				msg = self.message_queue.get()
				msg_dict = json.loads(msg)

				number = msg_dict['number']
				message = msg_dict['message']
				#gevent.spawn(self.sms_send,number,message)
				try: 
					self.__modem.sms_send(number,message)
					print "sent"
				except modem.AtCommandError:
					gevent.spawn(self.send_outbox,msg)
			gevent.sleep(0.2)

	def run(self):
		work = [gevent.spawn(self.recv),gevent.spawn(self.queue),gevent.spawn(self.send)]
		print "connecting to: %s" % (self.server)
		gevent.joinall(work)
	
	
