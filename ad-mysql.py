import MySQLdb
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
pass = config['MYSQL']['pass']
db = config['MYSQL']['db']

try:
    db = MySQLdb.connect(host, user, pass, db, charset='utf8')
except:
    print('Cant connect to db')
    assert False

##cursor = db.cursor()
##
##sql = """INSERT INTO contacts(name, mail, adres, tel)
##        VALUES ('%(name)s', '%(mail)s', '%(adres)s', '%(tel)s')
##        """%{"name":fname, "mail":fmail, "adres":fadres, "tel":ftel}
##cursor.execute(sql)


db.close()    
