# Store this code in 'app.py' file
import time

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors
import re
import os  # Add this import
from bs4 import BeautifulSoup


app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ravi4613'
app.config['MYSQL_DB'] = 'darkweb'

mysql = MySQL(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change to your SMTP server
app.config['MAIL_PORT'] = 587  # Change to the appropriate port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ravi.2003.io.in@gmail.com'  # Change to your email address
app.config['MAIL_PASSWORD'] = 'egqsnzmsathmixeo'  # Change to your email password
app.config['MAIL_DEFAULT_SENDER'] = 'ravi.2003.io.in@gmail.com'

mail = Mail(app)
def check_for_leaks(html_content, organization_name, sensitive_data):
    soup = BeautifulSoup(html_content, 'html.parser')
    leaked_data = []

    for  data_type , patterns in sensitive_data.items():
        for pattern in patterns:
            print("pattern:",pattern)
            print(soup.get_text())
            matches = re.findall(pattern, soup.get_text(), re.IGNORECASE)
            print("matches:",matches)
            if matches:
                leaked_data.extend(matches)
                
    return leaked_data





@app.route('/')

def home():
      from selenium import webdriver
      from selenium.webdriver.common.by import By 
      from selenium.webdriver.support.ui import WebDriverWait
      from selenium.webdriver.support import expected_conditions as EC
      driver=webdriver.Edge()
      driver.get("http://127.0.0.1:5000/admin/login")
      time.sleep(1)
      driver.maximize_window()
      driver.find_element(By.ID,"username").send_keys("admin@dwmb")
      driver.find_element(By.ID,"password").send_keys("password@dwmb")
      driver.find_element(By.CSS_SELECTOR,".btn").click()
      time.sleep(1)
      driver.get("http://127.0.0.1:5000/admin/monitor")
      time.sleep(1)
      driver.find_element(By.CSS_SELECTOR,".mbtn").click()
      time.sleep(1)
      #driver.find_element(By.LINK_TEXT,"Check_Leaks").click()  #
      driver.find_element(By.CSS_SELECTOR,".mbtn").click()
      for i in range(1,4):
            h2_present = False
            try:
                  driver.get(f"http://127.0.0.1:5000/admin/check_leaks?id={i}")
                  h2_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/h2")
                  h2_present = True
            except:
                  print("No h2 element found.")

# If h2 element is present, click the "Send_Mail" link
            if h2_present:
                try:
                      driver.get("http://127.0.0.1:5000/admin/monitor_data")
                      time.sleep(1)
                      send_mail_link = driver.get(f"http://127.0.0.1:5000/send_email?id={i}")
                      send_mail_link.click()
                      print("Clicked Send_Mail link.")
                except:
                      print("Send_Mail link not found or not clickable.")
            else:
                      print("No action taken as h2 element is not present.")
      return render_template('admin_dashboard.html')   
                      
			

@app.route('/dashboard')
def dashboard():
	if 'loggedin' in session:
		return render_template('dashboard.html')
	return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			return render_template('dashboard.html')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form and 'employee' in request.form and 'phoneno' in request.form and 'location' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		employee = request.form['employee']
		phoneno= request.form['phoneno']
		location = request.form['location']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
            'SELECT * FROM users WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)',(username, password, email, organisation, address, city,state, country, postalcode, employee ,phoneno , location))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)

@app.route("/index")
def index():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT organisation FROM users WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("index.html",account = account)
	return redirect(url_for('login'))

@app.route('/check_leaks', methods=['POST'])
def check_leaks():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    try:
        # Fetch sensitive data patterns from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username, password, email, organisation, address, city, state, country, postalcode, employee, phoneno, location FROM users")
        sensitive_data_rows = cursor.fetchall()
    except Exception as e:
        return f"Error fetching sensitive data patterns: {str(e)}"
    sensitive_data = {}
    for row in sensitive_data_rows:
        if row['id'] == session['id']:
            data_type = row['id']
            for key in ['username', 'password', 'email', 'organisation', 'address', 'city', 'state', 'country', 'postalcode', 'employee', 'phoneno', 'location']:
                pattern = row[key]
                sensitive_data.setdefault(data_type, []).append(pattern)
    dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')
    if os.path.exists(dark_web_path):
        with open(dark_web_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        leaked_data = check_for_leaks(html_content, "myCompany" ,sensitive_data)
        return render_template('dashboard.html', leaked_data=leaked_data)
    else:
        return "Error: dark_web.html file not found."


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))

