#Importing necessary modules
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import time
#Registering Blueprints for Auth.
auth = Blueprint('auth',__name__)

#defining user login func.
@auth.route('/login', methods=["POST",'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("LOGGED in!!",category='succces')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("incorrect password",category='error')
        else:
            flash('Email does not exist.',category='error')   
    return render_template('login.html',user = current_user)

#defining LOgout func.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#definining Sign-up
@auth.route('/sign-up',methods =["POST",'GET'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        #To check if user alredy exists or not
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email exist..",category='error')
        #Password min requirements
        elif len(email) < 4:
            flash('Email must be greater than 4 char.',category='error')
        elif len(first_name) <2:
            flash('FirstName must be greater than 1 char.',category='error')
        elif password !=password2:
            flash('Passwords don\'t match/',category='error')
        elif len(password)<5:
            flash('Password must be greater than 5 char.',category='error')
        else:
            #Adding new user to database
            new_user = User(email=email ,first_name=first_name,password=generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            # Autologin user after sucessful commit to Database
            login_user(new_user,remember= True)
            return redirect(url_for('views.home'))
            flash('Account Created...',category="success")
    # If GET req from /sign-up page then this will execute
    return render_template('sign_up.html',user = current_user)

 