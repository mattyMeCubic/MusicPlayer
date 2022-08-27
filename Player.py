from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


# Player functions and playlist
class Player(QMediaPlayer):

    def __init__(self):
        super().__init__()
        self.playlist = QMediaPlaylist()
        self.setPlaylist(self.playlist)

    # Add song to playlist
    def add_song_playlist(self, song):
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song.path)))

    # Clear playlist function
    def clear_playlist(self):
        self.playlist.clear()

    # Play next song function
    def next_song(self):
        self.playlist.next()

    # Play previous song function
    def previous_song(self):
        self.playlist.previous()

    # Function to play current highlighted song
    def play_select_song(self, index):
        self.playlist.setCurrentIndex(index)

    # Play random song from the playlist
    def shuffle_play(self):
        self.playlist.shuffle()

    # Play song in a loop
    # def loop_play(self):
    #     self.playlist.setPlaybackMode(self.playlist.Loop)
    #
    # def play_and_pause(self):
    #     pass
