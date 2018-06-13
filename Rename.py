import os
import linecache
#path ='/home/lq/mydata/sourceData/Annotation_files/'

#for files in os.listdir(path):
#    oldname = path + files
#    cur = files.split('(')
#    cur1 = cur[1].split(')')[0]
#    newname = path + str(cur1) + '.txt'
#    os.rename(oldname, newname)
#    print(oldname)

def Rename(basenum, Dirname, Type):
    

    for filename in os.listdir(Dirname):
        strNum=filename.split('.')[0]
        num = int(strNum) - basenum  
        #newname = str(num).zfill(6) + Type
        newname = str(num) + Type
        newname = Dirname + '/' + newname
        oldname = Dirname + '/' + filename
        os.rename(oldname, newname)       

def readBaseNum(fileNum):
    filename="/home/lq/mydata/sourceData/1/" + str(fileNum) + '.txt'
    string = linecache.getline(filename, 1)
    basenum = int(string.split(' ')[1] )
    return basenum    




def main():
    Dirname = '/home/lq/mydata/extractData/images'
    Dirname1 = '/home/lq/mydata/extractData/label'
    for i in range(1, 49):
        dirImg = Dirname + "/" + "video"+str(i)
        dirLabel =  Dirname1 +'/' + "video"+str(i)
        basenum = readBaseNum(i)   
        if basenum <= 0:
            continue
        Rename(basenum,dirImg, '.jpg')
        Rename(basenum, dirLabel, '.txt') 


#Dirname = '/home/lq/data/VOCdevkit/indoor/JPEGImages'
#Rename(0, Dirname, '.jpg')


Dirname = '/home/lq/data/VOCdevkit/indoor/label'
Rename(0, Dirname, '.txt')





