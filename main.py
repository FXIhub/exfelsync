import multiprocessing
import ringbuffer

from listener import Listener




def main():

    # Initialize a commone ringbuffer
    ring = ringbuffer.RingBuffer(slot_bytes=50000, slot_count=100)

    # Initialize data listeners
    list01 = Listener('tcp://localhost:4500')

    # List of processes
    processes = []
    processes.append(multiprocessing.Process(target=list01, args=(ring,)))

    # Start all processes
    for p in processes:
        p.start()

    # 
    for p in processes:
        p.join(timeout=20)
        assert not p.is_alive()
        assert p.exitcode == 0


if __name__ == '__main__':
    main()






