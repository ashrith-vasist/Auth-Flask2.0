from flask import Flask, render_template, session, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin,login_user,LoginManager,logout_user,current_user,login_required
from werkzeug.urls import url_encode
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "check_same_thread": False
    }
}

# print(app.config['SQLALCHEMY_DATABASE_URI'])

app.config['SECRET_KEY'] = 'tsecrectkeyashonlyknows'
bootstrap = Bootstrap5(app)
bcrypt= Bcrypt(app)
db = SQLAlchemy(app)

#In the python shell CLI type
#from app import app,db
#app.app_context().push()
#db.create_all()


login_manager = LoginManager()#app and flask login to wroktoghter
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader#reload
def load_suer(user_id):
    return User.query.get(int(user_id))


# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False,unique=True)
    password = db.Column(db.String(80), nullable=False)

# def __repr__(self):
#     return f'<User{self.username}>'

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=2,max=20)] , render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)],render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
    # for validation of username , when the user inputs the username its used to validate it
    def validate_username(sel, username):
        exisiting_user_username = User.query.filter_by(
            username=username.data).first()

        if exisiting_user_username:
            raise ValidationError(
                "That username already exists . Please choose a diffrenet one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=2,max=20)] , render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)],render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/register', methods=("GET", "POST"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    
    return render_template('register.html',form =form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('Profile'))
    return render_template('login.html',form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    redirect(url_for('login'))


@app.route('/Profile')
@login_required
def Profile():
    return render_template('Profile.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


