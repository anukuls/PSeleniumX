import MySQLdb
import logging
import Log_Manager

logger = logging.getLogger("utility.DB_Utils")

def connectDB(hostname, username, password, db_name):
    try:
        db = MySQLdb.connect(host=hostname,
                             user=username,
                             passwd=password,
                             db=db_name)
    except Exception as e:
        logger.exception("Unable to connect to DB %s on %s. Trace : %s" %(db_name, hostname, e))
        raise
    
    logger.info("Successfully connected to database %s on host %s" %(db_name, hostname))
    return db
    
def executeQuery(db, sql):
    try:
        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()
        # Use all the SQL you like
        cur.execute(sql)
    except Exception as e:
        logger.exception("Unable to execute query %s. Trace : %s" %(sql, e))
        db.close()
        raise
    
    logger.info("Successfully executed query %s" % sql)
    return cur.fetchall()
    
def closeDB(db):
    try:
        db.close()
        logger.info("Successfully closed DB connection.")
    except Exception as e:
        logger.exception("Unable to close DB. Trace : %s" % e)
        raise

# db_conn = connectDB("qevc1.qa1.liveops.com", "ccconf", "ccconf_dbctlusr", "ccconf")
# sql = "select * from rep where rep_id=22918"
# output = executeQuery(db_conn, sql)
# for row in output:
#     print row
# closeDB(db_conn)
# print all the first cell of all the rows
# for row in cur.fetchall():
#     print row