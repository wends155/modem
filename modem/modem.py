import humod
import time

class Modem(humod.Modem):
	"""
		upper level wrapper of pyhumod.
	"""
	def __init__(self, DATA_PORT = '/dev/ttyUSB0', CONTROL_PORT = '/dev/ttyUSB1'):
		humod.Modem.__init__(self, DATA_PORT, CONTROL_PORT)
		self.enable_textmode(True)
		
	def unread(self):
		return self.sms_msgs('REC UNREAD')
		
	def _time(self,sms_time):
		t = time.strptime(sms_time, '%y/%m/%d,%H:%M:%S+32')
		return time.mktime(t)
	
	def sms_msgs(self, status='ALL'):
		msgs = []
		for msg in self.sms_list(status):
			number = msg[2]
			message = self.sms_read(msg[0])
			msg_index = int(msg[0])
			sms_time = self._time(msg[4])
			sms_status = msg[1]
			
			pack = {'msg_index':msg_index, 'status':sms_status, 'sender':number, 'message':message,'time':sms_time}
			msgs.append(pack)
		return msgs
