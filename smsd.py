#!/usr/bin/python
from modem.lib.geventdaemon import GeventDaemon
import sys
import logging
import os
logfile = 'smsd.log'
pidfile = 'smsd.pid'
logging.basicConfig(filename=logfile,level=logging.INFO)

class ModemDaemon(GeventDaemon):
	def run(self, **kwargs):
		import sys
		from modem import Gateway

		try:
			gate = Gateway(**kwargs)
			gate.run()

			
		except SystemExit:
			logging.error("%s: Gateway SIGTERM, exiting" % time.strftime("%d%b%Y,%H:%M"))
			sys.exit(0)


if __name__ == "__main__":
	import time
	logging.info("%s: Starting Gateway" % (time.strftime("%d%b%Y,%H:%M")) )
	
	mydaemon = ModemDaemon(pidfile)
	try:
		connect = os.environ["CONNECT"]
		mydaemon.start(server=connect)
	except KeyError:
		connect = "184.164.136.144"
		mydaemon.start(server=connect)
	
