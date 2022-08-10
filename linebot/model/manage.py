import os
from select import select
import mysql.connector

rds_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="manage",
                              pool_size=5,
                              **rds_config)

def create(member_id, group_id):
    try:
        cnx = mysql.connector.connect(pool_name="manage")
        cursor = cnx.cursor()
        
        data = (member_id, group_id)
        
        
        query = ("INSERT IGNORE INTO Manage (member_id, group_id) VALUES (%s, %s)")
        cursor.execute(query, data)
        cnx.commit()

        return {"ok": True}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()