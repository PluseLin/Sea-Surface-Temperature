import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config:
    username = 'root'
    password = '012704'
    host = 'localhost'
    port = '3306'
    database_name = 'seatemp'

    # 创建数据库URL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY= "ahsdilwjaidajldjawlidjal"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    pass

config={
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}
