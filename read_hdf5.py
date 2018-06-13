import h5py
import numpy as np
f = h5py.File('/home/lq/DATA/VOCdevkit/indoor/H5/1.h5','r')

print f.keys()


print(f['normal'][:])

