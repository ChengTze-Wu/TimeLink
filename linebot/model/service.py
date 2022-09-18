import os
import mysql.connector

rds_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="service",
                              pool_size=5,
                              **rds_config)

        
def get_all_by_group_id(group_id):
    try:
        cnx = mysql.connector.connect(pool_name="service")
        cursor = cnx.cursor()
        
        data = (group_id,)
        query = ("SELECT id, name, price, openTime, closeTime, notAvailableTime "
                 "FROM Service WHERE group_id = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        data_set = None
        if result:
            data_set = []
            for data in result:
                data_set.append({"id": data[0],
                            "name": data[1],
                            "price": data[2],
                            "openTime": str(data[3]),
                            "closeTime": str(data[4]),
                            "notAvailableTime": str(data[5])})

        return {"data": data_set}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()
