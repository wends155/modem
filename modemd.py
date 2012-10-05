#!/usr/bin/python
from modem.lib.daemon import Daemon
import sys
import logging
logging.basicConfig(filename='gateway.log',level=logging.INFO)

class ModemDaemon(Daemon):
	def run(self, **kwargs):
		import sys
		from modem import Gateway

		try:
			gate = Gateway(**kwargs)
			gate.run()

			import signal
			

		except SystemExit:
			logging.error("%s: Gateway Error, exiting" % time.strftime("%d%b%Y,%H:%M"))
			sys.exit(0)

		except:
			logging.error("%s: Gateway Error, exiting" % time.strftime("%d%b%Y,%H:%M"))
			sys.exit(1)

	

if __name__ == "__main__":
	import time
	print sys.argv
	logging.info("%s: Starting Gateway" % (time.strftime("%d%b%Y,%H:%M")) )

	mydaemon = ModemDaemon('modem.pid')
	mydaemon.start()
