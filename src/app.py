from flask import Flask, render_template, session, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin,login_user,LoginManager,logout_user,current_user,login_required
#from werkzeug.urls import url_encode
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,BooleanField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt
import mysql.connector


app = Flask(__name__)

connection = mysql.connector.connect(
    user='root',password='12345',host='localhost',port='3306')
cursor = connection.cursor()
cursor.execute("CREATE DATABASE auth_user")
cursor.execute("USE auth_user")
cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                        ID int NOT NULL,
                        email varchar(20),
                        password varchar(20),
                        PRIMARY KEY (ID))
                    ''')


# print(app.config['SQLALCHEMY_DATABASE_URI'])

app.config['SECRET_KEY'] = 'tsecrectkeyashonlyknows'
bootstrap = Bootstrap5(app)


#In the python shell CLI type
#from app import app,db
#app.app_context().push()
#db.create_all()




# Define the User model


# def __repr__(self):
#     return f'<User{self.username}>'

class RegisterForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(),Length(min=2,max=20)] , render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)],render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/register', methods=("GET", "POST"))
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        email=form.email.data
        pswd = form.password.data
        sql = "INSERT INTO user(email,password) VALUES("+email +","+ pswd+")"
        cursor.execute()
        return redirect(url_for('login'))

    
    return render_template('register.html',form =form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form=LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        pswd = form.password.data
        cursor.execute("SELECT password FROM user")
        ps_sql = cursor.fectall()
        cursor.executr("SELECT email FROM user")
        em_sql = cursor.fetchall()
        count_ps=0
        count_em=0
        res1=0
        res2=0
        data=[{email}]
        for p in ps_sql:
            if p==pswd:
                res1=1
            count_ps+=1
        for e in em_sql:
            if e==email:
                res2=1
            count_em+=1
        if(res1==res2 and count_em==count_ps):
            return render_template('Profile.html',data=data)    
    
    return render_template('login.html',form=form)



@app.route('/logout')
def logout():
    logout_user()
    redirect(url_for('login'))


@app.route('/Profile')
def Profile():
    return render_template('Profile.html')

if __name__ == '__main__':

    app.run(debug=True)


