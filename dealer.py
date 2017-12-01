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
        self._buf = buf
        self._queues = queue
        self._socket = socket

        # t = Thread(target=self._send, args=(self._send_queue,))
        # t.start()


    def start(self):
        print("Starting reading...")
        while(True):
            for this_queue in self._queues:
                train_id = this_queue.get()
                if train_id is None:
                    #time.sleep(0.01)
                    continue
                else:
                    if all([train_id in this_buf for this_buf in self._buf]):
                        data_list = [this_buf[train_id] for this_buf in self._buf]
                        print("send data {}".format(train_id))
                        for this_buf in self._buf:
                            del this_buf[train_id]

    def send(self, queue):
        zmq_context = zmq.Context()
        zmq_socket = zmq_context.socket(zmq.REP)
        zmq_socket.bind(self._socket)
        
                
