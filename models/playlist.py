from model import db 


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, autoincrement = True)
    playlist_id = db.Column(db.Text, primary_key = True)
    image = db.Column(db.Text)
    name = db.Column(db.Text)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    description = db.Column(db.Text)

    @classmethod
    def getAllPlaylist(cls):
       
        playlists = Playlist.query.all()
        return playlists


    @classmethod
    def getAll(cls, username):
        all_playlist = Playlist.query.filter_by(username = username)
        return all_playlist
    
    @classmethod
    def updatePlaylist(cls, username, name, image, description):
        playlist = Playlist.query.filter_by(username)
        playlist.name = name
        playlist.image = image
        playlist.description = description
        return playlist

    @classmethod
    def userPlaylist(cls,id):
        playlist = Playlist.query.filter_by(playlist_id = id).first()
        return playlist
    @classmethod
    def deletePlaylist(cls,id, user):
        playlist = Playlist.query.filter_by(playlist_id = id).first()
        if(playlist.username == user.username):
            return playlist
        else:
            return False