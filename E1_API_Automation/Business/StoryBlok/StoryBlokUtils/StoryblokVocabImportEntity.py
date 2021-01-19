
class StoryblokVocabImportEntity:
    def __init__(self, vocab_name):
        self.__vocab_name = vocab_name
        self.__category = None
        self.__priority = None
        self.__phonetics = None
        self.__translation = None
        self.__image_filename = None
        self.__audio_filename = None
        self.__row = None

    @property
    def vocab_name(self):
        return self.__vocab_name

    @vocab_name.setter
    def vocab_name(self, vocab_name):
        self.__vocab_name = vocab_name

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category):
        self.__category = category

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        self.__priority = priority

    @property
    def phonetics(self):
        return self.__phonetics

    @phonetics.setter
    def phonetics(self, phonetics):
        self.__phonetics = phonetics

    @property
    def translation(self):
        return self.__translation

    @translation.setter
    def translation(self, translation):
        self.__translation = translation

    @property
    def image_filename(self):
        return self.__image_filename

    @image_filename.setter
    def image_filename(self, image_filename):
        self.__image_filename = image_filename

    @property
    def audio_filename(self):
        return self.__audio_filename

    @audio_filename.setter
    def audio_filename(self, audio_filename):
        self.__audio_filename = audio_filename

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, row):
        self.__row = row