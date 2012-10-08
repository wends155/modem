import lib.humod 
from lib.humod.errors import AtCommandError
import time
import re
import logging

def gettime():
	return time.strftime("%d%b%Y,%H:%M")

class Modem(lib.humod.Modem):
	"""
		upper level wrapper of pyhumod.
	"""
	pattern = '^(\+63|0)(\d+)'
	_observers = []

	def __init__(self, DATA_PORT = '/dev/ttyUSB0', CONTROL_PORT = '/dev/ttyUSB1'):
		from serial.serialutil import SerialException
		import sys

		try:
			lib.humod.Modem.__init__(self, DATA_PORT, CONTROL_PORT)
			self.enable_textmode(True)
		except: 
			logging.error("%s: No modem connected" % (gettime()) )
			raise SystemExit() #todo

	def unread(self):
		return self.sms_msglist('REC UNREAD')
		
	def _time(self,sms_time):
		t = time.strptime(sms_time, '%y/%m/%d,%H:%M:%S+32')
		return time.mktime(t)
	
	def sms_msglist(self, status='ALL'):
		msgs = []
		for msg in self.sms_list(status):
			number = self._sender(msg[2])
			message = self.sms_read(msg[0])
			index = int(msg[0])
			sms_time = self._time(msg[4])
			sms_status = msg[1]
			
			pack = {'index':index, 'status':sms_status, 'sender':number, 'message':message,'time':sms_time}
			msgs.append(pack)
		return msgs
	
	def sms_msg(self,index):
		return self.sms_msglist()[index]

	def _sender(self,sender):
		matcher = re.compile(self.pattern)
		match = matcher.search(sender)
		if match:
			match = match.groups()[1]
			return '0' + match
		else: 
			return sender

	def sms_clear(self):
		for msg in self.sms_list():
			self.sms_del(msg[0])

		
	def balance(self):
		try:
			self.sms_send('214','?15001')
		except AtCommandError:
			loggin.warning("sms not sent AtCommandError, rssi: %s" % (self.get_rssi()))