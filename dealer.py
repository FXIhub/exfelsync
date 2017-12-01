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
    def __init__(self, socket, buf, queue):
        self._socket = socket
        # TODO: Create a ZMQ service that can deal out data to a client
        self._send_queue = deque(maxlen=100)
        self._send_queue_max_size = 10
        self._buf = buf
        self._queue = queue
        self._socket = socket

        # t = Thread(target=self._send, args=(self._send_queue,))
        # t.start()


    def start(self):
        print("Starting reading...")
        while(True):
            train_id = self._queue.get()
            if train_id is None:
                time.sleep(0.0001)
            else:
                data_list = [this_buf[train_id] for this_buf in self._buf]
                #self._zmq_socket.send(msgpack.dumps(data_list))
                if len(self._send_queue) < self._send_queue_max_size:
                    print("Sending data {}".format(train_id))
                    self._send_queue.append(data_list)
                else:
                    print("Skipping data {}".format(train_id))
                for this_buf in self._buf:
                    del this_buf[train_id]

    def send(self, queue):
        zmq_context = zmq.Context()
        zmq_socket = zmq_context.socket(zmq.REP)
        zmq_socket.bind(self._socket)

        while(True):
            msg = zmq_socket.recv()
            if msg == b'next':
                while len(self._queue) <= 0:
                    sleep(0.1)
                zmq_socket.send(msgpack.dumps(queue.popleft()))
