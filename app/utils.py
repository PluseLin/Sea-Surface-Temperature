from os import name
from . import db
from .models import *
import os
import time
import netCDF4 as nc
import numpy as np
from tqdm import tqdm

session=db.session
FILE_DIRS="app/files"

def query_sst_bytime(time):
    return session.query(SST).filter(SST.time==time).first()

def query_sst(time,lat,lon):
    return session.query(SST).filter(SST.time==time,SST.lat==lat,SST.lon==lon).first()

def upload_sst(sst_file):
    try:
        dataset = nc.Dataset(sst_file, 'r')
    except:
        print(sst_file)
        return "error"
    ssts=dataset.variables["sst"][:]
    sstas=dataset.variables["ssta"][:]
    lats=dataset.variables["lat"][:]
    lons=dataset.variables["lon"][:]
    lev=dataset.variables["lon"][0]

    basename=os.path.basename(sst_file)
    date=basename.split(".")[1]
    date=f"{date[:4]}-{date[4:]}"
    if query_sst_bytime(time=date) is not None:
        dataset.close()
        return "duplicated"
    new_time=Time(time=date)
    session.add(new_time)


    for i,lat in enumerate(lats):
        for j,lon in enumerate(lons):
            # print(type(ssts[0][0][i][j]))
            # input()
            new_sst= SST(
                time=date,
                lev=lev,
                lat=lat,
                lon=lon,
                sst=None if ssts[0][0][i][j] is np.ma.masked else ssts[0][0][i][j],
                ssta=None if sstas[0][0][i][j] is np.ma.masked else sstas[0][0][i][j]
            )
            session.add(
                new_sst
            )
    session.commit()
    dataset.close()
    return "success"

def query_sst_byrange(time,lat_range,lon_range):
    result=session.query(SST).filter(
        SST.time==time,
        lat_range[0]<=SST.lat,
        SST.lat<=lat_range[1],
        lon_range[0]<=SST.lon,
        SST.lon<=lon_range[1]
    ).all()
    return [
        (
            item.time,
            item.lon,
            item.lat,
            item.sst if item.sst is not None else "N/A",
            item.ssta if item.ssta is not None else "N/A"
        )
        for item in result
    ]

def update_sst(time,lat,lon,sst,ssta):
    sst=None if sst=="N/A" or sst is None else sst
    ssta=None if ssta=="N/A" or ssta is None else ssta
    try:
        sst=float(sst)
        ssta=float(ssta)
    except:
        return False,"海洋表面温度(SST)，海表温度异常(SSTA)必须为整数或浮点数！"
    ori_item=session.query(SST).filter(
        SST.time==time,
        SST.lat==lat,
        SST.lon==lon
    ).first()
    if ori_item is None:
        return False,"待修改的温度信息不存在！"
    
    try:
        ori_item.sst=sst
        ori_item.ssta=ssta
        session.commit()
    except:
        return False,"更新失败！"
    return True,"更新成功！"

def delete_sst(time):
    items=session.query(SST).filter(SST.time==time)
    if items.all() == []:
        return 0
    del_num=len(items.all())
    items.delete()
    session.commit()
    return del_num

def pred_sst(lat,lon,month):
    PRED_NUM=5
    items=session.query(SST).filter(SST.lat==lat,SST.lon==lon,SST.time.like(f"%-{month}")).all()
    items=sorted(items,key=lambda x:x.time,reverse=True)
    items=items[:min(len(items),PRED_NUM)]

    sst=0.0
    ssta=0.0
    if len(items)==0:
        return None,None
    for item in items:
        if item.sst is None or item.ssta is None:
            sst=ssta=None
            break
        sst+=item.sst
        ssta+=item.ssta
    if sst is not None:
        sst=sst/len(items)
    if ssta is not None:
        ssta=ssta/len(items)
    return sst,ssta
        