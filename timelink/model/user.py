from . import db
from mysql.connector import IntegrityError

def create(username, password, name, email, phone):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        data = (username, password, name, email, phone)
        query = ("insert into User (username, password, name, email, phone) values (%s, %s, %s, %s, %s)")
        
        cursor.execute(query, data)
        cnx.commit()
        return True
    except IntegrityError:
        return False
    finally:
        cursor.close()
        cnx.close()
        
def auth(username) -> dict:
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (username,)
        query = ("select id, username, password from User where username = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            return {"id":result[0], "username":result[1], "password":result[2]}
        else:
            return {}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
