from distutils.version import LooseVersion, StrictVersion
from arcade import version

class ArcadeLegacy():
    ARCADE_VERSION = ""
    ARCADE_LEGACY = False

    @staticmethod
    def is_arcade_legacy():
        if ArcadeLegacy.ARCADE_VERSION == "":
            ArcadeLegacy.ARCADE_LEGACY = LooseVersion(version.VERSION) <= LooseVersion("1.3.7")
            ArcadeLegacy.ARCADE_VERSION = version.VERSION
        return ArcadeLegacy.ARCADE_LEGACY