import os
import math
import requests
import lorem

# Availability options
avail_opt = ["Hourly","Part-time","Full-time"]

# Temporary test values
# Selected skills from query
sel_skills = ["Python","JavaScript","HTML","CSS"]

# Selected Availability from query
sel_avail = ["Hourly","Full-time"]

def application(environ, start_response):
    cwd = os.path.dirname(os.path.abspath(__file__))

    if environ['PATH_INFO'] == "/img/favicon.png":
        start_response('200 OK', [('Content-type', 'image/png')])
        return [open(cwd+"/img/favicon.png","rb").read()]
    if environ['PATH_INFO'] == "/img/letter-x.svg":
        start_response('200 OK', [('Content-type', 'image/svg+xml')])
        return [open(cwd+"/img/letter-x.svg","rb").read()]
    if environ['PATH_INFO'] == "/css/stylesheet.css":
        start_response('200 OK', [('Content-type', 'text/css')])
        return [open(cwd+"/css/stylesheet.css","rb").read()]
    if environ['PATH_INFO'] == "/css/jquery.range.css":
        start_response('200 OK', [('Content-type', 'text/css')])
        return [open(cwd+"/css/jquery.range.css","rb").read()]
    if environ['PATH_INFO'] == "/js/jquery.range.js":
	start_response('200 OK', [('Content-type', 'application/javascript; charset=utf-8')])
	js = open(cwd+"/js/jquery.range.js","r").read()
	return [js]

    template = open(cwd+"/index.html","r").read()

    status = '200 OK'
    html = process_template(template)
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(html)))]
    start_response(status, response_headers)
    return [html]

# replaces ~()~ placeholders with data
def process_template(temp_string):
    results, result_num, pay_min, pay_max, exp_levels = process_results()
    temp_string = temp_string.replace("~(results)~", results)
    temp_string = temp_string.replace("~(skills)~",process_skills())
    temp_string = temp_string.replace("~(result_num)~",str(result_num))
    temp_string = temp_string.replace("~(avail_options)~",process_availability())
    temp_string = temp_string.replace("~(pay_min)~",str(pay_min))
    temp_string = temp_string.replace("~(pay_max)~",str(pay_max))
    processed_html = temp_string.replace("~(exp_levels)~",process_experience(exp_levels))
    return processed_html

# Replaces ~(skills)~ placeholder with skills given from query
def process_skills():
    skill_string = ""
    for skill in sel_skills:
        skill_string += "<div class='skill'><p class'skill_text' style='display: inline;'>{}</p><img class='clear_skill hvr-grow' style='display: inline;' src='img/letter-x.svg'/></div>\n".format(skill)
    return skill_string

def process_results(page=1):
    url = "http://ec2-13-58-141-207.us-east-2.compute.amazonaws.com:8081"
    r = requests.get(url)
    filtered_results = []
    for result in r.json():
        req_skills = result['required_skills'].split(",")
        for skill in req_skills:
            filtered_results.append(result)
            # if skill in sel_skills:
            #     if result['availability'] in sel_avail:
            #         if result['pay_rate'] >= pay_min and result['pay_rate'] <= pay_max:
            #             filtered_results.append(result)
    result_num = len(filtered_results)
    result_string = ""
    exp_levels = 1
    pay_min = 100
    pay_max = 0
    for result in filtered_results[5*(page-1):5*page]:
        if int(result['experience_level']) > exp_levels:
            exp_levels = result['experience_level']
        if int(result['pay_rate']) > pay_max:
            pay_max = result['pay_rate']
        elif int(result['pay_rate']) < pay_min:
            pay_min = result['pay_rate']
        result_string += """
        <div class='result'>
            <h4 class='result_title'>{0}</h4>
            <span class='result_type {1}'>{1}</span>
            <h4 class='pull-right result_pay'>${2} / hr</h4>

            <p class='job_title'><i class="material-icons">work_outline</i>&nbsp{3}</p>
            <p class='job_location'><i class="material-icons">room</i>&nbsp{4}</p>
            <p class='job_text'>{5}</p>
        </div>
        """.format(result['job_title'],\
        result['availability'].lower(),\
        result['pay_rate'],\
        result['company_name'],\
        result['location'],\
        lorem.text()[:250]+"...")

    result_string += '''
    <div class="pagination">
        <a href="#">&laquo;</a>'''

    pages = int(math.ceil(result_num/5))
    i = 1
    exp_string = ""
    while i < pages:
        if i == page:
            result_string += '<a href="#" class="active">{}</a>'.format(str(i))
        else:
            result_string += '<a href="#">{}</a>'.format(str(i))
        i += 1
    result_string += """<a href="#">&raquo;</a>
    </div>
    """
    return result_string, result_num, pay_min, pay_max, exp_levels

def process_availability():
    avail_string = ""
    for avail in avail_opt:
        avail_string += """
        <div class="checkbox">
            <label><input type="checkbox" value=""{0}>{1}</label>
        </div>
        """.format((check_availability(avail) or ""), avail)
    return avail_string

def check_availability(checked_option):
    if checked_option in sel_avail:
        return " checked"

def process_experience(exp_levels):
    i = 0
    exp_string = ""
    while i < exp_levels:
        i += 1
        if i == 1:
            exp_string += '<li role="presentation"><a role="menuitem" tabindex="-1" href="#">{} year of experience</a></li>'.format(i)
        else:
            exp_string += '<li role="presentation"><a role="menuitem" tabindex="-1" href="#">{} years of experience</a></li>'.format(i)
    return exp_string

