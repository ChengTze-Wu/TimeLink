from flask import Blueprint, request, session, current_app
from timelink import model
from timelink.util.uploader import upload_img_to_s3
import jwt


bp = Blueprint('service', __name__, url_prefix='/api')


SECRET_KEY = current_app.config['SECRET_KEY']


@bp.route("/services", methods=["POST"])
def create():
    created_status = False
    uploaded_status = False
    try:
        imageFile = request.files["imageFile"]
        data = request.form.to_dict()

        name = data["name"]
        price = data["price"]
        type = data["type"]
        group_id = data["group_id"]
        openTime = data["openTime"]
        closeTime = data["closeTime"]

        usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        user_id = usertoken["id"]
        
        # check if image file exists
        if imageFile:
            # upload image to s3
            uploaded_status = upload_img_to_s3(imgfile=imageFile, file_name=imageFile.filename)
            # if uploaded, create service
            if uploaded_status:
                created_status = model.service.create(name=name, type=type, price=price, group_id=group_id, 
                                    user_id=user_id, open_time=openTime, close_time=closeTime,
                                    imgUrl=f"https://d43czlgw2x7ve.cloudfront.net/timelink/{imageFile.filename}")
        else:
            created_status = model.service.create(name=name, type=type, price=price, group_id=group_id, 
                                user_id=user_id, open_time=openTime, close_time=closeTime)
        # if created, return success message
        if created_status:
            return {"success": True}, 201
        return {"success": False, "error":{"code": 200, "message":"Create Failed"}}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error":{"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500
    

@bp.route("/services", methods=["GET"])
def get_services():
    try:
        queryString = request.args
        if "groupId" in queryString:
            dbData = model.service.get_all_by_groupId(groupId=queryString["groupId"])
        elif "group_id" in queryString:
            dbData = model.service.get_all_by_group_id(group_id=queryString["group_id"])
        else:
            usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
            user_id = usertoken["id"]
            dbData = model.service.get_all_by_user_id(user_id=user_id)
            
        if dbData:
            return {"success": True, "data": dbData}, 200
        return {"success": False, "data": None}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error":{"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500

@bp.route("/services/<service_id>", methods=["GET"])
def get_service(service_id):
    try:
        dbData = model.service.get_all_by_service_id(service_id=service_id)
        if dbData:
            return {"success": True, "data": dbData}, 200
        return {"success": False, "data": None}, 200
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500
    
@bp.route("/services/<service_id>", methods=["DELETE"])
def delete(service_id):
    try:
        jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        model.service.delete(service_id=service_id)
        return {"success": True}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error":{"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500