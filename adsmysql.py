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

def write2mysql(conn, table, row):
    """Writes the row to the table into mysql db
    table - name of the table
    row - list of tuples (colname, value)
    """
    # TODO Convert table, row to sql
    for items in row:
        col = items[0]
        val = items[1]
    print(col, val)
    sql = """INSERT INTO '%(table)s'('%(col)s')
        VALUES ('%(val)s')
        """%{"table":table, "col":col, "val":val}
    execute_mysqldb(conn, sql)
    return

def execute_mysqldb(conn, sql):
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

# Usage example
##conn = init_mysqldb()    
##
##domain = 'ya.ru'
##sql = """INSERT INTO sites(domain)
##        VALUES ('%(name)s')
##        """%{"name":domain}
##
##execute_mysqldb(conn, sql)
##kill_mysqldb(conn)
##
##sql = """INSERT INTO contacts(name, mail, adres, tel)
##        VALUES ('%(name)s', '%(mail)s', '%(adres)s', '%(tel)s')
##        """%{"name":fname, "mail":fmail, "adres":fadres, "tel":ftel}


   
