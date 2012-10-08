from client import Receiver
import signal
import simplejson as json
import time
import pynotify

pynotify.init('icon-summary-body')
rec = Receiver()

def notify(sender,message):
	n = pynotify.Notification(sender,message,'notification-message-im')
	n.show()

try:
	while True:
		msg = rec.recv()
		msg = json.loads(msg)
		sender = msg['sender']
		message = msg['message']
		time = time.strftime("%d%b%Y,%H:%M",time.localtime(msg['time']))
		notify(sender,message)
		print "%s: (%s) > %s" % (time,sender,message)
		import time
		time.sleep(0.5)
except KeyboardInterrupt:
	print "bye"

