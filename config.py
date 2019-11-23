import os
basedir = os.path.abspath(os.path.dirname(__file__))
# DIALECT = 'mysql'
# DRIVER = 'mysqldb'
# USERNAME = 'root'
# PASSWORD = 'root'
# HOST = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'db_demo1'
class Config(object):



    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # sqlite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # mysql
    # SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST
    #                                                                    , PORT, DATABASE)
    heck_same_thread=False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 25
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['jxjjyekang@163.com']
    # 搜索框
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
