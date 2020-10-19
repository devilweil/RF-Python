# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:28:17 2020

@author: LW
"""

from osgeo import gdal,gdal_array,osr, ogr
import numpy as np
 
from skimage import io
import cv2
import datetime


lable_path=r'H:\gansu\wuwei\Rectangle\分类数据\complexResult-090.tif'
non_label_file_path=r'H:\gansu\wuwei\Rectangle\分类数据\complexResult-090.tif'#+vi+'_2019.tif' 20190423_S2A.tif

def getSplitImageAndImageByMutilBands():

    ####获取非标签原始影像的属性信息
    non_lable_ds=gdal.Open(non_label_file_path)
    ###获取放射变换信息
#    non_lable_transform = non_lable_ds.GetGeoTransform()
#    non_lable_xOrigin = non_lable_transform[0]
#    non_lable_yOrigin = non_lable_transform[3]
#    non_lable_pixelWidth = non_lable_transform[1]
#    non_lable_pixelHeight = non_lable_transform[5]
    non_lable_cols=non_lable_ds.RasterXSize
    non_lable_rows=non_lable_ds.RasterYSize
    
#    non_lable_ds_ref=io.imread(non_label_file_path)
#    print(non_lable_ds_ref.shape)

    ####获取标签影像的属性信息

    jpgwidth=32   ###224
    
    
    rowImageCount=int(non_lable_rows/jpgwidth)
    colImageCount=int(non_lable_cols/jpgwidth)
    print('行照片数',rowImageCount,'列照片数',colImageCount)

    for r in range(rowImageCount):
        for c in range(colImageCount):
            print('导出第',r,'行',c,'列')
            ###获取非标签位置
            non_lable_xOffset = c*jpgwidth
            non_lable_yOffset = r*jpgwidth
            
            non_lableArray_B1=non_lable_ds.GetRasterBand(1).ReadAsArray(non_lable_xOffset,non_lable_yOffset,jpgwidth,jpgwidth)

            count=np.sum(non_lableArray_B1 == 1)
            scale=count/(jpgwidth*jpgwidth)
            
            non_lableArray = np.zeros((jpgwidth,jpgwidth,3))
            non_lableArray[:,:,0]=non_lableArray_B1
            if scale>0:
                save_non_grape=r'H:\gansu\wuwei\Rectangle\SplitImage90_32\\'+str(r)+'-'+str(c)+'-'+'1'+'.png'
                cv2.imwrite(save_non_grape, non_lableArray)
#                save_label_grape=r'H:/gansu/wuwei/葡萄种植的外接矩形/根据分类结果生成32宽的JPG/Mask/'+str(r)+'-'+str(c)+'-'+'1'+'-mask.png'
#                cv2.imwrite(save_label_grape, lableArray)
            else:
                save_non_grape=r'H:\gansu\wuwei\Rectangle\SplitImage90_32\\'+str(r)+'-'+str(c)+'-'+'0'+'.png'
                cv2.imwrite(save_non_grape, non_lableArray)
                
if __name__ == "__main__": 
    
    starttime=datetime.datetime.now() 

    getSplitImageAndImageByMutilBands()
    
    endtime=datetime.datetime.now()
    print('Complete, time spends  ',endtime-starttime)

