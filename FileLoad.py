import traceback
from os import walk
from os.path import join

import eyed3
from PyQt5.QtCore import QThread, pyqtSignal

from model.SongModel import SongModel


class FileLoad(QThread):
    songs = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.folder = None
        self.extension = '.mp3'
        self.song_model_list = []

    def run(self):
        try:
            self.song_model_list = []
            unknown_count = 0
            # Walk function get all folder , files in user selected folder
            for root, dirs, files in walk(self.folder):
                # Iterate all files in folder
                for file in files:
                    # Check file extension if file extension is .mp3
                    if file.endswith(self.extension):
                        # Create new song model
                        song_model = SongModel()
                        # Join file path to root path
                        song_model.path = join(root, file)
                        # Extract all mp3 file metadata using eyeD3 library
                        song_data = eyed3.load(song_model.path)
                        # Only show errors
                        eyed3.log.setLevel('ERROR')
                        # Check song name none, if it is none set the song name to unknown
                        song_model.name = song_data.tag.title if song_data.tag.title else 'unknown  name'.format(
                            unknown_count)
                        # Check song album name, none if it is none, set the song album to unknown
                        song_model.album = song_data.tag.album if song_data.tag.album else 'unknown '
                        # Check song artist none if it is none, set the song artist to unknown
                        song_model.artist = song_data.tag.artist if song_data.tag.artist else 'unknown'
                        # Single line if else check song track_num tuple first index value none
                        # If is none  set song track_num  is unknown_count
                        song_model.track_num = song_data.tag.track_num[0] if song_data.tag.track_num[
                            0] else unknown_count
                        # Append song model in song model list
                        self.song_model_list.append(song_model)
                        # Add one to unknown_count
                        unknown_count += 1
            # Using sorted build in function of python sort song model list by album, artist and track_num
            self.song_model_list = sorted(self.song_model_list,
                                          key=lambda model: (model.album, model.artist, model.track_num))
            # This line notify GUI application song list that is ready to play
            self.songs.emit(self.song_model_list)

        except Exception as e:
            # If any exception, throw in mp3 file searching, traceback the error and emit error into GUI message box
            traceback.print_exc()
            self.error.emit(str(e))
