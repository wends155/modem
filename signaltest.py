from client import Receiver
import signal

rec = Receiver()
try:
	while True:
		print rec.recv()
		import time
		time.sleep(0.5)
except:
	print "bye"


