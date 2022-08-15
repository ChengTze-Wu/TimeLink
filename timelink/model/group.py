from . import db

def create(groupId, name, user_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        data = (groupId, name, user_id)
        query = ("insert into Line_Group (groupId, name, user_id) values (%s, %s, %s)")
        
        cursor.execute(query, data)
        cnx.commit()
        return {"data": True}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_all_by_user(user_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (user_id,)
        query = ("select * from Line_Group where user_id = %s")
        cursor.execute(query, data)
        result = cursor.fetchall()
        
        datas = []
        for data in result:
            datas.append({"id": data[0],
                            "groupId": data[1],
                            "name": data[2],
                            "createDatetime": data[3],
                            "user_id": data[4]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_all_groupId():
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()

        query = ("select groupId from Line_Group")
        cursor.execute(query)
        result = cursor.fetchall()
        
        datas = []
        for data in result:
            datas.append({"groupId": data[0]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
    
def get_group_id_by_groupId(groupId):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()

        data = (groupId,)
        query = ("select id from Line_Group where groupId = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
            
        return {"data": result[0]}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        