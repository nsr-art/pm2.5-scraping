import base64
import sqlalchemy

connection_name = "pivotal-sprite-285504:asia-southeast1:smarthome-seniorproject"
table_name = ""
#table_field = ""
#table_field_value = ""
db_name = "smart_home"
db_user = "NSR_ADMIN"
db_password = "natthapon024299"

# If your database is MySQL, uncomment the following two lines:
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    date = pubsub_message[2:12]
    time = pubsub_message[13:21]
    temp = pubsub_message[31:35]
    humi = pubsub_message[37:41]
    stat = pubsub_message[43]

    #stmt = INSERT(DHT11_Sensor).VALUES(Date=date,Time=time,Temperature=temp,Humidity=humi,Status=stat,Voltage=5)
    #stmt = sqlalchemy.text('INSERT INTO DHT11_Sensor (Date, Time, Temperature, Humidity, Status, Voltage) VALUES (22-0-2020,14.27,23.6,50.8,1,5)')
    sql = "INSERT INTO DHT11_Sensor (Date, Time, Temperature, Humidity, Status, Voltage) VALUES (%s,%s,%s,%s,%s,%s)"
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
            conn.execute(sql, (date,time,temp,humi,stat,5))
    except Exception as e:
        return 'Error: {}'.format(str(e))
    print(date, time, temp, humi, stat)