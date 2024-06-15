from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import netCDF4 as nc
import numpy as np
import os
import tqdm
from config import Config

# class Config:
#     username = 'root'
#     password = '012704'
#     host = 'localhost'
#     port = '3306'
#     database_name = 'seatemp'

#     # 创建数据库URL
#     SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     BOOTSTRAP_SERVE_LOCAL = True
#     SECRET_KEY= "ahsdilwjaidajldjawlidjal"

#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_COMMIT_TEARDOWN = True
#     @staticmethod
#     def init_app(app):
#         pass

app1=Flask(__name__)
app1.config.from_object(Config)
db=SQLAlchemy(app1)
session=db.session

class Time(db.Model):
    __tablename__ = 'time'
    id = db.Column(db.Integer, primary_key=True,nullable=False , autoincrement=True)
    time = db.Column(db.String(7),nullable=False)

class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    lev = db.Column(db.Float,nullable=False)

class Latitude(db.Model):
    __tablename__ = 'latitude'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    lat = db.Column(db.Integer, nullable=False)

class Longitude(db.Model):
    __tablename__ = 'longitude'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    lon = db.Column(db.Integer,nullable=False)

class SST(db.Model):
    __tablename__ = 'sst'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(7),nullable=False)
    lev= db.Column(db.Float,nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lon = db.Column(db.Integer,nullable=False)
    sst = db.Column(db.Float, nullable=True)
    ssta = db.Column(db.Float, nullable=True)

def load_data(src):
    with open(src,"r",encoding="utf-8") as f:
        datas=json.load(f)
    return datas

def insert_lat(key_fp):
    with open(key_fp,"r") as f:
        for value in json.load(f):
            new_lat=Latitude(lat=value)
            session.add(new_lat)
        session.commit()

def insert_lon(key_fp):
    with open(key_fp,"r") as f:
        for value in json.load(f):
            new_lon=Longitude(lon=value)
            session.add(new_lon)
        session.commit()

def insert_lev(key_fp):
    with open(key_fp,"r") as f:
        for value in json.load(f):
            new_lev=Level(lev=value)
            session.add(new_lev)
        session.commit()

def insert_sst(sst_dir):
    for sst_fp in tqdm.tqdm([f"{sst_dir}/{file}" for file in os.listdir(sst_dir)]):

        dataset = nc.Dataset(sst_fp, 'r')
        basename=os.path.basename(sst_fp)
        date=basename.split(".")[1]
        date=f"{date[:4]}-{date[4:]}"
        new_time=Time(time=date)
        session.add(new_time)
        lev=dataset.variables["lon"][0]

        ssts=dataset.variables["sst"][:]
        sstas=dataset.variables["ssta"][:]

        lats=dataset.variables["lat"][:]
        lons=dataset.variables["lon"][:]

        for i,lat in enumerate(lats):
            for j,lon in enumerate(lons):
                # print(type(ssts[0][0][i][j]))
                # input()
                session.add(
                    SST(
                        time=date,
                        lev=lev,
                        lat=lat,
                        lon=lon,
                        sst=None if ssts[0][0][i][j] is np.ma.masked else ssts[0][0][i][j],
                        ssta=None if sstas[0][0][i][j] is np.ma.masked else sstas[0][0][i][j]
                    )
                )
        session.commit()


def init():
    # 初始化数据库
    db.drop_all()
    db.create_all()
    
    insert_lon("data/keys/lon.json")
    insert_lev("data/keys/lev.json")
    insert_lat("data/keys/lat.json")
    insert_sst(
        "data/ERSST"
    )



if __name__=="__main__":
    init()