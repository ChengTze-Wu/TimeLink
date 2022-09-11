from flask import current_app
from . import db
import datetime
import json
import requests
from mysql.connector import IntegrityError


def get_profile(groupId=None, userId=None): 
    channel_access_token = current_app.config['LINE_CHANNEL_TOKEN']
    header = {'Authorization': "Bearer " + channel_access_token}
    url = f'https://api.line.me/v2/bot/profile/{userId}'
    if groupId:
        url = f'https://api.line.me/v2/bot/group/{groupId}/member/{userId}'
    try:
        resp = requests.get(url, headers=header)
        if resp.status_code == 400:
            return None
        data = json.loads(resp.text)
        img_url = data["pictureUrl"]
        member_name = data["displayName"]
        return {"img_url": img_url, "member_name": member_name}
    except Exception:
        return None
    

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
        
        if len(available_time) == 0:
            return None
        return {"available_time": available_time}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
def create(service_id, member_id, bookedDateTime, status=None) -> bool:
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        # check if the time is available
        check_query = ("SELECT * FROM Reserve "
                       "WHERE service_id = %s and bookedDateTime = %s")
        check_data = (service_id, bookedDateTime)
        
        cursor.execute(check_query, check_data)
        result = cursor.fetchone()
        
        if result:
            return False
        
        query = ("insert into Reserve "
                 "(service_id, member_id, bookedDateTime, status) "
                 "values (%s, %s, %s, %s)")
        data = (service_id, member_id, bookedDateTime, status)
        
        cursor.execute(query, data)
        cnx.commit()
        return True
    except Exception as e:
       raise e
    finally:
        cursor.close()
        cnx.close()
        
        
def update(reserve_id, bookedDateTime) -> bool:
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        query = ("UPDATE Reserve "
                 "SET bookedDateTime = %s "
                 "WHERE id = %s")
        data = (bookedDateTime, reserve_id)
        
        cursor.execute(query, data)
        cnx.commit()
        return True
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        

def get_reserve_by_user_id_and_group_id(user_id:int, group_id:int) -> dict:
    """
    ### Return Example ###
    {
        "data": [
            {
                "reserve_id": 1,
                "member_id": 1,
                "member_image": "xxxxx",
                "member_name": "test",
                "service_id": 1,
                "service_name": "test",
                "reserve_createDateTme": "2020-01-01 00:00:00",
                "reserve_bookedDateTime": "2020-01-01 00:00:00"
            },
        ]
        "group_id": 1,
        "group_name": "test",
    }
    """
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (user_id, group_id)
        query = ("SELECT Line_Group.id, Line_Group.groupId, Line_Group.name, "
                 "Member.id, Member.userId, Member.name, "
                 "Service.id, Service.name, "
                 "Reserve.id, Reserve.createDatetime, Reserve.bookedDateTime "
                 "FROM (((Reserve INNER JOIN Service ON Reserve.service_id = Service.id) "
                 "INNER JOIN Member ON Reserve.member_id = Member.id) " 
                 "INNER JOIN Line_Group ON Service.group_id = Line_Group.id) "
                 "WHERE Service.user_id = %s and Service.group_id = %s ")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        
        if result:
            reserves = []
            member_exist = []
            member_image = None
            for data in result:
                
                if data[3] not in member_exist:
                    # reduce number of requests of getting member image
                    profile = get_profile(groupId=data[1], userId=data[4])
                    member_image = profile["img_url"]
                    member_name = profile["member_name"]
                    member_exist.append(data[3])
                
                reserves.append({"reserve_id": data[8],
                                "member_id": data[3],
                                "member_image": member_image,
                                "member_name": member_name,
                                "service_id": data[6],
                                "service_name": data[7],
                                "reserve_createDateTme": data[9].strftime("%Y/%m/%d %H:%M:%S"),
                                "reserve_bookedDateTime": data[10].strftime("%Y/%m/%d %H:00")})
                
            return {"group_id": result[0][0], "group_name": result[0][2], "data": reserves}
        
        return None
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
        
def get_reserve_by_id(reserve_id:int):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (reserve_id, )
        query = ("SELECT * "
                 "FROM ((Reserve INNER JOIN Service ON Reserve.service_id = Service.id) "
                 "INNER JOIN Member ON Reserve.member_id = Member.id) " 
                 "WHERE Reserve.id = %s ")
        
        cursor.execute(query, data)
        result = cursor.fetchone()
        
        if result:
            profile = get_profile(userId=result[18])
            member_name = profile["member_name"]
            member_image = profile["img_url"]
            return {"reserve_id": result[0], "reserve_createDateTime": result[3].strftime("%Y/%m/%d %H:%M:%S"),
                    "reserve_bookedDateTime": result[5].strftime("%Y/%m/%d %H:00"),
                    "service_id": result[6], "service_name": result[7], "service_price": result[8], 
                    "service_image": result[16], "member_name": member_name, "member_image":member_image}
        
        return None
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
        
        

def delete_by_id(reserve_id:int):
    try:
        cnx = db.get_db()
        cursor = cnx.cursor()
        
        data = (reserve_id,)
        query = ("DELETE FROM Reserve WHERE id = %s")
       
        cursor.execute(query, data)
        cnx.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()