from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QSlider, QFileDialog, QAction, QTableWidget, QTableWidgetItem, \
    QHeaderView, QMessageBox, QAbstractItemView

from FileLoad import FileLoad
from Player import Player


# Converting milliseconds to seconds and minutes
def min_sec(i):
    s = 1000  # There is 1000 milliseconds in one second
    m = 60000  # There is 60000 milliseconds in one minute
    minutes, x = divmod(i, m)
    seconds, _ = divmod(x, s)
    return "%d:%02d" % (minutes, seconds)


class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()
        # Loading the UI file
        uic.loadUi('ui/main.ui', self)
        # Declare player object
        self.player = Player()

        # Find and create pyqt5 component objects
        self.button_play = self.findChild(QPushButton, 'play_btn')
        self.button_pause = self.findChild(QPushButton, 'pause_btn')
        self.button_previous = self.findChild(QPushButton, 'prev_song_btn')
        self.button_next = self.findChild(QPushButton, 'next_song_btn')
        self.button_stop = self.findChild(QPushButton, 'stop_btn')
        self.refresh_btn = self.findChild(QPushButton, 'refresh_btn')
        self.vol_slider = self.findChild(QSlider, 'vol_slider')
        self.change_action = self.findChild(QAction, 'action_change')
        self.song_list = self.findChild(QTableWidget, 'song_list')
        self.duration_slider = self.findChild(QSlider, 'duration_slider')
        self.shuffle_btn = self.findChild(QPushButton, 'shuffle_btn')
        self.repeat_btn = self.findChild(QPushButton, 'repeat_btn')

        # Set pyqt5 QTableWidget properties
        self.song_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.song_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.song_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.song_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.song_list.verticalHeader().setVisible(False)

        # Create File load QThread object
        self.file_loader = FileLoad()

        # Using QSetting save last open directory
        self.settings = QSettings('Music Player', 'Config')

        # Load save directory
        self.load_save_directory_song()

        # Connect table select change
        self.song_list.itemSelectionChanged.connect(self.select_song)

        # Directory open action
        self.change_action.triggered.connect(self.load_files)

        # Select current play song in table
        self.player.playlist.currentIndexChanged.connect(
            lambda: self.song_list.selectRow(self.player.playlist.currentIndex()))

        # Refresh button connected to refresh song list function of QMediaPlayer
        self.refresh_btn.clicked.connect(self.refresh_song_list)

        # Play button connected to play function of QMediaPlayer
        self.button_play.clicked.connect(self.player.play)

        # Pause button connected to pause function of QMediaPlayer
        self.button_pause.clicked.connect(self.player.pause)

        # NextSong button connected to next song function of QMediaPlayer
        self.button_next.clicked.connect(self.player.next_song)

        # Play songs in shuffle
        self.shuffle_btn.clicked.connect(self.player.shuffle_play)

        # self.repeat_btn.clicked.connect(self.player.loop_play)

        # Previous Song button connected to previous song function
        self.button_previous.clicked.connect(self.player.previous_song)

        # Stop currently played song
        self.button_stop.clicked.connect(self.player.stop)

        # Volume slider connect to set volume function
        self.vol_slider.valueChanged.connect(self.player.setVolume)

        # Update position of duration slider
        self.player.durationChanged.connect(self.update_duration)

        # Update timer of the song
        self.player.positionChanged.connect(self.update_timer)

        # Curation slider connect to position function
        self.duration_slider.valueChanged.connect(self.player.setPosition)

        # Connect file load tread single
        self.file_loader.songs.connect(self.display_songs)

        # Connect file load tread single
        self.file_loader.error.connect(self.error)

        # Duration update

    def update_duration(self, duration):
        self.duration_slider.setMaximum(duration)
        # Duration Timer update

    def update_timer(self, timer):
        if timer >= 0:
            self.time_label.setText(min_sec(timer))

        # To prevent triggering
        self.duration_slider.blockSignals(True)
        self.duration_slider.setValue(timer)
        self.duration_slider.blockSignals(False)

    # Load and save music directory
    def load_save_directory_song(self):
        # Get previous open folder value, if value is none set default value empty string
        self.file_loader.folder = self.settings.value('directory', '', str)
        # Check folder for not value none or empty start file , mp3 file load thread
        if self.file_loader.folder != '' or self.file_loader.folder is not None:
            self.file_loader.start()

    # Load the mp3 files chosen by user select directory
    def load_files(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.settings.setValue('directory', folder)
            self.file_loader.folder = folder
            self.file_loader.start()

    @pyqtSlot(list)
    def display_songs(self, songs):
        # Clear old playlist
        self.player.playlist.clear()
        # Reset song table list
        self.song_list.setRowCount(0)
        # Iterate song model list and append table
        for song in songs:
            row_position = self.song_list.rowCount()
            song.row_index = row_position
            self.song_list.insertRow(row_position)
            self.song_list.setItem(row_position, 0, QTableWidgetItem(str(song.track_num)))
            self.song_list.setItem(row_position, 1, QTableWidgetItem(str(song.name)))
            self.song_list.setItem(row_position, 2, QTableWidgetItem(str(song.album)))
            self.song_list.setItem(row_position, 3, QTableWidgetItem(str(song.artist)))
            # Add song playlist
            self.player.add_song_playlist(song)

    # Refresh list of songs function for refresh button
    def refresh_song_list(self):
        if self.file_loader.folder is None or self.file_loader.folder == '':
            QMessageBox.warning(self, 'Music Player', 'Please select music directory')
        else:
            self.file_loader.start()

    def select_song(self):
        # Get user select song index and set it player
        self.player.play_select_song(self.song_list.selectionModel().currentIndex().row())
        # User select song but player not playing the song then start playing song
        if QMediaPlayer.StoppedState == self.player.state():
            self.player.play()

    @pyqtSlot(str)
    def error(self, error):
        # Any error generated by mp3 file loading then show user error
        QMessageBox.information(self, 'Music Player', error)

    def close(self):
        # When application close destroy player object in memory
        self.player.destroyed()
