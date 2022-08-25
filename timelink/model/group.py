from . import db
from flask import current_app
import json
import requests


def get_groupInfo(groupId=None): 
    channel_access_token = current_app.config['LINE_CHANNEL_TOKEN']
    url_info = f'https://api.line.me/v2/bot/group/{groupId}/summary'
    url_count = f"https://api.line.me/v2/bot/group/{groupId}/members/count"
    header = {'Authorization': "Bearer " + channel_access_token}
    try:
        resp_info = requests.get(url_info, headers=header)
        if resp_info.status_code == 400:
            return None
        url_count = requests.get(url_count, headers=header)
        
        data_info = json.loads(resp_info.text)
        data_count = json.loads(url_count.text)
        
        pictureUrl = data_info["pictureUrl"]
        groupName = data_info["groupName"]
        count = data_count["count"]
        
        return {"pictureUrl": pictureUrl, "groupName": groupName, "count": count}
    except Exception:
        return None

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
            groupInfo = get_groupInfo(data[1])
            datas.append({"id": data[0],
                            "image": groupInfo["pictureUrl"],
                            "name": groupInfo["groupName"],
                            "memberCount": groupInfo["count"],
                            "createDate": data[3].strftime("%Y/%m/%d"),
                            "user_id": data[4]})
            
        return datas
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
        