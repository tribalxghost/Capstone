# from model import db




# class Post(db.Model):

#     __tablename__ = "post"
#     id = db.Column(db.Integer, primary_key = True, autoincrement=True)
#     post = db.Column(db.Text, nullable = True)
#     image = db.Column(db.Text, nullable = False)
#     username = db.Column(db.String, db.ForeignKey('users.username'))


#     @classmethod
#     def getPost(cls, username):
#         all_post = Post.query.filter_by( username = username)
#         return all_post
    
#     @classmethod
#     def getAllPost(cls):
#         posts = Post.query.all()
#         return posts


#     @classmethod
#     def getPostbyId(cls, id):
#         p = Post.query.filter_by(id = id).first()
#         print(p)
#         return p
    






