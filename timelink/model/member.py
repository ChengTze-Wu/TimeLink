from . import db
from mysql.connector import IntegrityError

def create(userId, name):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (userId, name)
        query = ("insert into Member (userId, name) values (%s, %s)")
        
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
        
def get_member_id_by_userId(userId):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()

        data = (userId,)
        query = ("SELECT id FROM Member WHERE userId = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
            
        return result[0]
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()