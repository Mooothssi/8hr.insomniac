from platform import system
import typing
import pyglet
from pyglet.media.player import Player
import copy
import threading

class AudioFile():
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.source = None

    def load_source(self):
        """
            Loads audio file into the memory as a Pyglet's AudioSource
        """
        self.source = pyglet.media.load(self.file_name)

    def play(self):
        # if self.source.is_queued:
        #     self.source = pyglet.media.load(self.file_name)
        #     self.source.play()
        # else:
        self.source.play()

    def pause(self):
        self.source.pause()


class AudioEngine():
    _ffmpeg2_loaded = False
    _instance = None

    def __init__(self):
        self.sources = {}
        self.player = Player()

    def add_source_from_filename(self, filename: str, file_id: str, lazy_load=False):
        audio_file = AudioFile(filename)
        if not lazy_load:
            audio_file.load_source()
        self.sources[file_id] = audio_file

    def play_by_id(self, id: str):
        file_ = self.sources[id]
        source = file_.source
        player = Player()

        def play(source, player):
            if source.is_queued:
                source = pyglet.media.load(file_.file_name)
                source.play()
            else:
                player.queue(source)
                player.play()
            source._players.append(self.player)

            def _on_player_eos():
                source._players.remove(self.player)
                player.on_player_eos = None
                player.delete()

            player.on_player_eos = _on_player_eos

        play(source, player)

    def load_sound_library(self):
        """
            Loads the proper avbin (audio library) automatically.\n
            It loads from our directory first, otherwise loads the installed 
            package (maybe incorrect).
        """
        if not AudioEngine._ffmpeg2_loaded:
            AudioEngine._ffmpeg2_loaded = True
        else:
            return
        import pyglet_ffmpeg2
        pyglet_ffmpeg2.load_ffmpeg()

    @staticmethod
    def get_instance():
        if AudioEngine._instance is None:
            AudioEngine._instance = AudioEngine()
        return AudioEngine._instance
