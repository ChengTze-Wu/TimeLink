import os
import mysql.connector

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

        
def get_reserve_by_member_id_and_group_id(member_id, group_id):
    try:
        cnx = mysql.connector.connect(pool_name="reserve")
        cursor = cnx.cursor()
        
        data = (member_id, group_id)
        query = ("SELECT Service.name, Reserve.bookedDateTime "
                 "FROM Reserve RIGHT JOIN Service "
                 "ON Reserve.service_id = Service.id "
                 "WHERE Reserve.member_id = %s "
                 "AND Service.group_id = %s")
       
        cursor.execute(query, data)
        result = cursor.fetchall()
        data_set = None
        if result:
            data_set = []
            for data in result:
                data_set.append({"serviceName": data[0],
                            "bookedDateTime": str(data[1])})
                
        return {"data": data_set}
    except Exception as e:
        raise e
    finally:
        cursor.close()
        cnx.close()