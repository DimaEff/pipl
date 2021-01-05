from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# followers = db.Table('followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('friend', db.Boolean, default=False)
# )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(12), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followeds = association_proxy('followeds', 'follower')
    followers = association_proxy('followers', 'followed')

    def __repr__(self):
        return 'User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            i = Follower(follower=self, followed=user)
            friend = Follower.query.get([user.id, self.id])
            if friend:
                i.friend == True
                friend.friend == True
            db.session.add(i)
            db.session.commit()
            # Изначально не было переменной f в предыдущем условии
            # f = Follower.query.get([self.id, user.id])
            # f.friend == True

    def unfollow(self, user):
        if self.is_following(user):
            i = Follower.query.get([self.id, user.id])
            friend = Follower.wuery.get([user.id, self.id])
            if friend:
                friend.friend == False
            db.session.delete(i)
            db.session.commit()

    def get_followers(self):
        return db.session.query(Follower). \
            filter(Follower.follower == self, Follower.friend == False).all()

    def get_friends(self):
        return db.session.query(Follower). \
            filter(Follower.follower == self, Follower.friend == True).all()

    def is_following(self, user):
        return Follower.query.get([self.id, user.id])

    def is_friend(self, user):
        if Follower.query.get(self.id, user.id) and Follower.query.get(user.id, self.id):
            return True


class Follower(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend = db.Column(db.Boolean, default=False)

    follower = db.relationship(User,
                               primaryjoin=(follower_id == User.id),
                               backref='followeds')
    followed = db.relationship(User,
                               primaryjoin=(followed_id == User.id),
                               backref='followers')


    # follower_u = db.relationship('User', primaryjoin=(Follower.followed_id == id), back_populates='followed_u', lazy='dynamic')
    # followed_u = db.relationship('User', primaryjoin=(Follower.follower_id == id), back_populates='follower_u', lazy='dynamic')
    # followed = db.relationship(
    #     'User',
    #     secondary=Follower,
    #     primaryjoin=(Follower.follower_id == id),
    #     secondaryjoin=(Follower.followed_id == id),
    #     backref=db.backref('follower', lazy='dynamic'),
    #     lazy='dynamic'
    # )
    # followed = db.relationship(
    #     'User',
    #     secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers', lazy='dynamic'),
    #     lazy='dynamic'
    # )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post: {}>'.format(self.body)