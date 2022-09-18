import os
import mysql.connector

rds_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="group",
                              pool_size=5,
                              **rds_config)
    

def get_group_id_by_groupId(groupId):
    try:
        cnx = mysql.connector.connect(pool_name="group")
        cursor = cnx.cursor()

        data = (groupId,)
        query = ("select id from Line_Group where groupId = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        