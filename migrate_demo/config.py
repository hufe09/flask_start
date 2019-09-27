DEBUG = True

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_demo'


SQLALCHEMY_DATABASE_URI = \
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE} \
        ?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
