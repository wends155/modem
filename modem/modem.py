import lib.humod 
import time
import re

class Modem(lib.humod.Modem):
	"""
		upper level wrapper of pyhumod.
	"""
	pattern = '^(\+63|0)(\d+)'

	def __init__(self, DATA_PORT = '/dev/ttyUSB0', CONTROL_PORT = '/dev/ttyUSB1'):
		lib.humod.Modem.__init__(self, DATA_PORT, CONTROL_PORT)
		self.enable_textmode(True)
		
	def unread(self):
		return self.sms_msgs('REC UNREAD')
		
	def _time(self,sms_time):
		t = time.strptime(sms_time, '%y/%m/%d,%H:%M:%S+32')
		return time.mktime(t)
	
	def sms_msgs(self, status='ALL'):
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
	
	def _sender(self,sender):
		matcher = re.compile(self.pattern)
		match = matcher.search(sender).groups()[1]
		return '0' + match

	def sms_clear(self):
		for msg in self.sms_list():
			self.sms_del(msg[0])

