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
        return {"ok": True}, 201
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        
def check(userId):
    try:
        cnx = mysql.connector.connect(pool_name="member")
        cursor = cnx.cursor()
        
        data = (userId,)
        query = ("SELECT * FROM Service WHERE userId = %s;")
        
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            return True
        return False
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()

        
def get_all_by_group_id(group_id):
    try:
        cnx = mysql.connector.connect(pool_name="member")
        cursor = cnx.cursor()
        
        data = (group_id,)
        query = ("SELECT Line_Group.name, Member.name "
                "FROM ((Manage INNER JOIN Line_Group ON Manage.group_id = Line_Group.id) "
                "INNER JOIN Member ON Manage.member_id = Member.id) "
                "WHERE group_id = %s;")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        
        datas = []
        for data in result:
            datas.append({"group_name": data[0],
                        "mamber_name": data[1]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()