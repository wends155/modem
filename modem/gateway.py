import gevent.monkey
gevent.monkey.patch_time()

import modem
import gevent
import zmq.green as zmq
#from gevent_zeromq import zmq
import simplejson as json
from gevent.queue import Queue
import logging
import time
import signal
import sys


class Gateway(object):
	
	def __init__(self,mod=None,**kwargs):
		
		
		self.__modem = mod or modem.Modem()
		self.message_queue = Queue()
		
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
		logging.info("%s Gateway recv starting." % time.strftime("%d%b%Y,%H:%M"))
		while True:
			for msg in self.__modem.unread():
				logging.info("%s recv msg: %s." % (time.strftime("%d%b%Y,%H:%M"),msg))
				pack_str = json.dumps(msg)
				print pack_str
				self.__push.send_string(pack_str)
				self.__modem.sms_del(msg['index'])
			gevent.sleep(0.5)

	def queue(self):
		logging.info("%s: Gateway queue starting." % time.strftime("%d%b%Y,%H:%M"))
		while True:
			msg = self.__sub.recv_string()
			#print type(msg)
			if type(msg) is unicode:
				msg = msg.encode()

			self.message_queue.put_nowait(msg)
			logging.info("%s: message queued." % time.strftime("%d%b%Y,%H:%M"))
			gevent.sleep(0.2)

	def send_outbox(self,msgpack):
		logging.info("%s: sending message to outbox." % time.strftime("%d%b%Y,%H:%M") )
		self.__outbox.send_string(msgpack)

	def send(self):
		logging.info("%s: Gateway send starting." % time.strftime("%d%b%Y,%H:%M"))
		while True:
			if not self.message_queue.empty():
				msg = self.message_queue.get()
				logging.info("%s: dequeue: %s" % (time.strftime("%d%b%Y,%H:%M"),msg))
				msg_dict = json.loads(msg)
				logging.info("%s: sending...." % time.strftime("%d%b%Y,%H:%M"))
				number = msg_dict['number']
				message = msg_dict['message']
				mid = msg_dict['id']
				#gevent.spawn(self.sms_send,number,message)
				try:
					
					self.__modem.sms_send(number,message)
					logging.info("%s: sent msg#: %s" % (time.strftime("%d%b%Y,%H:%M"),mid))
				except modem.AtCommandError:
					logging.warning("%s: sms not sent AtCommandError, rssi: %s,id:%s" %(time.strftime("%d%b%Y,%H:%M"),self.__modem.get_rssi(),mid))
					gevent.spawn(self.send_outbox,msg)
			gevent.sleep(0.5)

	def stop(self,signum,frame):
		logging.info("%s Stopping." % time.strftime("%d%b%Y,%H:%M"))
		gevent.killall(self.workers)
		raise SystemExit("Exiting.")
			
	def run(self):
		gevent.signal(signal.SIGTERM,self.stop)
		self.workers = [gevent.spawn(self.recv),gevent.spawn(self.queue),gevent.spawn(self.send)]
		#print "connecting to: %s" % (self.server)
		logging.info("%s: connecting to host: %s" % (time.strftime("%d%b%Y,%H:%M"),self.server))
		gevent.joinall(self.workers)
	
	
