from client import Outbox
import signal

outb = Outbox()
try:
	while True:
		print "failed: %s" % outb.recv()
		import time
		time.sleep(0.5)
except:
	print "bye"


