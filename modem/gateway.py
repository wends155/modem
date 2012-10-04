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
			'push' : 'tcp://*:5555',
			'sub'  : 'tcp://*:5556'
		}
		settings.update(kwargs)
				
		self.ctx = zmq.Context()

		self.__push = self.ctx.socket(zmq.PUSH)
		self.__push.connect(settings['push'])

		self.__sub = self.ctx.socket(zmq.SUB)
		self.__sub.connect(settings['sub'])
		self.__sub.setsockopt(zmq.SUBSCRIBE,"")
 
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

	def sms_send(self,number,message):
		try:
			self.__modem.sms_send(number,message)
		except modem.AtCommandError:
			print 'ATCommandError'

	def send(self):
		while True:
			if not self.message_queue.empty():
				msg = self.message_queue.get()
				msg = json.loads(msg)

				number = msg['number']
				message = msg['message']
				gevent.spawn(self.sms_send,number,message)

			gevent.sleep(0.2)

	def run(self):
		work = [gevent.spawn(self.recv),gevent.spawn(self.queue),gevent.spawn(self.send)]
		print 'starting work'
		gevent.joinall(work)
	
	
