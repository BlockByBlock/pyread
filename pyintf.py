#!/usr/bin/python

"""
pyintf.

~~~~~~~~~~
This module reads from serial using python.
It launches a session and provide a menu option.
-- ybingcheng@gmail.com
"""

import sys
import serial
# import threading
import logging
from time import sleep
from pycolor import WHT, HRED, GRN, BLU, HYEL
from misca import procfieldvar, procprevfield

# STX = 0x02
# ENQ = 0x01

logging.basicConfig(
    filename='serial.log',
    filemode='w',
    format='',
    level=logging.DEBUG
)


class SerialPort(object):
    """Create a serial port class."""

    def __init__(self, port, baudrate, bytesize, parity, stopbits,
                 timeout):
        """Return port, baudrate."""
        self.serial = serial.Serial(port, baudrate, bytesize, parity,
                                    stopbits, timeout)
        self.dataread = ""  # Flush

#    def start(self):
#        """Start serial port thread."""
#        self.alive = True
#        self.thread = threading.Thread(target=self.listener)
#        # self.thread.setDaemon(True)
#        self.thread.start()

#    def listener(self):
#        """Listen to the serial port."""
#        pass

    def stop(self):
        """Close serial port."""
        self.serial.close()
        print "Exiting...\n"
        sys.exit()
#        self.alive = False

#    def join(self):
#        """Join thread."""
#        self.thread.join()

    def writer(self):
        """Send command."""
        # buffer = ENQ
        store_buffer = ""
        cmd = raw_input("Send Command >> ")
        bcmd = bytearray(cmd + '\r')
        self.serial.write(bcmd)
        sleep(3)  # buffer
        print "Sending " + HYEL + bcmd + WHT
        writelen = len(bcmd) + 5
        for x in range(0, writelen):
            self.dataread = self.serial.readline()
#            print self.dataread
            if isinstance(self.dataread, str) is True:
                store_msg = self.dataread
                store_buffer += store_msg  # store up
                store_msg = store_buffer
            else:
                print "Detected not string"
        return store_msg

    def reader(self):
        """Read serial port."""
        counter = 1
        try:
            while self.serial.isOpen():
                counter += 1
                self.serial.write(str(chr(counter)))
                sleep(.1)
                if counter == 225:
                    counter = counter  # Reset counter
                self.dataread = self.serial.readline()
                logging.info(self.dataread)
                print self.dataread
        except serial.SerialException, e:
            self.alive = False
            print ("Error: ") + str(e)

    def menu(self):
        """Print menu for command selection."""
        print "--------------------------------------"
        print "Reader/Writer Tool for RS232 Device"
        print "--------------------------------------"
        print "Option :: "
        print "1. Write Command"
        print "2. Read Only"
        print "3. Process Msg Fields"
        print "0. Exit"
        print "\n"


def main(argv):
    """Open serial port."""
    config_file = open("portconfig.txt")
    port = config_file.readline().rstrip('\n')
    baudrate = config_file.readline()
    bytesize = serial.EIGHTBITS
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    timeout = 0
    session = 1

    try:
        sp = SerialPort(port, baudrate, bytesize, parity, stopbits, timeout)
    except serial.SerialException, e:
        sys.stderr.write(HRED + "Port cannot be open %r: %s\n" % (port, e))
        sys.exit(1)

    sys.stderr.write(GRN + 'Reading port on %s with baudrate of %d\n' % (
        sp.serial.port,
        sp.serial.baudrate
    ) + WHT)

#    sp.start()
    sp.menu()
    while session == 1:
        cmdkey = raw_input(BLU + "Number Only. Key In Command: " + WHT)
        if cmdkey == "0":
            session = 0
            sp.stop()
        elif cmdkey == "1":
            print "Write command and send via serial port :  "
            sp.serial.reset_input_buffer()
            sp.serial.reset_output_buffer()
            return_msg = sp.writer()  # Nil count
            if return_msg is None:
                print "Nothing"
            else:
                print "I received : "
                print return_msg
            # sys.exit()
        elif cmdkey == "2":
            print "Read from serial port : "
            sp.reader()
        elif cmdkey == "3":
            print "Processing message fields"
            endindex = procfieldvar()
            startindex = procprevfield()
            print return_msg[startindex:endindex]
        else:
            sp.menu()

#    try:
#        sp.join()
#    except KeyboardInterrupt:
#        pass
#    sys.stderr.write("\n >>> Exiting... ")
#    sp.join()


if __name__ == '__main__':
    main(sys.argv[1:])  # Take all arguments after 1st
