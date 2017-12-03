import time
import sys
import zmq
import msgpack
from collections import deque
from threading import Thread

# send_context = zmq.Context()
# send_socket = send_context.socket(zmq.REP)
# send_socket.bind('tcp://*:{}'.format(OUTPUT_PORT))


dealer = lambda *args: Dealer(*args).start()
class Dealer(object):
    def __init__(self, port, nsubscribe, buf, queue):
        self._nsubscribe = nsubscribe
        self._port = port
        # TODO: Create a ZMQ service that can deal out data to a client
        self._send_queue = deque(maxlen=100)
        self._send_queue_max_size = 10
        self._buf = buf
        self._queue = queue

    def start(self):
        #t = Thread(target=self.send, args=(self._send_queue,))
        #t.start()
        zmq_context = zmq.Context()
        zmq_socket = zmq_context.socket(zmq.PUB)
        zmq_socket.bind("tcp://*:%d" %(self._port))

        print("Starting reading...")
        while(True):
            if self._queue.qsize() <= 0:
                time.sleep(0.01)
            else:
                train_id = self._queue.get()
                socket_id = train_id % self._nsubscribe
                try:
                    data_list = [this_buf[train_id] for this_buf in self._buf]
                except KeyError:
                    print(train_id)
                    continue
                zmq_socket.send(b"%d %s" %(socket_id, msgpack.dumps(data_list)))
                for this_buf in self._buf:
                    try:
                        del this_buf[train_id]
                    except KeyError:
                        pass

