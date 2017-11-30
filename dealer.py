import time, sys

dealer = lambda *args: Dealer(*args).start()
class Dealer(object):
    def __init__(self, socket, buf):
        self._socket = socket
        # TODO: Create a ZMQ service that can deal out data to a client
        self._buf = buf

    def start(self):
        print("Starting reading...")
        while(True):
            print("Reader", len(self._buf))
            #for k in self._buf.keys():
            #    del self._buf[k]
            sys.stdout.flush()
            time.sleep(1)

        
