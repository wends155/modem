#!/usr/bin/python
from modemd import ModemDaemon

d = ModemDaemon('modem.pid')
d.stop()