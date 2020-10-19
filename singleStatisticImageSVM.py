# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:34:48 2020

@author: LW
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 19:48:14 2020

@author: LW
"""
from osgeo import gdal,gdal_array,osr, ogr
import os,sys 
import glob
import numpy as np
import random
import random
from skimage import io

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

#获取样本点列表
def getSHPPoint(pointPath):
    #############获取矢量点位的经纬度
    #设置driver
    driver=ogr.GetDriverByName('ESRI Shapefile')
    #打开矢量
    ds=driver.Open(pointPath, 0)
    if ds is None:
        print('Could not open ' +'shapefile')
        sys.exit(1)
        #获取图层
    layer = ds.GetLayer()

    #获取要素及要素地理位置
    xyValues = []
#    yValues = []
    feature = layer.GetNextFeature()
    while feature:
        geometry = feature.GetGeometryRef()
        x0 = geometry.GetX()
        y0 = geometry.GetY()
        xyValues.append([[x0,y0]])
#        yValues.append(y)  
        feature=layer.GetNextFeature()    
    del ds,driver
    return xyValues

 #获取样本点的行列号
def getSampleRowCols(imagePath,pixellist,value):
    #打开栅格数据
    ds = gdal.Open(imagePath,gdal.GA_ReadOnly)
    if ds is None:
        print('Could not open image')
        sys.exit(1)
    #获取行列、波段
#    rows = ds.RasterYSize
#    cols = ds.RasterXSize
#    bands = ds.RasterCount
    #获取放射变换信息
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    colsMax=ds.RasterXSize
    rowsMax=ds.RasterYSize
    relist=[]
    #
    for f in range(len(pixellist)):
        x1 = pixellist[f][0][0]
        y1 = pixellist[f][0][1]
        #获取点位所在栅格的位置
        rows = int((y1-yOrigin)/pixelHeight)
        cols = int((x1-xOrigin)/pixelWidth)
        if rows<0 or rows>=rowsMax:
            continue
        if cols<0 or cols>=colsMax:
            continue
        pixellist[f].append([rows,cols])
        relist.append([rows,cols,value])
    del ds
    return pixellist,relist  

def readImageBySample(samples,reftif):
    ###根据样本的行列号
    tifs=io.imread(refimage)
    print(tifs.shape)
    x=[]
    y=[]
    for i in range(len(samples)):
        r=samples[i][0]
        c=samples[i][1]
        v=samples[i][2]
        ###由于随机森林需要的是2D的数据，因此本文采用补0处理
        x.append([tifs[r][c],0])
        y.append(v)
    
    del tifs
    return x,y

def readSingleImageMultiVIBySample(samples,refimage):
    
    os.chdir(r'H:\gansu\wuwei\S2-Statisitic')
    dirList = sorted(glob.glob('CTVI*.tif'))
    indice=len(dirList)
    ###根据样本的行列号
    tifs=io.imread(refimage)
    print(tifs.shape)
    x=[]
    y=[]
    for i in range(len(samples)):
        r=samples[i][0]
        c=samples[i][1]
        v=samples[i][2]
        ###由于随机森林需要的是2D的数据，因此本文采用补0处理
        x.append([tifs[r][c],0])
        y.append(v)
    
    del tifs
    return x,y

def predictImage(clt,reftif):
    tifs=io.imread(refimage)
    
    print(tifs.shape)
    rs,cs=tifs.shape[0],tifs.shape[1]
    rc=[]
    
    for r in range(rs):
        print('正在执行：',r,'行')
        temp=[]
        for c in range(cs):
            temp.append([tifs[r][c],0])
#            pred=np.array()pred.reshape(1, -1)  
        rcpred=clt.predict(temp)
#        pred=[]
#        for p in rcpred:
#            if p[1]>p[0]:
#                if p[1]>0.9:
#                    pred.append(1)
#                else:
#                    pred.append(0)
#            else:
#                pred.append(0)
        rc.append(rcpred)
    del tifs
    return rc

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
    
    # 获取样本行列号
    print('Loading grape sample')
    grapeSample=r'F:\代码资源\CNN\分类样本\武威\葡萄\grapepoint.shp'
    grape = getSHPPoint(grapeSample)

    print('Loading nonGrape sample')
    nonGrapeSample=r'F:\代码资源\CNN\分类样本\武威\非葡萄\nongrapepoint.shp'
    nongrape = getSHPPoint(nonGrapeSample)
    nongrape=random.sample(nongrape,250000)

    print('Loading OSMData sample')
    osmNonGrapeSample=r'F:\代码资源\CNN\分类样本\武威\OSM\roadandwater_buffer_point.shp'
    osmnongrape = getSHPPoint(osmNonGrapeSample)
    osmnongrape=random.sample(osmnongrape,250000)

    ####获取单景统计影像的分类结果
    refimage=r'H:\gansu\wuwei\S2-Statisitic\CTVI_MAX_2019.tif'
    
    grapeRC1,X1=getSampleRowCols(refimage,grape,1)
    grapeRC2,X2=getSampleRowCols(refimage,nongrape,0)
    grapeRC3,X3=getSampleRowCols(refimage,osmnongrape,0)
    
    X=np.vstack((X1,X2,X3))
    print(len(X))
    
    print('读取统计image的样本点')
    
    x,y=readImageBySample(X,refimage)
    
    print('SVM.....')
#    maxdata=x[~np.isnan(x)].max()
#    x[np.isnan(x)]=maxdata
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    
    print('Progressing SVM...')
    #,n_estimators=150
#    clf = RandomForestClassifier(n_jobs=-1,random_state=0,n_estimators=200)
    clf= make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(x_train, y_train)
    
    print(' SVM has trainned ')
#    print(clf.feature_importances_) 
    y_pred=clf.predict(x_test)
    print(confusion_matrix(y_test, y_pred))
    print(clf.score(x_test, y_test))
    
    ####进行预测
    outimage=predictImage(clf,refimage)
    outimage=np.array(outimage)
    print(outimage.shape)
    ###保存预测后的结果
    ####获取非标签原始影像的属性信息
    ds=gdal.Open(refimage)
    ###获取放射变换信息
    transform = ds.GetGeoTransform()
#    non_lable_xOrigin = non_lable_transform[0]
#    non_lable_yOrigin = non_lable_transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    cols=ds.RasterXSize
    rows=ds.RasterYSize
    
    #导出到TIF中
    savePath=r'H:\gansu\wuwei\预测结果\predict-singleimage-svm.tif'
    write_imgArray(savePath,cols,rows,transform,outimage)

    del ds
    
    print('Complete')
    
    