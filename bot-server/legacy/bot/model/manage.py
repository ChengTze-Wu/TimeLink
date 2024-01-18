from genericpath import exists
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

def create(memberId=None, groupId=None, member_id=None, group_id=None):
    try:
        cnx = mysql.connector.connect(pool_name="manage")
        cursor = cnx.cursor()
        
        if memberId:
            memberId_data = (memberId,)
            memberId_query = ("SELECT id FROM Member WHERE userId = %s")
            cursor.execute(memberId_query, memberId_data)
            memberId_result = cursor.fetchone()
            if memberId_result:
                member_id = memberId_result[0]

        if groupId:
            groupId_data = (groupId,)
            groupId_query = ("SELECT id FROM Line_Group WHERE groupId = %s")
            cursor.execute(groupId_query, groupId_data)
            groupId_result = cursor.fetchone()
            if groupId_result:
                group_id = groupId_result[0]
        
        if member_id and group_id:
            # Check if member_id and group_id already exist in Manage
            check_data = (member_id, group_id)
            check_query = ("SELECT id FROM Manage WHERE member_id = %s AND group_id = %s")
            cursor.execute(check_query, check_data)
            exists_result = cursor.fetchone()
            if exists_result:
                return "Already exists"
            Manage_data = (member_id, group_id)
            Manage_query = ("INSERT INTO Manage (member_id, group_id) VALUES (%s, %s)")
            cursor.execute(Manage_query, Manage_data)
            cnx.commit()
            return True
        return False
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()