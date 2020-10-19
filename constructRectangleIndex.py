# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 19:43:57 2020
外接矩形的索引构建
@author: LW
"""
import numpy as np
import os,sys 
import glob
import datetime

def getNearPNG(row,col):
    ####返回3*3的中心像素的临近8像素
    t=str(int(row)-1)+'-'+str(int(col))+'-1.png'
    l=str(int(row))+'-'+str(int(col)-1)+'-1.png'
    r=str(int(row))+'-'+str(int(col)+1)+'-1.png'
    b=str(int(row)+1)+'-'+str(int(col))+'-1.png'
    lt=str(int(row)-1)+'-'+str(int(col)-1)+'-1.png'
    lb=str(int(row)+1)+'-'+str(int(col)-1)+'-1.png'
    rt=str(int(row)-1)+'-'+str(int(col)+1)+'-1.png'
    rb=str(int(row)+1)+'-'+str(int(col)+1)+'-1.png'
    return t,l,r,b,lt,lb,rt,rb 

def checkExistPNG(r,c,imglist,tempRectangle):
    ###判断是否存在，存在加进数组，不存在新建数组,进行邻近的8像素循环
    top,left,right,bottom,ltop,lbottom,rtop,rbottom=getNearPNG(r,c)
    if top in imglist and top not in tempRectangle:
        tempRectangle.append(top)
        checkExistPNG(r-1,c,imglist,tempRectangle)
    if left in imglist and left not in tempRectangle:
        tempRectangle.append(left)
        checkExistPNG(r,c-1,imglist,tempRectangle)    
    if right in imglist and right not in tempRectangle:
        tempRectangle.append(right)
        checkExistPNG(r,c+1,imglist,tempRectangle) 
    if bottom in imglist and bottom not in tempRectangle:
        tempRectangle.append(bottom)
        checkExistPNG(r+1,c,imglist,tempRectangle) 
    if ltop in imglist  and ltop not in tempRectangle:
        tempRectangle.append(ltop)
        checkExistPNG(r-1,c-1,imglist,tempRectangle) 
    if lbottom in imglist and lbottom not in tempRectangle:
        tempRectangle.append(lbottom)
        checkExistPNG(r+1,c-1,imglist,tempRectangle) 
    if rtop in imglist and rtop not in tempRectangle:
        tempRectangle.append(rtop)
        checkExistPNG(r-1,c+1,imglist,tempRectangle) 
    if rbottom in imglist and rbottom not in tempRectangle:
        tempRectangle.append(rbottom)
        checkExistPNG(r+1,c+1,imglist,tempRectangle) 
        
        
def ConstructRectangleIndex():
    
    imglist=os.listdir(r'H:\gansu\wuwei\Rectangle\SplitImage90_32')
    
    ###构建矩形的索引
    indexRectangle=[]
    for imgs in imglist:
        temp=imgs.split('.')[0]
        r,c,types=temp.split('-')[0],temp.split('-')[1],temp.split('-')[2]
        print('r,c,types are ',r,c,types)
        tempRectangle=[]
        ###判断是否包含葡萄地块,有，则继续下一步操作，无，继续下一个循环
        if types=='0':
            continue
        
        ###从第一个包含葡萄信息的照片开始，把所有连通的照片找出来，保存到数组中,需要不断的迭代，直至结束
        isExist=False
        for index in indexRectangle:
            if imgs in index:
                isExist=True
                break
        
        if isExist:
            continue
        else:
            tempRectangle.append(imgs)
        
        checkExistPNG(int(r),int(c),imglist,tempRectangle)
        
        indexRectangle.append(tempRectangle)
        
    return indexRectangle
        
    
if __name__ == "__main__": 
    
    starttime=datetime.datetime.now()
    
    indexRectangle=ConstructRectangleIndex()
    indexRectangle=np.array(indexRectangle)
    ###保存外接多边形
    savePath=r'H:\gansu\wuwei\Rectangle\外接多边形TXT\Rectangle.txt'
    np.savetxt(savePath, indexRectangle,fmt='%s')  ###delimiter = ',',fmt='%s'
    
    endtime=datetime.datetime.now()
    print('Complete, time spends  ',endtime-starttime)


