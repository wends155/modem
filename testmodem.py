#!/usr/bin/python
from modem import Modem,Gateway
#from serial.serialutil import SerialException
import sys
import logging
import time

def main(**kwargs):
	try:
		
		gate = Gateway(**kwargs)
		gate.run()
	except KeyboardInterrupt:
		logging.error("%s: process stopped by user" % (time.strftime("%d%b%Y,%H:%M")))
		sys.exit()
			
if __name__ == "__main__":
	logging.basicConfig(filename='gateway.log',level=logging.INFO)
	logging.info("%s: starting server" % (time.strftime("%d%b%Y,%H:%M")) )
	if len(sys.argv) > 1:
		server = sys.argv[1]
		main(server=server)
	main()
