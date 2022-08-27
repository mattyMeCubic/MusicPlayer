# Song  Data Transfer Object(DTO)
class SongModel:
    name = ''
    album = ''
    artist = ''
    track_num = 0
    path = ''

    # This function create the feature, we are using object print() and print all data in object
    def __str__(self):
        return "Name :{0}\n Album :{1} \n Artist :{2} \n Track num :{3}".format(self.name, self.album, self.artist,
                                                                                self.track_num)
