import MySQLdb
import json
from kafka import KafkaConsumer

def quote(input_string):
    return "\""+input_string+"\""

def insert_job_into_db(data):
    db = MySQLdb.connect("localhost","rs_admin","risksense","job_listing_data")
    cursor = db.cursor()
    cursor.execute('''INSERT INTO job_listings (availability,pay_rate,experience_level,job_title,company_name,location,required_skills)
            VALUES
        ({0},{1},{2},{3},{4},{5},{6});'''.format(quote(data[0]),data[1],data[2],quote(data[3]),quote(data[4]),quote(data[5]),quote(data[6])))
    db.commit()
    db.close()

consumer = KafkaConsumer('job_listings')
for msg in consumer:
    json_data = json.loads(msg.value)
    objectData = []
    objectData.append(json_data['availability'])
    objectData.append(json_data['pay_rate'])
    objectData.append(json_data['experience_level'])
    objectData.append(json_data['job_title'])
    objectData.append(json_data['company_name'])
    objectData.append(json_data['location'])
    objectData.append(json_data['required_skills'])
    insert_job_into_db(objectData)

