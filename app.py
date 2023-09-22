import os
from flask import Flask, request, redirect, render_template, flash, session, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from model import db, connect_db
import time
# from secret import clientId, api, DATABASE, SECRET
from forms import Register, Login, PostForm, PlaylistForm, UpdatePlaylist, UpdatePost, UpdateProfile
from models.user import User, Post
from models.playlist import Playlist
import base64
import spotipy
from spotipy.oauth2 import SpotifyOAuth



TOKEN_INFO = 'token_info'
clientId = os.environ.get("CLIENTID")
api = os.environ.get("API")

bcrypt = Bcrypt()
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE")
#postgres://localhost:dqVc4Yx114xV1VdMZ5nGkTP0kP4pDcWz@dpg-ck5pqa5drqvc73dauddg-a/spotify_db
app.config['SECRET_KEY'] = os.environ.get("SECRET")


with app.app_context():
    connect_db(app)
    db.create_all()

# Convert client id to bytes then convert to base64


client_bytes = clientId.encode("ascii")
base64_bytes = base64.b64encode(client_bytes)

# CONVERT Client Secret to bytes then base64


api_bytes = api.encode("ascii")
base64_api = base64.b64encode(api_bytes)

# Landing page route
@app.route('/', methods=['GET','POST'])
def home():
    session.pop('_flashes', None)
    return render_template('index.html')

# Send user to spotify to agree to terms and get spotify oath code for authentication
@app.route('/spot', methods=['GET','POST'])
def get_data():
    url = "https://accounts.spotify.com/authorize?"
    scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'
    return redirect(f"https://accounts.spotify.com/authorize?client_id={clientId}&response_type=code&redirect_uri=https://cap-yo2q.onrender.com/redirect&scope={scope}")

# Validate form and add user to the database
@app.route('/register', methods=['GET','POST'])
def register():
    form = Register()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        avatar = form.avatar.data
        
        user = User.register(username=username, password=password, name = name, email = email, avatar = avatar)
        if(user):
            session['user_id'] = user.username
            db.session.add(user)
            db.session.commit()
            flash(f"Added {user.username}")
            g = session.get('user_id')
            return redirect(url_for('user_page', external = True))
        else:
            session.pop('_flashes', None)
            flash("Please try again")
            return redirect("/register")
    
    else:
        return render_template('register.html', form=form)
    
# Check password and login user

@app.route('/login', methods = ['GET','POST'])
def login():
    form = Login()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        
        if(user):
            session['user_id'] = user.username
            auth_url = spotify_oath().get_authorize_url()
            return redirect(auth_url)
        else:
            session.pop('_flashes', None)
            flash("Try again")
            return redirect('/login')
    else:
        return render_template('login.html', form = form)
    
# Log user out


@app.route('/logout')
def logout():
    if(session.get('user_id')):
        session.pop("user_id")
        return redirect("/")
    else:
        return redirect("/")

@app.route('/redirect')
def redirect_page():
    try:
        if(session.get('user_id')):
            g = session.get('user_id')
            code = request.args.get('code')
            # Exchange auth code for access token 
            token_info = spotify_oath().get_access_token(code)
            session[TOKEN_INFO] = token_info
            return redirect(url_for('user_page', external = True))
        else:
            
            return redirect(url_for('register', external = True))
    except:
        if(session.get('user_id')):
            code = request.args.get('code')
            # Exchange auth code for access token 
            token_info = spotify_oath().get_access_token(code)
            session[TOKEN_INFO] = token_info
            return redirect(url_for('user_page', external = True))
        else:
            return redirect(url_for('logout', external = True))

# Get user's customized page and show top 10 releases for user
@app.route('/user')
def user_page():
    if(session.get('user_id')):
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = User.getUser(session.get('user_id'))
        new_albums = []


        all_post = Post.getAllPost()
        all_playlist = Playlist.getAll(username = user.username)
        allP = Playlist.getAllPlaylist()
        url = sp.new_releases(limit=10).get('albums').get('items')[0].get('images')[0].get('url')
        albums = sp.new_releases(limit=10)['albums']['items']

        for album in albums:
            new_albums.append(album)

        return render_template('user.html', name = user.username, url = url, new_albums = new_albums, all_post = all_post, all_playlist = allP, user = user, f = User)
    else:
        session.pop('_flashes', None)
        flash("Please login")
        return redirect('/login')



@app.route('/follow/<username>', methods = ['GET','POST'])
def follow(username):
    if(session.get('user_id')):
        followed_user = User.query.get_or_404(username)
        print(followed_user.username)
        if(session.get('user_id') == followed_user.username):
            return redirect(url_for('user_page'))
        user = User.getUser(session.get('user_id'))
        user.following.append(followed_user)
        db.session.commit()
        return redirect(url_for('user_page'))
    else:
        return redirect(url_for('login'))

@app.route('/unfollow/<username>', methods = ['GET','POST'])
def unfollow(username):
    if(session.get('user_id')):
        followed_user = User.query.get_or_404(username)
        user = User.getUser(session.get('user_id'))
        user.following.remove(followed_user)
        db.session.commit()
        return redirect(url_for('user_page'))
    else:
        return redirect(url_for('login'))






# Get users profile page
@app.route('/profile/<username>')
def profile(username):
    if(session.get('user_id')):
        user = User.getUser(username=username)
        loggedinuser = User.getUser(session.get('user_id'))
        if(user):
            posts = Post.getPost(username)
            followcount = len(user.following)
            followercount = len(user.followers)
            playlists = Playlist.getAll(username=username)
            return render_template('profile.html',u = loggedinuser, user = user, posts = posts, playlists = playlists, followercount = followercount, followingcount = followcount)
        else:
            return redirect(url_for('user_page'))
    else:
        return redirect('login')
    
