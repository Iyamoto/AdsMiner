import pymysql
import configparser

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

host = config['MYSQL']['host']
user = config['MYSQL']['user']
password = config['MYSQL']['pass']
db = config['MYSQL']['db']

try:
    conn = pymysql.connect(host, user, password, db)
except:
    print('Cant connect to db')
    assert False

##cursor = db.cursor()
##
##sql = """INSERT INTO sites(domain)
##        VALUES ('%(name)s')
##        """%{"name":domain}
##cursor.execute(sql)


conn.close()    
