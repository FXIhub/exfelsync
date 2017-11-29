import numpy as np
import msgpack
import msgpack_numpy
import zmq
msgpack_numpy.patch()

class Listener(object):
    """Simple listener."""
    def __init__(self, socket, buf):
        self._socket = socket
        self._zmq_context = zmq.Context()
        self._zmq_request = self._zmq_context.socket(zmq.REQ)
        self._zmq_request.connect(self._socket)
        self._buf = buf
        self._running = False

    def get_data(self):
        """Receive data packets over the network"""
        self._zmq_request.send(b'next')
        return  msgpack.loads(self._zmq_request.recv())

    def write_data(self, data):
        """Write data into the ringbuffer"""
        print('Wrote %d bytes' % (len(data)))
    
    def start(self):
        print("Starting...")
        self._running = True
        while(self._running):
            self.write_data(self.get_data())

    def stop(self):
        self._running = False

agipd_listener = lambda *args: AGIPDListener(*args).start()        
class AGIPDListener(Listener):
    def __init__(self, *args, **kwargs):
        Listener.__init__(self, *args, **kwargs)
    def get_pulse_data(self, obj, pos):
        img = np.rollaxis(obj['image.data'][:,:,:,pos], 2)
        img = np.ascontiguousarray(img.reshape((img.shape[0], 1, img.shape[1], img.shape[2])))
        return img
    def get_pulse_time(self, obj, pos):
        timestamp = obj['metadata']['timestamp']
        return str(timestamp['sec'] + timestamp['frac'] * 1e-18 + pos * 1e-2)
    def write_data(self,data):
        train = data['SPB_DET_AGIPD1M-1/DET/3CH0:xtdf']
        for p in range(2,64-2,2):
            pulse_data = self.get_pulse_data(train, p)
            pulse_time = self.get_pulse_time(train, p)
            self._buf[pulse_time] = pulse_data

slowdata_listener = lambda *args: SlowDataListener(*args).start()            
class SlowDataListener(Listener):
    def __init__(self, *args, **kwargs):
        Listener.__init__(self, *args, **kwargs)
    def write_data(self,data):
        print(data)

# Testing
def main():
    listener = Listener('tcp://localhost:4500', {})
    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()
        print("Exiting...")

if __name__ == '__main__':
    main()
