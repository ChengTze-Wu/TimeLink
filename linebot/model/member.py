import os
import mysql.connector

rds_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="member",
                              pool_size=5,
                              **rds_config)

def create(userId, name):
    try:
        cnx = mysql.connector.connect(pool_name="member")
        cursor = cnx.cursor()
        
        data = (userId, name)
        query = ("insert into Member (userId, name) values (%s, %s)")
        
        cursor.execute(query, data)
        cnx.commit()
        
        return True
    except Exception as e:
        if e.errno == 1062:
            return "Already exists"
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_member_id_by_userId(userId):
    try:
        cnx = mysql.connector.connect(pool_name="member")
        cursor = cnx.cursor()

        data = (userId,)
        query = ("SELECT id FROM Member WHERE userId = %s")
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