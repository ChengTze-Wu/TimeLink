import os
import mysql.connector
import datetime

rds_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="reserve",
                              pool_size=5,
                              **rds_config)

def get_available_time(service_id, booking_date):
    try:
        cnx = mysql.connector.connect(pool_name="reserve")
        cursor = cnx.cursor()
        
        data = (service_id, booking_date)
        query = ("SELECT * FROM Reserve "
                 "RIGHT JOIN Service "
                 "ON Reserve.service_id = Service.id "
                 "WHERE Service.id = %s "
                 "AND DATE(Reserve.bookedDateTime) = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchall()

        # time control
        # get operation time
        openTime = (datetime.datetime.min + result[0][13]).time()
        closeTime = (datetime.datetime.min + result[0][14]).time()
        
        available_time = [time_node for time_node in range(openTime.hour, closeTime.hour)]
        
     
        for data in result:
            if data[5]:
                bookedTime = data[5].hour
                available_time.remove(bookedTime)

        return {"data": {"available_time": available_time}}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()