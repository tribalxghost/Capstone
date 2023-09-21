from model import db
from flask_bcrypt import Bcrypt
import datetime
bcrypt = Bcrypt()


userPost = db.Table('user_post',
                    db.Column('user_username', db.Text, db.ForeignKey('users.username')),
                    db.Column('user_post', db.Integer, db.ForeignKey('post.id'))
                    )
postComments = db.Table('post_comment',
                    db.Column('comment', db.Integer, db.ForeignKey('comment.id')),
                    db.Column('post', db.Integer, db.ForeignKey('post.id'))
                    )






class Follows(db.Model):
    __tablename__ = 'follows'

    user_being_followed = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )

    user_following = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )




class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.Text, primary_key=True, nullable = False, unique = True)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    post = db.relationship('Post',secondary=userPost, backref='user_post')
    avatar = db.Column(db.Text)
    playlist = db.relationship('Playlist',backref ='user_playlist')
    
   
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed == username),
        secondaryjoin=(Follows.user_following == username)
    )


    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following == username),
        secondaryjoin=(Follows.user_being_followed == username)
    )



    
    @classmethod
    def register(cls, username, password, name, email, avatar):
        user = User.query.filter_by(username=username).first()
        if(user == None):
            hashed = bcrypt.generate_password_hash(password)
            hashed_utf8 = hashed.decode("utf8")
            return cls(username = username, password = hashed_utf8, name = name, email = email, avatar = avatar)
        else:
            return False
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
    @classmethod
    def getUser(cls, username):
        user = User.query.filter_by(username = username).first()
        return user
    @classmethod 
    def getAllUsers(cls):
        user = User.query.all()
    
    @classmethod
    def getPost(cls):
        return
    
    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

    


    



class Post(db.Model):

    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    post = db.Column(db.Text, nullable = True)
    image = db.Column(db.Text, nullable = False)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now(),
    )
    comments = db.relationship('Comment',secondary=postComments, backref='comment')
 



    @classmethod
    def getPost(cls, username):
        all_post = Post.query.filter_by( username = username)
        return all_post
    
    @classmethod
    def getAllPost(cls):
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        return posts


    @classmethod
    def getPostbyId(cls, id):
        p = Post.query.filter_by(id = id).first()
        print(p)
        return p






class Comment(db.Model):
    """Post comments"""

    __tablename__ = 'comment'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now(),
    )

    user_id = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False,
    )

