from . import db

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