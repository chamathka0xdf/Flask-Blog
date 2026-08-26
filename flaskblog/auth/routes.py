from flask import render_template, url_for, flash, redirect, request, Blueprint , current_app
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.auth.forms import RegisterForm, LoginForm, updateForm
import os
import secrets
from PIL import Image
from sqlalchemy.exc import IntegrityError

class AuthError(Exception):
    pass

auth = Blueprint('auth',__name__)


@auth.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Account created successfully", 'success')
            return redirect(url_for("auth.login"))
        except IntegrityError:
            db.session.rollback()
            flash("Unable to create account.",'danger')
            return redirect(url_for('auth.register'))
    return render_template('register.html',form=form)

@auth.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        try:
            if not user:
                raise AuthError("Invalid email or password")
            if not bcrypt.check_password_hash(user.password, form.password.data):
                raise AuthError("Invalid email or password")
            login_user(user,remember=form.remember.data)
            flash("Logged in successfully.",'success')
            next_page=request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        except AuthError as e:
            flash(str(e),'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html',form=form)

@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))

@auth.route('/profile',methods=['POST','GET'])
@login_required
def profile():
    form=updateForm()
    if form.validate_on_submit():
        if form.profilepic.data:
            savepicture(form.profilepic.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()
            flash("Account Updated Successfully",'success')
            return redirect(url_for('auth.profile'))
        except IntegrityError:
            flash("Unable to update account.",'danger')
            return redirect(url_for('auth.profile'))
    elif request.method=='GET':
        form.email.data=current_user.email
        form.username.data=current_user.username
    return render_template('profile.html',form=form)

@auth.route('/user/<int:id>')
def user_posts(id):
    user=User.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter(Post.author==user).order_by(Post.created_at.desc()).paginate(per_page=5, page=page)
    return render_template('user_posts.html',posts=posts,user=user)


def savepicture(profilepic):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(profilepic.filename)
    filename=random_hex + f_ext
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath=os.path.join(upload_folder,filename)
    output_size=(125,125)
    i = Image.open(profilepic)
    i.thumbnail(output_size)
    i.save(filepath)
    current_user.image_file=filename
    try:
        db.session.commit()
    except IntegrityError:
        raise