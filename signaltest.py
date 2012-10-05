import os
import sys

def run():
	import gevent.monkey
	gevent.monkey.patch_time()
	import atexit
	import gevent
	import signal
	
	
	def sigstop():
		sys.exit()
	gevent.signal(signal.SIGTERM,sigstop)
	

	def delpid():
		os.remove('test.pid')
	atexit.register(delpid)
	from modem import Gateway
	gate = Gateway()
	gate.run()

def writepid(pid):
	open('test.pid','w+').write("%s\n"%pid)

def daemonize():
	import gevent
	pid = gevent.fork()
	if pid == 0:
		run()
		sys.exit(0)
	else:
		writepid(pid)

def stop():
	sys.exit(0)

daemonize()