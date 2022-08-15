from . import db
import datetime

def get_available_time(service_id, booking_date, working_minutes=60):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (service_id, )
        query = ("SELECT * FROM Reserve "
                 "RIGHT JOIN Service "
                 "ON Reserve.service_id = Service.id "
                 "WHERE Service.id = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        # time control
        # get operation time
        openTimeDelta = result[0][13]
        closeTimeDelta = result[0][14]
        timeRange = (closeTimeDelta - openTimeDelta)//datetime.timedelta(minutes=working_minutes)
        available_time = []
        
        for frag in range(timeRange):
            available_time.append(str((datetime.datetime.min + openTimeDelta + datetime.timedelta(minutes=frag*working_minutes)).time()))
        
        for data in result:
            if data[5]:
                if str(data[5].date()) == booking_date:
                    bookedTime = str(data[5].time())
                    available_time.remove(bookedTime)
                    
        return {"data": {"available_time": available_time}}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def create(service_id, member_id, bookedDateTime, status=None):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        query = ("insert into Reserve "
                 "(service_id, member_id, bookedDateTime, status) "
                 "values (%s, %s, %s, %s)")
        data = (service_id, member_id, bookedDateTime, status)
        
        cursor.execute(query, data)
        cnx.commit()
        return {"ok": True}, 201
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
        
def get_reserve_by_member_id_and_group_id(member_id, group_id):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (member_id, group_id)
        query = ("SELECT * FROM Reserve "
                 "RIGHT JOIN Service "
                 "ON Reserve.service_id = Service.id "
                 "WHERE Reserve.member_id = %s "
                 "AND Service.group_id = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        datas = []
        for data in result:
            datas.append({"serviceName": data[7],
                         "bookedDateTime": str(data[5])})
            
        return {"data": datas}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()