@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form and 'employee' in request.form and 'phoneno' in request.form and 'location' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			postalcode = request.form['postalcode']
			employee = request.form['employee']
			phoneno= request.form['phoneno']
			location = request.form['location']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(
			'SELECT * FROM users WHERE username = % s',
				(username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s,\
				password =% s, email =% s, organisation =% s, \
				address =% s, city =% s, state =% s, \
				country =% s, postalcode =% s,employee =% s ,phoneno= % s, location =% s WHERE id =% s', (username, password, email, organisation,address, city, state, country, postalcode, employee,phoneno,location , (session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
	if 'admin_logged_in' not in session:
		return redirect('/admin/login')
	if request.method == 'GET' and 'check_users' in request.args:
		cur = mysql.connection.cursor()
		cur.execute("SELECT username,organisation,email FROM users")
		users = cur.fetchall()
		cur.close()
		return render_template('admin_dashboard.html', users=users)
	return render_template('admin_dashboard.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']       
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cur.fetchone()
        cur.close()
        if admin:
            session['admin_logged_in'] = True
            return redirect('/admin/dashboard')
        else:
            return 'Invalid username or password'   
    return render_template('admin_login.html')


@app.route('/admin/view_users')
def admin_view_users():
    if 'admin_logged_in' not in session:
        return redirect('/admin/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT username,organisation,email FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/monitor')
def admin_monitor():
	if 'admin_logged_in' not in session:
		return redirect('/admin/login')
	if request.method == 'GET' and 'check_users' in request.args:
		cur = mysql.connection.cursor()
		cur.execute("SELECT username,organisation,email FROM users")
		users = cur.fetchall()
		cur.close()
		return render_template('admin_monitor.html', users=users )
	return render_template('admin_monitor.html') 

@app.route('/admin/monitor_data')
def admin_monitor_data():
    if 'admin_logged_in' not in session:
        return redirect('/admin/login')  
    cur = mysql.connection.cursor()
    cur.execute("SELECT username,organisation,email,id FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('admin_monitor.html', users=users)

@app.route('/send_email')
def send_email():
	if 'admin_logged_in' not in session:
		return redirect('/admin/login')
	viewid = request.args.get('id')
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("SELECT email FROM users where id = % s",(viewid, ))
	users = cur.fetchone()
	cur.close()
	if users:
		recipient = users['email']
	else:
		return 'User not found'
	subject = 'Urgent Notification: Your Data Compromised on the Dark Web'
	body = "Hello client\n\n  \t We regret to inform you that our dark web monitoring system has detected a security incident involving your data. According to our investigation, sensitive information associated with your account has been compromised and is now circulating on the dark web.\n\n \tYou can see compromised data by clicking http://127.0.0.1:5000/check_leaks \n \t As your trusted service provider, we take the security and privacy of your information seriously. We are actively working to mitigate the impact of this incident and take appropriate steps to enhance our security measures to prevent future breaches.\nHere is what you can do to protect yourself: \n \t 1.Change your passwords immediately, especially if you use the same password for multiple accounts \n\t 2.Enable two-factor authentication (2FA) on your accounts wherever possible \n\t 3.Monitor your financial accounts and credit reports for any suspicious activity \n\t 4.Be cautious of phishing attempts or suspicious emails asking for personal information.\n \t We sincerely apologize for any inconvenience this may cause you and assure you that we are committed to resolving this issue swiftly and transparently. If you have any questions or require further assistance, please do not hesitate to contact us. \n \t Thank you for your understanding and cooperation.      "
	msg = Message(subject=subject, recipients=[recipient],body=body)

	try:
		mail.send(msg)
		return 'Email sent successfully!'
	except Exception as e:
		return str(e)
   
@app.route('/admin/check_leaks', methods=['POST','GET'])
def admin_check_leaks():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    try:
        viewid = request.args.get('id')
        # Fetch sensitive data patterns from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username, password, email, organisation, address, city, state, country, postalcode, employee, phoneno, location FROM users where id = % s",(viewid,))
        sensitive_data_rows = cursor.fetchone()
    except Exception as e:
        return f"Error fetching sensitive data patterns: {str(e)}"
    if sensitive_data_rows:
        sensitive_data = {}
        data_type = sensitive_data_rows['id']
        for key in ['username', 'password', 'email', 'organisation', 'address', 'city', 'state', 'country', 'postalcode', 'employee', 'phoneno', 'location']:
            pattern = sensitive_data_rows[key]
            sensitive_data.setdefault(data_type, []).append(pattern)
    dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')
    if os.path.exists(dark_web_path):
        with open(dark_web_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        leaked_data = check_for_leaks(html_content, "my company" ,sensitive_data)
        return render_template('admin_monitor.html', leaked_data=leaked_data)
    else:
        return "Error: dark_web.html file not found."


if __name__ == '__main__':
    app.run(debug=True)