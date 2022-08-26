from flask import current_app
import boto3
from botocore.exceptions import ClientError
import imghdr

REGION = current_app.config['REGION']
AWS_ACCESS_KEY_ID = current_app.config['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = current_app.config['AWS_SECRET_ACCESS_KEY']

def upload_img_to_s3(imgfile, file_name=None) -> bool:
    s3 = boto3.client("s3", region_name=REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        # check if file is an image
        if(imghdr.what(imgfile)):
            s3.upload_fileobj(imgfile, "wehelpimagetest", "timelink/"+file_name)
            return True
    except ClientError as e:
        return False
    return False