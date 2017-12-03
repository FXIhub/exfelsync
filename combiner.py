#from multiprocessing import Process, Manager, Queue
from threading import Thread
from queue import Queue
#from listener import slowdata_listener
#from listener import agipd_listener
import listener
from dealer import dealer
from collections import OrderedDict
import sys

def main(number_of_subscribers):
    buffers = [OrderedDict(), OrderedDict(), OrderedDict()]
    
    queue = Queue()
    

    #ip = "127.0.0.1"
    ip = "10.253.0.52"
        
    # List of processes
    processes = []
    processes.append(Thread(target=dealer,
                             args=(5100, number_of_subscribers, buffers, queue)))
    processes.append(Thread(target=listener.listener,
                             args=('tcp://{}:4600'.format(ip), buffers, queue, 0)))
    processes.append(Thread(target=listener.listener,
                             args=('tcp://{}:4601'.format(ip), buffers, queue, 1)))
    processes.append(Thread(target=listener.listener,
                            args=('tcp://{}:4602'.format(ip), buffers, queue, 2)))

    
    # Start all processes
    for p in processes:
        p.start()

    # Stop all processes
    for p in processes:
        p.join()
        assert not p.is_alive()
        assert p.exitcode == 0

if __name__ == '__main__':

    number_of_subscribers = int(sys.argv[1])
    main(number_of_subscribers)
