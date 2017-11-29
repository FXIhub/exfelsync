import msgpack
import msgpack_numpy
import zmq
msgpack_numpy.patch()



class Listener(object):
    def __init__(self, socket):
        # Reading data over ZMQ using socket adress (this is blocking, so this backend only works with one source at a time)
        self._zmq_context = zmq.Context()
        self._zmq_request = self._zmq_context.socket(zmq.REQ)
        self._zmq_request.connect(socket)
        self._running = False

    def get_data(self):
        self._zmq_request.send(b'next')
        msg = self._zmq_request.recv()
        self._data = msgpack.loads(msg)
        return self._data

    def start(self):
        self._running = True
        while(self._running):
            data = self.get_data()
            print('Got %d bytes' % (len(data)))
            ## TODO: need to feed here into Ringbuffer object

    def stop(self):
        self._running = False

# Testing 
listener = Listener('tcp://localhost:4500')
try:
    listener.start()
except KeyboardInterrupt:
    listener.stop()
    print("Exiting...")

