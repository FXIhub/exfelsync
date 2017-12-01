from multiprocessing import Process, Manager, Queue
#from listener import slowdata_listener
#from listener import agipd_listener
import listener
from dealer import dealer

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
    buffers = [Manager().dict(),
               Manager().dict(),
               Manager().dict()]
    
    #queue = Queue()
    queue = [Queue(), Queue(), Queue()]
    
        
    # List of processes
    processes = []
    processes.append(Process(target=dealer,
                             args=('tcp://127.0.0.1:5100', buffers, queue)))
    processes.append(Process(target=listener.listener,
                             args=('tcp://127.0.0.1:4600', buffers[0], queue[0])))
    processes.append(Process(target=listener.listener,
                             args=('tcp://127.0.0.1:4601', buffers[1], queue[1])))
    processes.append(Process(target=listener.listener,
                             args=('tcp://127.0.0.1:4602', buffers[2], queue[2])))

    
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
