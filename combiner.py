from multiprocessing import Process, Manager
from listener import slowdata_listener
from listener import agipd_listener

class Combiner(object):
    def __init__(self):

        # Initialize data managers
        buffer_agipd_03 = Manager().dict()
        # TODO: add more managers here
        
        # Initialize data listeners
        self._agipd_03 = agipd_listener('tcp://127.0.0.1:4500', buffer_agipd_03)
        # TODO: add more listeners here

    def start(self):
        
        # List of processes
        self.processes = []

        # Set up pipes and processes for AGIPD 03
        self.processes.append(Process(target=self._agipd_03))
        
        # Start all processes
        for p in self.processes:
            p.start()

        # Stop all processes
        for p in self.processes:
            p.join(timeout=20)
            assert not p.is_alive()
            assert p.exitcode == 0

def main():
    combiner = Combiner()
    combiner.start()

if __name__ == '__main__':
    main()


