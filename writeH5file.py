import h5py
import numpy as np
import linecache
import os

path ='/home/lq/DATA/VOCdevkit/indoor/label'

def createH5Label(label,array,filename):
    
    f = h5py.File(filename,'w')
    f[label] = np.array([array])
    
    #f.create_dataset(label, (4,), 'i')
    
    #f[label] = narray


def readtxt(filename):
    string=linecache.getline(filename,2) 
    
    string1 = string.split('\n')[0]

    stl=string1.split(' ')      

    label = stl[0]
 
    array = np.array(stl[1:])
    
    array = processRct(array)
 
    return label,array


def test(num):
    
    filename = path +'/' +num +'.txt'
    filename1 = path + '/' + num +'.h5'
    label, array= readtxt(filename)
    createH5Label(label, array, filename1)
    print(array)



def processRct(array):
    x = int(array[0])
    y = int(array[1])
    w = int(array[2]) - x
    h = int(array[3]) - int(array[1])
    return np.array([x,y,w,h])

def main():
    for i in os.listdir(path):
        filen = path + '/' + i
        label, array = readtxt(filen)
        name = i.split('.txt')[0]
        filename = '/home/lq/DATA/VOCdevkit/indoor/H5/' + name + '.h5'
        createH5Label(label, array,filename)



if __name__ =='__main__':
#    test('1')
    main()

