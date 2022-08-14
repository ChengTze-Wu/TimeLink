from . import db

def create(username, password, name, email, phone):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        data = (username, password, name, email, phone)
        query = ("insert into User (username, password, name, email, phone) values (%s, %s, %s, %s, %s)")
        
        cursor.execute(query, data)
        cnx.commit()
        return {"data": True}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        
def auth(username):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (username,)
        query = ("select id, username, password from User where username = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            return {"data": {"id":result[0], "username":result[1], "password":result[2]}}
        else:
            return {"data": None}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        
def get_all():
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        query = ("select * from User")
        cursor.execute(query)
        result = cursor.fetchall()
        
        datas = []
        for data in result:
            datas.append({"id": data[0],
                            "username": data[1],
                            "password": data[2],
                            "name": data[3],
                            "email": data[4],
                            "phone": data[5],
                            "createDatetime": data[6]})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        
