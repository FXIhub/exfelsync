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

    def get_data(self):
        self._zmq_request.send(b'next')
        msg = self._zmq_request.recv()
        self._data = msgpack.loads(msg)
        return self._data

listener = Listener('tcp://localhost:4500')
while(True):
    data = listener.get_data()
    print('Got %d bytes' % (len(data)))
    
    
