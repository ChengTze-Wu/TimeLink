from . import db

def create(name, price, user_id, group_id, type=None, open_time=None, close_time=None, not_available_time=None):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        query = ("insert into Service "
                 "(name, price, type, user_id, group_id, openTime, closeTime, notAvailableTime) "
                 "values (%s, %s, %s, %s, %s, %s, %s, %s)")
        data = (name, price, type, user_id, group_id, open_time, close_time, not_available_time)
        
        cursor.execute(query, data)
        cnx.commit()
        return {"ok": True}, 201
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_all_by_service_id(service_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (service_id,)
        query = ("SELECT * FROM Service WHERE id = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            datas.append({"id": data[0],
                        "name": data[1],
                        "price": data[2],
                        "openTime": str(data[7]),
                        "closeTime": str(data[8]),
                        "notAvailableTime": str(data[9])})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_all_by_user_id(user_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (user_id,)
        query = ("select Service.id, Service.name, Service.type, Service.price, Line_Group.name from Service "
                 "INNER JOIN Line_Group ON Service.group_id = Line_Group.id where Service.user_id = %s")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            if not data[2]:
                type = "無"
            else:
                type = data[2]
            
            datas.append({"id": data[0],
                        "name": data[1],
                        "type": type,
                        "price": data[3],
                        "group_name":data[4]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()

def get_all_by_group_id(group_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (group_id,)
        query = ("select * from Service where group_id = %s")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            datas.append({"id": data[0],
                        "name": data[1],
                        "price": data[2],
                        "type": data[3],
                        "openTime": str(data[7]),
                        "closeTime": str(data[8]),
                        "notAvailableTime": str(data[9])})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_all_by_groupId(groupId):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (groupId,)
        query = ("SELECT * FROM Service WHERE group_id in "
                 "(SELECT id FROM Line_Group WHERE groupId = %s)")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            datas.append({"id": data[0],
                        "name": data[1],
                        "price": data[2],
                        "openTime": str(data[7]),
                        "closeTime": str(data[8]),
                        "notAvailableTime": str(data[9])})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()

def delete(service_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (service_id,)
        query = ("DELETE FROM Service WHERE id = %s;")
        
        cursor.execute(query, data)
        cnx.commit()
        
        return {"ok": True}, 200
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
