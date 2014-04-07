import pymysql
import configparser

def init_mysqldb():
    """ Connects to mysql db """
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
    return conn

def write2mysql(conn, sql):
    """ executes sql request"""
    cur = conn.cursor()
    cur.execute(sql)
    for response in cur:
        print(response)
    cur.close()
    return

def kill_mysqldb(conn):
    """ Finishes connection to db"""
    conn.close()

conn = init_mysqldb()    

domain = 'ya.ru'
sql = """INSERT INTO sites(domain)
        VALUES ('%(name)s')
        """%{"name":domain}

write2mysql(conn, sql)
kill_mysqldb(conn)



   
