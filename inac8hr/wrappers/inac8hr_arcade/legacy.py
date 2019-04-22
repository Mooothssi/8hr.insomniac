from distutils.version import LooseVersion, StrictVersion
from arcade import version

class ArcadeLegacy():
    ARCADE_VERSION = ""
    ARCADE_LEGACY = False

    @classmethod
    def is_arcade_legacy(cls, given_version="1.3.7"):
        if cls.ARCADE_VERSION == "":
            cls.ARCADE_LEGACY = LooseVersion(version.VERSION) <= LooseVersion(given_version)
            cls.ARCADE_VERSION = version.VERSION
        return cls.ARCADE_LEGACY