from multiprocessing import Process, Manager
from listener import slowdata_listener
from listener import agipd_listener
from dealer import dealer

def main():

    # Initialize data managers
    buffer_agipd_03 = Manager().dict()
    # TODO: add more managers here
        
    # List of processes
    processes = []
    processes.append(Process(target=dealer, args=('tcp://127.0.0.1:5100', buffer_agipd_03)))
    processes.append(Process(target=agipd_listener, args=('tcp://127.0.0.1:4500', buffer_agipd_03)))

    # Start all processes
    for p in processes:
        p.start()

    # Stop all processes
    for p in processes:
        p.join(timeout=20)
        #assert not p.is_alive()
        #assert p.exitcode == 0

if __name__ == '__main__':
    main()
