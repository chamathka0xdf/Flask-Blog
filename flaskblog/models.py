from flaskblog import db , login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(
        db.Integer,
        primary_key=True
            )

    username=db.Column(
        db.String(100),
        nullable=False,
        unique=True
            )

    email=db.Column(db.String(100),
                    nullable=False,
                    unique=True
                )

    password=db.Column(db.String(255),
                       nullable=False
    )
    image_file=db.Column(db.String(50),
                         nullable=False,
                         default='default.webp'
                    )
    created_at=db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.utcnow
                    )

    posts=db.relationship('Post',
                          back_populates='author',
                          lazy=True
                        )

    def __repr__(self):
        return f"User({self.id} {self.username} {self.email} {self.password} {self.image_file})"

class Post(db.Model):
    __tablename__="posts"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(250),nullable=False)
    body=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    author_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    author = db.relationship('User', back_populates='posts')
    def __repr__(self):
        return f"User({self.id} {self.title} {self.body}  {self.author_id})"