from i18n.en_US import *
from i18n.th_TH import *


class Language:
    def __init__(self, full_name, short_name, dictionary={}, font_name=None):
        self.short_name = short_name
        self.full_name = full_name
        self.dictionary = dictionary
        self.font_name = font_name


class Localization():
    __instance = None
    "Allow players to customize their own language."
    def __init__(self, default="en_US"):
        self.languages = {}
        self.default_lang = default
        self.add_language(Language("English (US)", "en_US", LOC_TEXTS_EN_US,
                                   "assets/fonts/NotoSans-Regular"))
        self.add_language(Language("Thai", "th_TH", LOC_TEXTS_TH,
                                   "assets/fonts/SansThai-Regular"))
        self.initialized = True

    @staticmethod
    def instance():
        if Localization.__instance is None:
            Localization.__instance = Localization()
        return Localization.__instance

    def add_language(self, language: Language):
        self.languages[language.short_name] = language
        
    def set_language_by_code(self, lang_short_name: str):
        self.default_lang = lang_short_name

    def get_translated_text(self, key="!ERROR!"):
        if key in self.languages[self.default_lang].dictionary:
            return self.languages[self.default_lang].dictionary[key]
        else:
            return f"!MISSING! {key}!"

    def get_localized_font_name(self):
        return self.languages[self.default_lang].font_name


class LocalizedText:
    def __init__(self, key):
        self.key = key
        self.locale = Localization.instance()

    def get(self):
        self.locale.get_translated_text(self.key)

    def __str__(self):
        return self.locale.get_translated_text(self.key)
