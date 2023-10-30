from . import db
from mysql.connector import IntegrityError

def create(name, price, user_id, group_id, type=None, open_time=None, close_time=None, not_available_time=None, imgUrl=None) -> bool:
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        query = ("insert into Service "
                 "(name, price, type, user_id, group_id, openTime, closeTime, notAvailableTime, imgUrl) "
                 "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (name, price, type, user_id, group_id, open_time, close_time, not_available_time, imgUrl)
        
        cursor.execute(query, data)
        cnx.commit()
        return True
    except IntegrityError:
        return False
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def get_service_by_id(service_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (service_id,)
        query = ("SELECT id, name, price, openTime, "
                 "closeTime, notAvailableTime, imgUrl "
                 "FROM Service WHERE isDeleted = 0 AND id = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchone()
        
        if result:
            return {"id": result[0],
                    "name": result[1],
                    "price": result[2],
                    "openTime": str(result[3]),
                    "closeTime": str(result[4]),
                    "notAvailableTime": str(result[5]),
                    "image": result[6]}
            
        return None
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
                 "INNER JOIN Line_Group ON Service.group_id = Line_Group.id where Service.isDeleted = 0 AND Service.user_id = %s")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        data_set = []
        for data in result:
            if not data[2]:
                type = "無"
            else:
                type = data[2]
            
            data_set.append({"id": data[0],
                        "name": data[1],
                        "type": type,
                        "price": data[3],
                        "group_name":data[4]})
            
        return data_set
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
        query = ("select id, name, price, type, "
                 "openTime, closeTime, notAvailableTime, imgUrl "
                 "from Service where isDeleted = 0 AND group_id = %s")
    
        cursor.execute(query, data)
        result = cursor.fetchall()
        
        data_set = []
        for data in result:
            data_set.append({"id": data[0],
                        "name": data[1],
                        "price": data[2],
                        "type": data[3],
                        "openTime": str(data[4]),
                        "closeTime": str(data[5]),
                        "notAvailableTime": str(data[6]),
                        "image": data[7]})
            
        return data_set
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
        query = ("SELECT id, name, price, "
                 "openTime, closeTime, notAvailableTime, imgUrl "
                 "FROM Service WHERE isDeleted = 0 AND group_id in "
                 "(SELECT id FROM Line_Group WHERE groupId = %s)")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        data_set = []
        for data in result:
            data_set.append({"id": data[0],
                        "name": data[1],
                        "price": data[2],
                        "openTime": str(data[3]),
                        "closeTime": str(data[4]),
                        "notAvailableTime": str(data[5]),
                        "image": data[6]})
            
        return data_set
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()

# logical deletion
def logical_delete(service_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (service_id,)
        query = ("update Service set isDeleted = 1 where id = %s")
        
        cursor.execute(query, data)
        cnx.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
