import msgpack
import msgpack_numpy
import zmq
msgpack_numpy.patch()

def agipd_listener(*args):
    AGIPDListener(*args).start()

def slowdata_listener(*args):
    SlowDataListener(*args).start()

class Listener(object):
    """Simple listener."""
    def __init__(self, socket, buf):
        self._socket = socket
        self._zmq_context = zmq.Context()
        self._zmq_request = self._zmq_context.socket(zmq.REQ)
        self._zmq_request.connect(self._socket)
        self._buf = buf
        self._running = False

    def get_data(self):
        """Receive data packets over the network"""
        self._zmq_request.send(b'next')
        return  msgpack.loads(self._zmq_request.recv())

    def write_data(self, data):
        """Write data into the ringbuffer"""
        print('Wrote %d bytes' % (len(data)))
    
    def start(self):
        print("Starting...")
        self._running = True
        while(self._running):
            print("Is running...")
            data = self.get_data()
            print('Got %d bytes' % (len(data)))
            self.write_data(data)

    def stop(self):
        self._running = False

class AGIPDListener(Listener):
    def __init__(self, *args, **kwargs):
        Listener.__init__(self, *args, **kwargs)
    def write_data(self,data):
        print(data)

class SlowDataListener(Listener):
    def __init__(self, *args, **kwargs):
        Listener.__init__(self, *args, **kwargs)
    def write_data(self,data):
        print(data)

# Testing
def main():
    listener = Listener('tcp://localhost:4500', {})
    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()
        print("Exiting...")

if __name__ == '__main__':
    main()
