from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField,URLField,BooleanField, FileField, validators
from wtforms.validators import InputRequired, DataRequired


images = UploadSet('images', IMAGES)

class Register(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    avatar = URLField("Image URL", default="https://i.ytimg.com/vi/Ryog0PHw998/maxresdefault.jpg")


class Login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])    

class PostForm(FlaskForm):
    post = StringField("What's on your mind?")
    image = URLField("Image URL", validators=[DataRequired()])

class PlaylistForm(FlaskForm):
    name = StringField('Playlist name', validators=[DataRequired()])
    public = BooleanField('Is this a private playlist',default = 'checked')
    description = StringField('Description',default= 'description')
    image = URLField('Image Url',default = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZEsCh8gEoKCKQOoSek4Prj0kKK1JDQDoCQg&usqp=CAU')

class UpdatePlaylist(FlaskForm):
    name = StringField("Update name")
    image = StringField("Update image")
    description = StringField("Description")
    public = BooleanField('Is this a private playlist')

class UpdatePost(FlaskForm):
    post = StringField("Edit post")
    image = URLField("Edit image")

class UpdateProfile(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    avatar = URLField("Image URL", default="https://i.ytimg.com/vi/Ryog0PHw998/maxresdefault.jpg")
    