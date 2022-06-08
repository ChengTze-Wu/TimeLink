import os
import mysql.connector

rds_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="service",
                              pool_size=5,
                              **rds_config)

def create(name, price, type, user_id, group_id):
    try:
        cnx = mysql.connector.connect(pool_name="service")
        cursor = cnx.cursor()
        query = ("insert into Service (name, price, type, user_id, group_id) values (%s, %s, %s, %s, %s)")
        data = (name, price, type, user_id, group_id)
        
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
        
def get_all_by_user_id(user_id):
    try:
        cnx = mysql.connector.connect(pool_name="service")
        cursor = cnx.cursor()
        
        data = (user_id,)
        query = ("select Service.name, Service.type, Service.price, Line_Group.name from Service INNER JOIN Line_Group ON Service.group_id = Line_Group.id where Service.user_id = %s")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            if not data[1]:
                type = "無"
            else:
                type = data[1]
            
            datas.append({"name": data[0],
                            "type": type,
                            "price": data[2],
                            "group_name":data[3]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()

def get_all_by_group(group_id):
    try:
        cnx = mysql.connector.connect(pool_name="service")
        cursor = cnx.cursor()
        
        data = (group_id,)
        query = ("select name, price from Service where group_id = %s")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            datas.append({"name": data[0],
                            "price": data[1]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()