from multiprocessing import Process, Manager
from listener import slowdata_listener
from listener import agipd_listener
from dealer import dealer

def main():

    # Initialize data managers
    buffer_agipd_03 = Manager().dict()
    buffer_agipd_04 = Manager().dict()
    buffer_agipd_15 = Manager().dict()
    buffer_slowdata = Manager().dict()
    buffers = [buffer_agipd_03,
               buffer_agipd_04,
               buffer_agipd_15,
               buffer_slowdata]
        
    # List of processes
    processes = []
    processes.append(Process(target=dealer,
                             args=('tcp://127.0.0.1:5100', buffer_agipd_03)))
    processes.append(Process(target=agipd_listener,
                             args=('tcp://127.0.0.1:4600', buffer_agipd_03, 10)))
    processes.append(Process(target=agipd_listener,
                             args=('tcp://127.0.0.1:4601', buffer_agipd_04, 10)))
    processes.append(Process(target=agipd_listener,
                             args=('tcp://127.0.0.1:4602', buffer_agipd_15, 10)))
    processes.append(Process(target=slowdata_listener,
                             args=('tcp://127.0.0.1:4602', buffer_slowdata, 10)))

    
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
