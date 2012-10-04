#!/usr/bin/python
from modem import Modem,Gateway
import sys

def main(**kwargs):
	try:
		mod = Modem()
		gate = Gateway(mod, **kwargs)
		gate.run()
	except KeyboardInterrupt:
		print "exiting"
		sys.exit()
	except KeyError:
		print "keyerror"
		sys.exit(1)
		
if __name__ == "__main__":
	if len(sys.argv) > 1:
		server = sys.argv[1]
		main(server=server)
	main()
