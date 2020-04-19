# Import flask and template operators
from flask import Flask, render_template,send_from_directory,redirect,url_for,flash,request,json
from flask_login import LoginManager,current_user,login_user,logout_user,login_required
from app.userModel import User
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Json config
jsonconf = json.load(open(app.config['JSON_CONFIG_PATH']))


@login.user_loader
def user_loader(email):
    if email not in User.users:
        return
    user = User()
    user.id = email
    return user


@login.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in User.users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == User.users[email]['password']

    return user


@app.route('/')
@app.route('/login.html')
@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    if email in User.users and request.form['password'] == User.users[email]['password']:
        user = User()
        user.id = email
        login_user(user)

        next = request.args.get('next')
        return redirect(url_for('index'))

    return  render_template("error_auth.html")

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

#@app.route('/login')
#def test_login():
 #   return render_template("auth/login.html")


@app.route('/logout')
@login_required
def do_logout():
    logout_user()
    return redirect("login")

@login.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

print(app.static_folder)

#page navigation,所有有导航的模块,都必须在这里引入一下,否则没法注册app.route()
from app  import views
from app.mod_user import forms
from app.mod_commodity import forms
from app.mod_motion import forms
from app.mod_org import forms