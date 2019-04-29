from inac8hr.loaders.dirs import GameDirectories
from inac8hr.levels.tilemaps import TILEMAP


class ImageLoader():
    ASSET_ROOT = GameDirectories.IMAGES

    @classmethod
    def get_texture_filename_from_index(cls, idx):
        return f"{ImageLoader.ASSET_ROOT}/levels/{TILEMAP[idx]}.png"
