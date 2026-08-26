from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main',__name__)


@main.route('/')
def index():
    page=request.args.get("page",1,type=int)
    posts=Post.query.order_by(Post.created_at.desc()).paginate(per_page=5,page=page)
    return render_template('index.html',posts=posts,page=page)