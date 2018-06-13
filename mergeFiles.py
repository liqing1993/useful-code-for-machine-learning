import os
import shutil
#merge Dir1 to Dir2 and change name to be  continus number
def mergeImg():
    Dirname1 = '/home/lq/mydata/extractData/images' 
    Dirname2 = '/home/lq/mydata/extractData/images/IMAGES'
    for i in range(1, 49):
        Dir = Dirname1 + '/' + 'video' + str(i)
        basenum2 = len(os.listdir(Dirname2))
        for filename in os.listdir(Dir):
            strNum=filename.split('.')[0]
            num = int(strNum) + basenum2
            newname = str(num).zfill(6) + '.jpg'
            #print(newname)
            src = Dir +'/'+filename
            dest = Dirname2 +'/' +newname
            shutil.copy(src, dest)
        



def mergeLabel():
    Dirname1 = '/home/lq/mydata/extractData/label' 
    Dirname2 = '/home/lq/mydata/extractData/label/LABELS'
    for i in range(1, 49):
        Dir = Dirname1 + '/' + 'video' + str(i)
        basenum2 = len(os.listdir(Dirname2))
        for filename in os.listdir(Dir):
            strNum=filename.split('.')[0]
            num = int(strNum) + basenum2
            newname = str(num).zfill(6) + '.txt'
            #print(newname)
            src = Dir +'/'+filename
            dest = Dirname2 +'/' +newname
            shutil.copy(src, dest)
        




mergeLabel()
