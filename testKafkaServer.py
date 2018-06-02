import json
import random
import time
import requests
from faker import Faker
fake = Faker()

isDevelop = False

def returnJobs(jobNumber):
    start = time.time()
    finalJsonString = "["
    i = 0
    while (i < jobNumber):
        data = {}
        avail_options = ['Full-time','Part-time','Hourly']
        data['availability'] = random.choice(avail_options)
        data['pay_rate'] = random.randint(10,200)
        data['experience_level'] = random.randint(0,50)
        exp_options = ['Junior','Senior','Entry-Level','Experienced','Back End','Front End']
        lang_options = ['JavaScript','Swift','Python','Java','C++','Ruby','Rust','Elixir','Scala','R']
        job_lang = random.choice(lang_options)
        data['job_title'] = random.choice(exp_options)+" "+job_lang+" Developer"
        comp_options = ['Enterprises','Group','Industries','International','Services','Systems','& Co.','& Son']
        data['company_name'] = fake.name()+" "+random.choice(comp_options)
        data['location'] = fake.address().split("\n")[1]
        data['required_skills'] = job_lang
        finalJsonString += json.dumps(data)
        i += 1
        if i != jobNumber and jobNumber > 1:
            finalJsonString += ","
    finalJsonString += "]"
    end = time.time()
    print "Took {} seconds to randomly generate {} jobs.".format((end - start),jobNumber)
    if isDevelop:
        print finalJsonString
    else:
        r = requests.post('http://ec2-18-188-80-81.us-east-2.compute.amazonaws.com:8082', finalJsonString)
        print r.text
                
returnJobs(100000)
