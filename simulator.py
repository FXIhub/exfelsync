import msgpack
import msgpack_numpy
msgpack_numpy.patch()
import numpy as np
from time import sleep, time
import sys, os
from threading import Thread
import zmq
import pickle
import copy


_TRAINS = [i for i in range(1455918683, 1455918699)]
_PULSES = 64
_SAVED_PULSES = int((64-2)/2)
_MODULES = 16
_MOD_X = 512
_MOD_Y = 128
_SHAPE = (_SAVED_PULSES, _MODULES, _MOD_X, _MOD_Y)
#_SHAPE = (_MOD_X, _MOD_Y, 2, _PULSES)

data_file = "/gpfs/exfel/exp/SPB/201701/p002013/usr/ekeberg/data_simulation_template/dump_3ch0.p"
data_file = "/Users/ekeberg/Work/Beamtimes/XFEL2013/xfel2013/scripts/dump_3ch0.p"

with open(data_file, "rb") as file_handle:
    data_dict = pickle.load(file_handle)
    

def sender(source, port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:{}'.format(port))
    local_data_dict = copy.deepcopy(data_dict)

    counter = 0
    while True:
        msg = socket.recv()
        if msg == b'next':
            local_data_dict["SPB_DET_AGIPD1M-1/DET/3CH0:xtdf"]["header.trainId"] = counter
            print(local_data_dict["SPB_DET_AGIPD1M-1/DET/3CH0:xtdf"]["header.trainId"])
            socket.send(msgpack.dumps(local_data_dict))
            print("sending data at port {}".format(port))
            counter += 1
        else:
            print('wrong request')
            break
    else:
        socket.close()
        context.destroy()


if __name__ == '__main__':
    source = 'SPB_DET_AGIPD1M-1/DET/3CH0:xtdf'
    #source = 'SPB_DET_AGIPD1M-1/DET'
    # port = 4600
    # sender(source, port)

    t0 = Thread(target=sender, args=(source, 4600,))
    t1 = Thread(target=sender, args=(source, 4601,))
    t2 = Thread(target=sender, args=(source, 4602,))
    t0.start()
    t1.start()
    t2.start()
