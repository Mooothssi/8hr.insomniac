from i18n.en_US import *
from i18n.th_TH import *


class Language:
    def __init__(self, full_name, short_name, dictionary={}):
        self.short_name = short_name
        self.full_name = full_name
        self.dictionary = dictionary


class Localization():
    __instance = None
    "Allow players to customize their own language."
    def __init__(self, default="en_US"):
        self.languages = {}
        self.default_lang = default
        self.add_language(Language("English (US)", "en_US", LOC_TEXTS_EN_US))
        self.add_language(Language("Thai", "th_TH", LOC_TEXTS_TH))
        self.Instance = self

    @staticmethod
    def instance():
        if Localization.__instance is None:
            Localization.__instance = Localization()
        return Localization.__instance

    def add_language(self, language: Language):
        self.languages[language.short_name] = language

    def get_translated_text(self, key="!ERROR!"):
        return self.languages[self.default_lang].dictionary[key]


class LocalizedText:
    def __init__(self, key, locale=Localization()):
        self.key = key
        self.locale = locale

    def get(self):
        self.locale.get_translated_text(self.key)

    def __str__(self):
        return self.locale.get_translated_text(self.key)
