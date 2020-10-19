# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 15:30:50 2020

@author: LW
"""
from osgeo import gdal,gdal_array,osr, ogr
import os,sys 
import glob
from skimage import io
import datetime


def PolygonizeTheRaster():
    inputfile = r'H:/gansu/wuwei/Rectangle/RectangleTIFF/rectangle90-32.tif'
    ds = gdal.Open(inputfile, gdal.GA_ReadOnly)
    srcband=ds.GetRasterBand(1)
    maskband=srcband.GetMaskBand()
    
    dst_filename='H:/gansu/wuwei/Rectangle/RectangleTIFF/TifToSHP/rectangle90-32.shp'
    drv = ogr.GetDriverByName('ESRI Shapefile')
    dst_ds = drv.CreateDataSource(dst_filename)
    srs = None
    
    dst_layername = 'out'
    dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
    dst_fieldname = 'DN'
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    dst_field = 0
#    prog_func =test()
    options=[]
    # 参数  输入栅格图像波段\掩码图像波段、矢量化后的矢量图层、需要将DN值写入矢量字段的索引、算法选项、进度条回调函数、进度条参数
    gdal.Polygonize(srcband, maskband, dst_layer,dst_field, options)

if __name__ == "__main__": 
    
    starttime=datetime.datetime.now()
    
    PolygonizeTheRaster()
    
    endtime=datetime.datetime.now()
    print('Complete, time spends  ',endtime-starttime)

