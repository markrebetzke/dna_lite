from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import json, requests
from forms import RegistrationForm, LoginForm, ForgotForm
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dd72f8fd5e3b02ce8f5fdc972f0ee022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy="dynamic")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

uri_token = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"
user = "devnetuser"
password = "Cisco123!"

def get_token(uri, user, password):
    url = uri
    payload = {}
    headers = {
      'Accept': 'application/json'
    }
    response = requests.post(url=url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload, verify=False)
    json_response = response.json()
    return json_response['Token']

def get_server_info(token):
    url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/ip-address/10.10.22.70"
    payload = {}
    headers = {
        'X-auth-token':token
    }
    response = requests.post(url=url, headers=headers, data=payload, verify=False)
    print(response.json)

def get_run(server, port, token):
    url = "https://{0}:{1}/api/v1/global/running-config".format(server, port)
    payload = {}
    headers = {'X-auth-token': token}
    response = requests.get(url=url, headers=headers, data=payload, verify=False)
    text = response.text
    #webex_notify(roomId, webexToken, text)
    return response.text

def get_employee_Data():
    url = "https://reqres.in/api/users"
    headers = {}
    response = requests.get(url=url, headers=headers)
    resp = response.json()
    resp = resp['data']
    return resp

@app.route('/')
def hello_world():
    return 'test'

@app.route('/home')
def blog():
    return render_template('home.html', posts=get_employee_Data(), title='Home')

@app.route('/run')
def run():
    url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/ip-address/10.10.22.70"
    payload = {}
    headers = {
        'Accept':'application/json',
        'X-auth-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1ZTlkYmI3NzdjZDQ3ZTAwNGM2N2RkMGUiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjVkYzQ0NGQ1MTQ4NWM1MDA0YzBmYjIxMiJdLCJ0ZW5hbnRJZCI6IjVkYzQ0NGQzMTQ4NWM1MDA0YzBmYjIwYiIsImV4cCI6MTU4ODIwODQ2MCwidXNlcm5hbWUiOiJkZXZuZXR1c2VyIn0.SSn6l6AW9B4pi3XXe2JWR8UB8a5TjvpnrXuD5aygGCI'
    }
    response = requests.get(url=url, headers=headers, data=payload, verify=False)
    data = response.json()
    print(data['response'])
    return(data['response'])


@app.route('/employees')
def employees():
    return render_template('test.html', employees=get_employee_Data())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('employees'))
    return render_template('register.html',title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Successful Login {form.email.data}!', 'success')
            return redirect(url_for('employees'))
        else:
            flash(f'Login Unsuccessful', 'danger')
            return redirect(url_for('login'))
        return redirect(url_for('employees'))
    return render_template('login.html',title='login', form=form)

@app.route('/forgot')
def forgot():
    form = ForgotForm()
    return render_template('forgot_password.html',title='forgot', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8042)

token = get_token(uri_token, user, password)