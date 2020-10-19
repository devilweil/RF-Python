# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 23:49:46 2020

@author: LW
"""

import matplotlib.pyplot as plt
import pylab
import cv2
import numpy as np
import datetime
from osgeo import gdal,gdal_array,osr, ogr
import os,sys 
import glob
from skimage import io

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
    fil = np.array([[ 1,1,1],                        #这个是设置的滤波，也就是卷积核
                [ 1,1,1],
                [ 1,1,1]])

    ###设定工作空间
    os.chdir(r'H:\gansu\wuwei\待滤波数据')
    dirList = sorted(glob.glob('*.tif'))
    indice=len(dirList)
    
    ####获取非标签原始影像的属性信息
    ds=gdal.Open(dirList[0])
    ###获取放射变换信息
    transform = ds.GetGeoTransform()
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    cols=ds.RasterXSize
    rows=ds.RasterYSize
    ###循环加载同一个指数的遥感影像
    imgDataSet=[]
    maxs=0
    for i in range(indice):
        print('Image is readed in ',i)
        tifs=io.imread(dirList[i])
        tifs=tifs.astype('float32')
#        res = cv2.filter2D(tifs,-1,fil)                      #使用opencv的卷积函数,当ddepth=-1时，表示输出图像与原图像有相同的深度。
#        res = cv2.medianBlur(tifs,5)
        #后面两个数字：空间高斯函数标准差，灰度值相似性标准差
        res = cv2.bilateralFilter(tifs,3,75,75)
#        res = cv2.GaussianBlur(tifs,(5,5),0)
        #导出到TI F中
        savePath=r'H:\gansu\wuwei\结果滤波\\gs55'+dirList[i]
        write_imgArray(savePath,cols,rows,transform,res)
    
    
    
    endtime=datetime.datetime.now()
    print('Complete, time spends  ',endtime-starttime)