@app.route('/update-profile', methods = ['GET', 'POST'])
def update_profile():
        if(session.get('user_id')):
            user = User.getUser(session.get('user_id'))
            form = UpdateProfile(obj=user)
            if form.validate_on_submit():
                user.name = form.name.data
                user.email = form.email.data
                user.avatar = form.avatar.data
                if(user):
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('user_page'))
            else:
                return render_template('update-profile.html', form = form, user=session.get('user_id'))


# Create a new post
@app.route('/register-post', methods = ['POST','GET'])
def post():
    form = PostForm()
    if(session.get('user_id')):
        if form.validate_on_submit():
            image_url = form.image.data
            new_post = form.post.data
            userpost = Post(post = new_post, image = image_url, username = session.get('user_id'))
            user = User.getUser(session.get('user_id'))
            if(userpost):
                user_post = user.post.append(userpost)
                db.session.add(userpost)
                db.session.commit()
                flash(f"Added")
                return redirect(url_for('user_page',external = True))
            else:
                return render_template('register-post.html', form = form)
        else:
            return render_template('register-post.html', form = form)
    else:
        session.pop('_flashes', None)
        flash("Please login")
        return redirect(url_for('login'))





# Update user's post
@app.route('/update-post/<int:id>', methods = ['GET', 'POST'])
def update_post(id):
    if(session.get('user_id')):
        p_id = id
        userPost = Post.getPostbyId(id = p_id)
        form = UpdatePost(obj=userPost)
        if form.validate_on_submit():
            userPost.post = form.post.data
            userPost.image = form.image.data
            if(userPost):
                db.session.add(userPost)
                db.session.commit()
                return redirect(url_for('user_page'))
        else:
            return render_template('update-post.html', form = form, post = userPost, user=session.get('user_id'))
        
# Delete user's post
@app.route('/delete-post/<int:id>', methods = ['GET', 'POST'])
def delete_post(id):
    if(session.get('user_id')):
        p_id = id
        userPost = Post.getPostbyId(id = p_id)
        if(userPost):
            db.session.delete(userPost)
            db.session.commit()
            return redirect(url_for('user_page'))
        else:
            return redirect(url_for('user_page'))
        


# Create playlist and add to spotify
@app.route('/register-playlist', methods = ['GET','POST'])
def create_playlist():
        form = PlaylistForm()
        if(session.get('user_id')):
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'])
            user = sp.me()
            if(user.get('id')):
                if form.validate_on_submit():
                    image = form.image.data
                    name = form.name.data
                    public = form.public.data
                    description = form.description.data
                    playlist = sp.user_playlist_create(user=user['id'], name = name, public=public,collaborative=False, description=description )
                    p_id = playlist.get('id')
                    if(playlist):
                        db_playlist = Playlist(playlist_id = p_id, image = image, name = name, username = session['user_id'], description = description)
                        db.session.add(db_playlist)
                        db.session.commit()
                    return redirect(url_for('user_page', external = True))      
                else:
                    return render_template('register-playlist.html', form = form, user=session.get('user_id'))
            else:
                get_token()
                return redirect(url_for('create_playlist'), external = True)
        else:
            session.pop('_flashes', None)
            flash("Please login")
            return redirect(url_for('login', extenal = True))


# Update user playlist 
@app.route('/update-playlist/<id>', methods = ['PUT','GET','POST'])
def update_playlist(id):
    if(session.get('user_id')):
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        p_id = id
        userPlaylist = Playlist.userPlaylist(p_id)
        print(userPlaylist.playlist_id)
        form = UpdatePlaylist(obj=userPlaylist)
        if form.validate_on_submit():
            image = form.image.data
            name = form.name.data
            public = form.public.data
            description = form.description.data
            userPlaylist.image = image
            userPlaylist.name = name
            userPlaylist.public = public
            userPlaylist.description = description
            sp.playlist_change_details(user=session.get('user_id'), playlist_id=id, name=name, public=public,collaborative=False, description=description)
            if(userPlaylist):
                db.session.add(userPlaylist)
                db.session.commit()
                return redirect(url_for('user_page'))
        else:
            return render_template('update-playlist.html', form = form, playlist = userPlaylist, user=session.get('user_id'))
    else:
        return redirect(url_for('login'))
    

# Delete playlist
@app.route('/delete-playlist/<id>', methods = ['DELETE','GET'])
def delete_playlist(id):
    if(session.get('user_id')):
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = User.getUser(session.get('user_id'))
        del_playlist = Playlist.deletePlaylist(id=id, user = user)
        if(del_playlist):
            sp.current_user_unfollow_playlist(playlist_id=del_playlist.playlist_id)
            db.session.delete(del_playlist)
            db.session.commit()
            return redirect(url_for('user_page'))
        else:
            return redirect(url_for('user_page')) 

        





# Get token from spotify api
def get_token():
    print(session)
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external = False))
    now = int(time.time())
    is_expired = token_info.get('expires_at') - now < 60
    if(is_expired):
        spot = spotify_oath()
        token_info = spot.refresh_access_token(token_info['refresh_token'])
    return token_info

# User agreements and user profile information. Get code from spotify api
def spotify_oath():
    return SpotifyOAuth(
            client_id = clientId,
            client_secret = api,
            redirect_uri = url_for('redirect_page', _external= True),
            scope = 'ugc-image-upload user-read-playback-state playlist-read-private playlist-modify-private user-read-email user-read-private'
            )



    
    









    




