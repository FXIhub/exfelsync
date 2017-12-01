#from multiprocessing import Process, Manager, Queue
from threading import Thread
from queue import Queue
#from listener import slowdata_listener
#from listener import agipd_listener
import listener
from dealer import dealer
from collections import OrderedDict

def main():

    # Initialize data managers
    # buffer_agipd_03 = Manager().dict()
    # buffer_agipd_04 = Manager().dict()
    # buffer_agipd_15 = Manager().dict()
    # buffer_slowdata = Manager().dict()
    # buffers = [buffer_agipd_03,
    #            buffer_agipd_04,
    #            buffer_agipd_15,
    #            buffer_slowdata]
    # buffers = [Manager().dict(),
    #            Manager().dict(),
    #            Manager().dict()]
    buffers = [OrderedDict(), OrderedDict(), OrderedDict()]
    
    queue = Queue()
    
        
    # List of processes
    processes = []
    processes.append(Thread(target=dealer,
                             args=('tcp://127.0.0.1:5100', buffers, queue)))
    processes.append(Thread(target=listener.listener,
                             args=('tcp://127.0.0.1:4600', buffers, queue, 0)))
    processes.append(Thread(target=listener.listener,
                             args=('tcp://127.0.0.1:4601', buffers, queue, 1)))
    processes.append(Thread(target=listener.listener,
                             args=('tcp://127.0.0.1:4602', buffers, queue, 2)))

    
    # Start all processes
    for p in processes:
        p.start()

    # Stop all processes
    for p in processes:
        p.join()
        assert not p.is_alive()
        assert p.exitcode == 0

if __name__ == '__main__':
    main()
