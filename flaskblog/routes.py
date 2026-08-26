from flask import render_template , flash , redirect ,url_for , request , current_app , abort
from flaskblog import app , db , bcrypt
from flaskblog.forms import RegisterForm, LoginForm , updateForm , NewPost
from flask_login import login_required , login_user , logout_user , current_user
from flaskblog.models import User , Post
from sqlalchemy.exc import IntegrityError
import secrets
import os
from PIL import Image

class AuthError(Exception):
    pass

@app.route('/')
def index():
    page=request.args.get("page",1,type=int)
    posts=Post.query.order_by(Post.created_at.desc()).paginate(per_page=5,page=page)
    return render_template('index.html',posts=posts,page=page)

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Account created successfully", 'success')
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("Unable to create account.",'danger')
            return redirect(url_for('register'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['POST','GET'])
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
            return redirect(url_for('index'))
        except AuthError as e:
            flash(str(e),'danger')
            return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@app.route('/profile',methods=['POST','GET'])
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
            return redirect(url_for('profile'))
        except IntegrityError:
            flash("Unable to update account.",'danger')
            return redirect(url_for('profile'))
    elif request.method=='GET':
        form.email.data=current_user.email
        form.username.data=current_user.username
    return render_template('profile.html',form=form)

@app.route('/post/new',methods=['POST','GET'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, body=form.content.data, author=current_user)
        db.session.add(new_post)
        try:
            db.session.commit()
            flash("Post Published Successfully",'success')
            return redirect(url_for('index'))
        except IntegrityError:
            flash("Unable to publish post",'danger')
            return redirect(url_for('new_post'))
    return render_template('newpost.html',form=form,legend="Create New Post",title="Create New Post")

@app.route('/post/<int:id>')
def view_post(id):
    post=Post.query.get_or_404(id)
    return render_template("post.html",post=post)

@app.route('/post/<int:id>/update',methods=['POST','GET'])
@login_required
def update_post(id):
    post=Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = NewPost()
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.content.data
        try:
            db.session.commit()
            flash("Post updated successfully",'success')
            return redirect(url_for('view_post',id=id))
        except IntegrityError:
            flash("Failed to update post",'danger')
            return redirect(url_for('update_post'))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.body
    return render_template("newpost.html",post=post,form=form,legend="Update Post",title="Update Post")


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

@app.route('/post/<int:id>/delete',methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    try:
        db.session.commit()
        flash("Post Deleted Successfully",'success')
        return redirect(url_for('index'))
    except IntegrityError:
        flash("Failed to delete post",'danger')
        return redirect(url_for('delete_post',id=id))

@app.route('/user/<int:id>')
def user_posts(id):
    user=User.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter(Post.author==user).order_by(Post.created_at.desc()).paginate(per_page=5, page=page)
    return render_template('user_posts.html',posts=posts,user=user)




    return render_template('index.html',posts=posts,page=page)


# TODO : keep this on memery if something failed dont redirect except render template
# TODO : we want to redirect after post request if we render it can make the post request again
# TODO : try by sending post to delete route using curl








