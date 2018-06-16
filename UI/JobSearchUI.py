import os
import math
import requests
import lorem

# Availability options
avail_opt = ["Hourly","Part-time","Full-time"]

# Selected Availability from query
sel_avail = []

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
    if environ['PATH_INFO'] == "/js/client.js":
	start_response('200 OK', [('Content-type', 'application/javascript; charset=utf-8')])
	return [open(cwd+"/js/client.js","r").read()]

    template = open(cwd+"/index.html","r").read()

    #for e in environ:
#	print(e)
#	print(environ[e])

    if "search_text" in environ['REQUEST_URI']:
	env_vars = environ['REQUEST_URI'].split("/")
	page_num = 1
	search_text = None
	for var in env_vars:
	    if "page" in var:
		page_num = var.split("=")[1]
	    if "?search_text" in var:
		search_text = var.split("=")[1]
	status = '200 OK'
	html = process_template(template, search_data=search_text, page=int(page_num))
	response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(html)))]
	start_response(status, response_headers)
	return [html]
	
    status = '200 OK'
    page_num = 1
    env_vars = environ['REQUEST_URI'].split("/")
    html = ""
    for var in env_vars:
	if "page" in var:
	    page_num = var.split("=")[1]
    if int(page_num) == 1:
	html = process_template(template)
    else:
	html = process_template(template, page=int(page_num))
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(html)))]
    start_response(status, response_headers)
    return [html]

# replaces ~()~ placeholders with data
def process_template(temp_string,search_data=None, page=1):
    results, result_num, pay_min, pay_max, exp_levels, skills, search_keywords = process_results(search_data=search_data,page=page)
    if search_keywords:
	print(" ".join(search_keywords))
	temp_string = temp_string.replace("~(search_keywords)~","value='"+" ".join(search_keywords)+"'")
    else:
	temp_string = temp_string.replace("~(search_keywords)~","")
    temp_string = temp_string.replace("~(results)~", results)
    temp_string = temp_string.replace("~(skills)~",process_skills(skills))
    temp_string = temp_string.replace("~(result_num)~",str(result_num))
    temp_string = temp_string.replace("~(avail_options)~",process_availability())
    temp_string = temp_string.replace("~(pay_min)~",str(pay_min))
    temp_string = temp_string.replace("~(pay_max)~",str(pay_max))
    processed_html = temp_string.replace("~(exp_levels)~",process_experience(exp_levels))
    return processed_html

# Replaces ~(skills)~ placeholder with skills given from query
def process_skills(sel_skills=[]):
    skill_string = ""
    for skill in sel_skills:
        skill_string += "<div class='skill'><p class'skill_text' style='display: inline;'>{}</p><img class='clear_skill hvr-grow' style='display: inline;' src='img/letter-x.svg'/></div>\n".format(skill)
    return skill_string

def process_results(search_data=None,page=1):
    url = "http://ec2-13-58-141-207.us-east-2.compute.amazonaws.com:8081"
    r = requests.get(url)
    filtered_results = []
    search_keywords = []
    if search_data:
        keywords = search_data.split("+")
        for keyword in keywords:
	    search_keywords.append(keyword.replace("%2B","+"))
    else:
	search_keywords = None
    for result in r.json():
        req_skills = result['required_skills'].split(",")
	if search_data:
            for keyword in search_keywords:
		    if keyword.lower() in req_skills or \
		     keyword.lower() in result['availability'].lower() or \
		     keyword.lower() in result['job_title'].lower() or \
		     keyword.lower() in result['location'].lower():
		        if result not in filtered_results:
			    filtered_results.append(result)			
	else:
	    filtered_results.append(result)
    result_num = len(filtered_results)
    result_string = ""
    exp_levels = 1
    pay_min = 100
    pay_max = 0
    skills = []
    for i, result in enumerate(filtered_results, 1):
        if int(result['experience_level']) > exp_levels:
            exp_levels = result['experience_level']
        if int(result['pay_rate']) > pay_max:
            pay_max = result['pay_rate']
        elif int(result['pay_rate']) < pay_min:
            pay_min = result['pay_rate']
	for skill in result['required_skills'].split(','):
	    if skill not in skills:
		skills.append(skill)
	if i >= 5*(page-1) and i <= 5*page:
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
    <div class="pagination">'''

    pages = int(math.ceil(result_num/5))
    i = 1
    exp_string = ""
    while i <= (pages+1):
        if i == page:
	    result_string += '''<a onclick="page_url({0})" class="active">{0}</a>\n'''.format(str(i))
        else:
            result_string += '''<a onclick="page_url({0})">{0}</a>\n'''.format(str(i))
        i += 1
    result_string += "</div>"
    return result_string, result_num, pay_min, pay_max, exp_levels, skills, search_keywords

def process_availability():
    avail_string = ""
    for avail in avail_opt:
	if avail not in sel_avail:
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

