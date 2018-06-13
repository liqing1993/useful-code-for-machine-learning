#coding:utf-8
import os
import linecache   
import shutil

#filename ="my.txt"
sourceDir="/home/lq/mydata/sourceData/"
destDir = "/home/lq/mydata/extractData/"

#def readStart2EndFrame(filename):    #读取文件两行
    #f=open("filename",'r')
#   dirpath = sourceDir + "1/" + filename    
#    startLine = linecache.getline(dirpath,1)   

    #cur = startLine.split('\n')
    #cur1 = cur[0].split(',')
    #print(cur1)
    #startLine = f.readline()
#    endLine = linecache.getline(dirpath, 2)
    #endLine = f.readline()
#    start = startLine.split("\n")[0]   #将行中的换行符号\n去掉
    
#    end = endLine.split("\n")[0]

#    return [start, end] 


def readTXTline(filename, line_num):
    
    dirpath = sourceDir + "1/" + filename    
    Line = linecache.getline(dirpath,line_num)   
    start = int(Line.split(' ')[0])
    end = int(Line.split(' ')[1])
    return [start, end]


#def getFileLine(filePath):
#    f = open(filePath)
#    length=len(f.readlines())
#    return length


#def normalInterval(filePath, filename):
#    length = getFileLine(filePath)
#    cur =  readStart2EndFrame(filename)
#    normalInterval = [0,0]

#    if(length > int(cur[0])+2):
#        normalInterval[0] = int(cur[0]) + 2       
#        normalInterval[1] = length 
#    else:
#        pass 
#    return normalInterval




#def creatFileforLabel(start2endlist, filename):   #将readStart2EndFrame()函数输出区间对应行读取到新文件中
#    destfile = destDir + '1/' + filename
#    srcfile = sourceDir + '1/' + filename
#    f = open(destfile, "a+") 
#    for i in range(int(start2endlist[0])+2, int(start2endlist[1])+3):
#        curline = linecache.getline(srcfile, i)
#        f.write(curline)
       # f.write('\n')
#    f.close()  



def moveImg(curD, destD,nameInterval):
    source= os.path.join(sourceDir,curD)
    target = os.path.join(destDir,destD)
    print(source)
   # if os.path.isfile(sourceFile) and os.path.isfile(targetFile)
     #   print("source file or target file don't exit,please creat it!")
     #   break
    for img in os.listdir(source):  
        
        name = os.path.splitext(img)[0]
	num = int(name) 
        #if num>=int(nameInterval[0]) and num<=int(nameInterval[1]):
        if num>=nameInterval[0] and num<=nameInterval[1]:
         #   name = os.path.splitext(img)[0]    #将文件名前缀提取出来
         #  Type = os.path.splitext(img)[1]     #将文件后缀提取出来
         #   src = source + img + zfill(7) + Type   #将文件名设置为7位，不包含后缀，不够在文件名前补0
         #   dest = target + ima + zfill(7) +Type
            src = source +'/' + img
            dest = target + '/'+img
            print(src)
            shutil.copy(src, dest)    #将文件从源文件夹拷贝到目的文件夹


def creatLabelOfFoll_down(fallingInterval, video_num):
    newDirname = "video"+str(video_num) 
    os.mkdir("/home/lq/mydata/extractData/label/"+newDirname)
    dirpath = destDir + "label/"+ newDirname +'/'    
    srcfile = sourceDir + 'Annotation_files/'  +  str(video_num) +'.txt'
    
    for i in range(fallingInterval[0]+2, fallingInterval[1]+3):
        newfile = dirpath + str(i-2) +".txt"

        fw = open(newfile, 'a+')                 
        fw.write('1\n')
        	
        Line = linecache.getline(srcfile,i)  #读取文件srcfile中到第i行 
       # print(Line)
        	
        cur = Line.split('\n')      #去掉该行行尾到换行符号
        cur1 = cur[0].split(',')     #将该行以逗号为分隔符区分开，得到纯数字字符数组
       # print(cur1)
        words = "falling_down" + ' '  + cur1[2] +' ' +cur1[3] +' ' + cur1[4] + ' ' + cur1[5]
        fw.write(words)
        fw.close() 




def creatLabelOfnormal(normalInterval, video_num):
    dirpath = destDir + "label/" + "video" + str(video_num) +'/' 
    srcfile = sourceDir + 'Annotation_files/' +  str(video_num) + '.txt'
    
    for i in range(normalInterval[0]+2, normalInterval[1]+3):
        newfile = dirpath + str(i-2) +".txt"

        fw = open(newfile, 'w+')                 
        fw.write('1\n')
        	
        Line = linecache.getline(srcfile,i)  #读取文件srcfile中到第i行 
        	
        cur = Line.split('\n')      #将Line字符串以'\n'分开
        cur1 = cur[0].split(',')     #将该行以逗号为分隔符区分开，得到纯数字字符数组
       # print(cur1)
        words = "normal" + ' '  + cur1[2] +' ' +cur1[3] +' ' + cur1[4] + ' ' + cur1[5]
        fw.write(words)
        fw.close() 










## test1##
#l=readStart2EndFrame("1.txt")
#print(l)
#creatFileforLabel(l, "1.txt")

##test2##
#L=["1","3"]
#moveImg("1","1",L)

##test3##
#l = readStart2EndFrame('1.txt')
#print(l)
#creatLabelOfFoll_down(l, 1)

##test4##

#filePath = sourceDir + 'Annotation_files/' + str(1) + '.txt'
#print(getFileLine(filePath))
#print(normalInterval(filePath, '1.txt'))

##test5##

#filePath = sourceDir + 'Annotation_files/' + str(1) + '.txt'
#interval = normalInterval(filePath, '1.txt')
#creatLabelOfnormal(interval, 1)



##test6##  create label
#for i in range(26, 49):
#    filename = str(i) + '.txt'
#    print(filename)
#    l = readTXTline(filename, 3)  #读取1.txt文件中的第三行，返回fall_down图片序列区间
#    print(l)

#    creatLabelOfFoll_down(l ,i)   #读取视频1中，区间l上的标签，并写入新file

#    l1 = readTXTline(filename, 2)
#    print(l1)
#    creatLabelOfnormal(l1, i)


##test7##
for i in range(1, 49):
    os.mkdir("/home/lq/mydata/extractData/images/"+'video'+str(i))

    filename = str(i) + '.txt'
    Dirname = 'images/' + 'video' + str(i)
    Srcname = 'Coffee_room_01/' +'video' +' ' +'(' + str(i) + ')'
     
    l = readTXTline(filename,2)
    l1 = readTXTline(filename, 3)
    inval = [l[0], l1[1]]
    print(i)
    moveImg(Srcname, Dirname,inval)
    




