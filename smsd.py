#!/usr/bin/python
from modem.lib.geventdaemon import GeventDaemon
import sys
import logging
import os
logfile = '/var/run/smsd/smsd.log'
pidfile = '/var/run/smsd/smsd.pid'
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
	if len(sys.argv) > 1:
		mydaemon.start(server=sys.argv[1])
	else: 
		mydaemon.start(server="*")
