# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 18:54:28 2020

@author: LW
"""
from osgeo import gdal,gdal_array,osr, ogr
import numpy as np
import os 
from skimage import io
import cv2
import datetime
from numpy import nan as NaN
import pandas as pd

lable_path=r'H:\gansu\wuwei\Rectangle\分类数据\complexResult-090.tif'
non_label_file_path=r'H:\gansu\wuwei\Rectangle\分类数据\complexResult-090.tif'#+vi+'_2019.tif' 20190423_S2A.tif

def combineImage(imgList):
    ####获取非标签原始影像的属性信息
    non_lable_ds=gdal.Open(lable_path)
    ###获取放射变换信息
    non_lable_transform = non_lable_ds.GetGeoTransform()
#    non_lable_xOrigin = non_lable_transform[0]
#    non_lable_yOrigin = non_lable_transform[3]
    non_lable_pixelWidth = non_lable_transform[1]
    non_lable_pixelHeight = non_lable_transform[5]
    non_lable_cols=non_lable_ds.RasterXSize
    non_lable_rows=non_lable_ds.RasterYSize
    outimg=np.zeros((non_lable_rows,non_lable_cols))
    outimg[outimg==0]=NaN
    
#    outimg[0:2,0:1]=1
    del non_lable_ds
    jpgwidth=32   ###224
    
    ###循环赋值
    for img in imgList:
        temp=img.split('.')[0]
        r,c,predType=temp.split('-')[0],temp.split('-')[1],temp.split('-')[2]
        print('r,c,predType are ',r,c,predType)
        non_lable_xOffset = int(c)*jpgwidth
        non_lable_yOffset = int(r)*jpgwidth
        outimg[non_lable_yOffset:(non_lable_yOffset+jpgwidth),non_lable_xOffset:(non_lable_xOffset+jpgwidth)]=int(predType)  
    
    #导出到TIF中
    savePath=r'H:\gansu\wuwei\Rectangle\RectangleTIFF\rectangle90-32.tif'
    write_imgArray(savePath,non_lable_cols,non_lable_rows,non_lable_transform,outimg)

def combineImageByConstructIndex(imgList):
    ####获取非标签原始影像的属性信息
    non_lable_ds=gdal.Open(lable_path)
    ###获取放射变换信息
    non_lable_transform = non_lable_ds.GetGeoTransform()
#    non_lable_xOrigin = non_lable_transform[0]
#    non_lable_yOrigin = non_lable_transform[3]
    non_lable_pixelWidth = non_lable_transform[1]
    non_lable_pixelHeight = non_lable_transform[5]
    non_lable_cols=non_lable_ds.RasterXSize
    non_lable_rows=non_lable_ds.RasterYSize
    outimg=np.zeros((non_lable_rows,non_lable_cols))
    outimg[outimg==0]=NaN
    
#    outimg[0:2,0:1]=1
    del non_lable_ds
    jpgwidth=32   ###224
    
    ###循环赋值
    for imgs in imgList:
        for img in imgs:
            temp=img.split('.')[0]
            r,c,predType=temp.split('-')[0],temp.split('-')[1],temp.split('-')[2]
            print('r,c,predType are ',r,c,predType)
            non_lable_xOffset = int(c)*jpgwidth
            non_lable_yOffset = int(r)*jpgwidth
            outimg[non_lable_yOffset:(non_lable_yOffset+jpgwidth),non_lable_xOffset:(non_lable_xOffset+jpgwidth)]=int(predType)  
    
    #导出到TIF中
    savePath=r'H:\gansu\wuwei\Rectangle\RectangleTIFF\rectangleByConstructIndex90-32.tif'
    write_imgArray(savePath,non_lable_cols,non_lable_rows,non_lable_transform,outimg)


        
def write_imgArray(filename,im_width,im_height,im_geotrans,im_data):
    # 生成影像
    dataset = gdal.GetDriverByName('GTiff').Create(filename, xsize=im_width, ysize=im_height, bands=1,
                                                     eType=gdal.GDT_Float32)#gdal.GDT_Float32   GDT_CInt16

    proj = osr.SpatialReference()
    proj.SetWellKnownGeogCS("WGS84"); 
    dataset.SetGeoTransform(im_geotrans)              #写入仿射变换参数
    dataset.SetProjection(proj.ExportToWkt())         #写入投影
    dataset.GetRasterBand(1).WriteArray(im_data)  #写入数组数据
   
    del dataset       

                
if __name__ == "__main__": 
    
    starttime=datetime.datetime.now() 
#    os.chdir(r'H:\gansu\wuwei\Rectangle\SplitImage32')
    #####不构建索引进行外接多边形TIF影像化
#    imglist=os.listdir(r'H:\gansu\wuwei\Rectangle\SplitImage90_32')
#    
#    combineImage(imglist)
    
    ###构建索引后的外接多边形tif影像化
#    imglist=np.loadtxt(r'H:\gansu\wuwei\Rectangle\外接多边形TXT\Rectangle.txt')
    #read txt method one
    imglist=[]
    f = open(r'H:\gansu\wuwei\Rectangle\外接多边形TXT\Rectangle.txt')
    lines = f.readlines()
#    imglist=pd.read_csv(r'H:\gansu\wuwei\Rectangle\外接多边形TXT\Rectangle.csv',header=None)
    for line in lines:
        lists=line.split(',')
        lists[0]=lists[0].split('[')[1]
        lists[len(lists)-1]=lists[len(lists)-1].split(']')[0]
        ####去除包含的空格和‘的符号
        temp=[]
        for li in lists:
            temp.append(li.split('\'')[1])
        
        imglist.append(temp)
    
    combineImageByConstructIndex(imglist)
    
    
    endtime=datetime.datetime.now()
    print('Complete, time spends  ',endtime-starttime)
