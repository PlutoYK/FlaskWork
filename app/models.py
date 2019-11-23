from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from app import login,app
from datetime import datetime
from flask_login import UserMixin
import jwt
from time import time
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

followers = db.Table('followers',
                   db.Column('follower_id',db.Integer,db.ForeignKey('users.id')),
                   db.Column('followed_id',db.Integer,db.ForeignKey('users.id'))
)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # 粉丝关注模型
    followed = db.relationship('User',secondary = followers,primaryjoin=(followers.c.follower_id==id),
                                secondaryjoin=(followers.c.followed_id == id),
    backref = db.backref('followers',lazy = 'dynamic'),lazy = 'dynamic')
    #  关注实现
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
            return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    #
    def followed_posts(self):

        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter\
            (followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    def get_reset_password_token(self,expires_in=600):
        return jwt.encode({'reset_password':self.id,'exp':time()+expires_in},app.config['SECRET_KEY'],algorithm= 'HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


