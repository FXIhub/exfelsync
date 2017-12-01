import numpy as np
import msgpack
import msgpack_numpy
import zmq
msgpack_numpy.patch()

listener = lambda *args: Listener(*args).start()
class Listener(object):
    """Simple listener."""
    def __init__(self, socket, buf, queue, lifetime = 60):
        self._socket = socket
        self._zmq_context = zmq.Context()
        self._zmq_request = self._zmq_context.socket(zmq.REQ)
        self._zmq_request.connect(self._socket)
        self._buf = buf
        self._queue = queue
        self._running = False
        self._lifetime = lifetime

    def get_data(self):
        """Receive data packets over the network"""
        self._zmq_request.send(b'next')
        #return  msgpack.loads(self._zmq_request.recv())
        data = msgpack.loads(self._zmq_request.recv())
        train_id = data[list(data.keys())[0]]["header.trainId"]
        self._buf[train_id] = data
        self._queue.put(train_id)

    # def _drop_old_data(self, current_time):
    #     """Remove expired data from the buffer"""
    #     for k in self._buf.keys():
    #         timelimit = current_time - self._lifetime
    #         if (k < timelimit):
    #             del self._buf[k]
        
    def start(self):
        print("Starting...")
        self._running = True
        while(self._running):
            #self.write_data(self.get_data())
            self.get_data()

    def stop(self):
        self._running = False

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
