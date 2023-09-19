from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from werkzeug.utils import secure_filename
from mongoengine.errors import NotUniqueError
from ..forms import (
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
    UpdateProfilePicForm,
)
from ..models import User
from ..utils import get_b64_img


users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:         
        return redirect(url_for('index'))
    
    form = RegistrationForm()     
    if form.validate_on_submit():         
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')         
        user = User(username=form.username.data,                     
                    email=form.email.data, password=hashed)         
        user.save()   
        flash("Register successfully", "success")      
        return redirect(url_for('users.login'))
    elif request.method == 'POST':
        flash("Error, registration failed", "fail")

    
    return render_template('register.html', title='Register', form=form)



@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:         
        return redirect(url_for('index'))
     
    form = LoginForm()     
    if form.validate_on_submit():         
        user = User.objects(username=form.username.data).first()

        if (user is not None and
            bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)             
            return redirect(url_for('users.account'))
        else:
            flash("Error, check your username and password", "fail")
            return redirect(url_for("users.login"))
                   
    return render_template('login.html', title='Login', form=form)



@users.route("/logout")
@login_required
def logout():
    logout_user()     
    return redirect(url_for('movies.index'))

@users.route("/reviews")
@login_required
def reviews():    
    return redirect(url_for('users.user_detail'))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()

    if update_username_form.validate_on_submit():
        try:
            current_user.username = update_username_form.new_username.data
            current_user.save()
            flash("Username updated successfully", "success")
            return redirect(url_for("users.account"))
        except NotUniqueError:
            flash("Error, username already exists", "fail")

    if update_profile_pic_form.validate_on_submit():
        image = update_profile_pic_form.profile_pic.data
        
        if image is not None:
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'
            
            if current_user.profile_pic.get() is None:             
                current_user.profile_pic.put(image.stream, content_type=content_type)         
            else:             
                current_user.profile_pic.replace(image.stream, content_type=content_type)         
            current_user.save()

            flash("Profile picture updated successfully", "success")
            return redirect(url_for('users.account'))

    image = get_b64_img(current_user.username)
    return render_template("account.html", image=image, update_username_form=update_username_form, update_profile_pic_form=update_profile_pic_form)