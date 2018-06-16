# Job Search API

The completed running project can be accessed through the UI site Job Search, which is located here:
`http://13.58.141.207`

This project contains various moving parts that lend it to be on the more complex side. The main parts are:

<b>JobSearchAPI (Java)</b> - REST API that queries MySQL DB and responds in JSON data.<br/>
<b>JobPostAPI (Java)</b> - REST API that takes in a POST request with JSON data and creates a Kafka producer for that data.<br/>
<b>KafkaConsumer (Python)</b> - Kafka Consumer that waits for JSON data on the Kafka queue and pushes the data into the MySQL DB.<br/>
<b>JobSearchUI (HTML, JS, CSS, Python)</b> - Website with a custom Python mod_wsgi back end that employs MVC architecture to maintain separation of data and front-end. Ensures no information about data source can be retrieved from the front-end.<br/>

[The source for this project is available here][src].

# Source Code Navigation:
<b>JobSearchAPI (Java):</b><br/>
The Java source code can be found under `../JobSearchAPI/` and follows the basic structure for a Maven project, with classes being available in the `../JobSeachAPI/target` directory.<br/>
<b>JobPostAPI (Java):</b><br/>
The Java source code can be found under `../JobPostAPI/` and follows the basic structure for a Maven project, with classes being available in the `../JobPostAPI/target` directory.<br/>
<b>KafkaConsumer.py (Python):</b><br/>
The Kafka consumer lives in a Python script that acts as it's own source code. In order to access the source code of this program, open the `../KafkaConsumer.py` file in any text editor.
There is also a unit test file that will generate a set number of job listings and add them to the Kafka queue to test the system with a load. This file is located at `../testKafkaServer.py` and is currently set to add 100 random job listings to the queue.<br/>
<b>JobSearchUI (HTML, JS, CSS, Python)</b><br/>
The UI is a bit more complex than the rest of the project, but for good reason. The UI flow works as follows:
<pre>
<b>Request:</b>
	client (http request) -> apache (http request) -> JobSearchUI.py (http request) -> JobSearchAPI (DB query) -> MySQL DB
<b>Response:</b>
    MySQL DB (data) -> JobSearchAPI (JSON) -> JobSearchUI.py (html, js, css) -> client
</pre>

The `../UI/JobSearchUI.py` file is a mod_wsgi server that will process the request of the user and respond with the appropriate data, it also handles pagination of the data as well as filtering out the keywords. In the future this will also be able to handle the AJAX requests given from the filters on the left side of the UI, but is not currently configured to do so. Since this Python program handles the request and only responds with appropriate data in html format, none of the data's origin can be discerned from the source code of the UI, and hitting the server with malicious URLs will get only get a response of the formatted index page.<br/>
The `../UI/` directory also includes the `index.html` file which is a template and is not meant to be served directly. This file includes many `~()~` directives which the `../UI/JobSearchUI.py` Python file will replace with the appropriate data. The `../UI/js/`, `../UI/css/`, and `../UI/img/` folders should be directly readable, note however that all files that are necessary for the site to run are <i>explicitly</i> defined and any requests for any other, or potentially injected files will not go through and will once again simply get the response of the formatted index page.

# Using Functionality Separately (for testing)

This program is meant to be a full stack and is not meant to be run in the various sections, however the separate functions can be utilized through their own ports. If data is to be added from an outside source apart from the unit test located in `../testKafkaServer.py` it is necessary to use the functionality separately (you can also add data directly through the MySQL database, but it's no fun).

<b>JobSearchAPI:</b><br/>
The JobSearchAPI is a REST API that will query the MySQL DB and respond in JSON format (this is also the format you will need to use in order to add data via the post method).
<pre>
GET: http://ec2-13-58-141-207.us-east-2.compute.amazonaws.com:8081
</pre>
<b>JobPostAPI:</b><br/>
The JobSearchAPI is a REST API will accept POST requests passing in job listings in JSON format and will respond with a basic HTML page that will tell you how many job listings were added with your request and how long the process took.
<pre>
POST: http://ec2-13-58-141-207.us-east-2.compute.amazonaws.com:8082
BODY: [{"company_name":"RiskSense","required_skills":"UI,UX,Javascript,MVC,MySQL","location":"Albuquerque, NM","availability":"Full-time","pay_rate":23,"experience_level":3,"job_title":"Javascript Developer"}]
<hr>
Response:<h1>1 Job listing has been added to the Kafka queue in 0 seconds.</h1>
</pre>
<b>MySQL DB (direct access):</b><br/>
Obviously this is the worst way to access the information due to it requiring credentials, however if you need access to this database directly, you can do so like so:
<pre>
HOST: 13.58.147.207:3306
Username: rs_admin
Password: risksense
</pre>
<b>Kafka Consumer (direct access):</b><br/>
The Kafka Consumer can be hit directly, however you may want to check out the `../testKafkaServer.py` file to see the format of the data.
<pre>
HOST: http://ec2-13-58-141-207.us-east-2.compute.amazonaws.com:9092
</pre>

# Unique Features!

The UI may look pretty basic, but actually has a lot of advanced features going on behind the scenes!<br>
<b>Data Abstraction:</b><br/>
When data is requested from the UI, a lot of layers split up the data and the data source to the extent that it makes reverse engineering impossible. The request comes into the Python server, which will query the JobSearchAPI. The JobSearchAPI will query the database and return only the data to the Python server. The Python server will also only return the data, but now in html format and baked into the page directly rather than retrieved at runtime. This makes it so that if someone were to dig through the source code of the UI (html,css,js) they would not be able to determine where the data is coming from.<br/>
<b>Speed:</b><br>
Since all the data that is required is baked into the page directly, there is very little JavaScript being run on the client side, allowing the page to be run on the client with very little resources, and the baked data is all that needs to be passed over the net making transfer speeds from server to client blazing fast.<br>
<b>Injection Resistant:</b><br/>
Since the UI has no way to access the data directly, there is no way to inject malicious JS or SQL code into the site. The Python server has even been programmed to be URL agnostic in many situations, so that if a malicious user is attempting to execute code via the URL or AJAX that hasn't been <i>explicitly</i> allowed, then the server will simply respond with the default formatted index page (unlike a basic Apache server).<br/>

# TODO / Known Bugs:

This project was done in a very short amount of time, so there will be bugs as well as things I haven't gotten around to implementing yet.

<b>Filters:</b><br>
Essentially none of the filter buttons have been wired up to the back end yet, so many buttons will appear to be unresponsive. With more time (maybe a couple of days) I could wire these up.

That doesn't mean that you can't filter the data however! If you put any search terms into the search bar and hit the "Search" button, it will filter the results using the search terms that were provided.



[src]: https://github.com/izzythecubemaster/RiskSense-TechAssessment
