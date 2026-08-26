from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.post.forms import NewPost

post = Blueprint('post',__name__)


@post.route('/post/new',methods=['POST','GET'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, body=form.content.data, author=current_user)
        db.session.add(new_post)
        try:
            db.session.commit()
            flash("Post Published Successfully",'success')
            return redirect(url_for('main.index'))
        except IntegrityError:
            flash("Unable to publish post",'danger')
            return redirect(url_for('post.new_post'))
    return render_template('newpost.html',form=form,legend="Create New Post",title="Create New Post")

@post.route('/post/<int:id>')
def view_post(id):
    post=Post.query.get_or_404(id)
    return render_template("post.html",post=post)

@post.route('/post/<int:id>/update',methods=['POST','GET'])
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
            return redirect(url_for('post.view_post',id=id))
        except IntegrityError:
            flash("Failed to update post",'danger')
            return redirect(url_for('post.update_post'))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.body
    return render_template("newpost.html",post=post,form=form,legend="Update Post",title="Update Post")




@post.route('/post/<int:id>/delete',methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    try:
        db.session.commit()
        flash("Post Deleted Successfully",'success')
        return redirect(url_for('main.index'))
    except IntegrityError:
        flash("Failed to delete post",'danger')
        return redirect(url_for('post.delete_post',id=id))