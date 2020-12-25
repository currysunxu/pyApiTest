
class StoryblokReaderImportEntity:
    def __init__(self):
        self.__reader_name = None
        self.__reader_story = None
        self.__cover_image = None
        self.__title_audio = None
        self.__page_layout = None
        self.__layout_group = None
        self.__sentence_text = None
        self.__image_filename = None
        self.__double_image_filename = None
        self.__audio_filename = None
        self.__level = None
        self.__reader_provider = None
        self.__question_text = None
        self.__question_image = None
        self.__answer_1 = None
        self.__answer_2 = None
        self.__answer_3 = None
        self.__answer_4 = None

    @property
    def reader_name(self):
        return self.__reader_name

    @reader_name.setter
    def reader_name(self, reader_name):
        self.__reader_name = reader_name

    @property
    def reader_story(self):
        return self.__reader_story

    @reader_story.setter
    def reader_story(self, reader_story):
        self.__reader_story = reader_story

    @property
    def cover_image(self):
        return self.__cover_image

    @cover_image.setter
    def cover_image(self, cover_image):
        self.__cover_image = cover_image

    @property
    def title_audio(self):
        return self.__title_audio

    @title_audio.setter
    def title_audio(self, title_audio):
        self.__title_audio = title_audio

    @property
    def page_layout(self):
        return self.__page_layout

    @page_layout.setter
    def page_layout(self, page_layout):
        self.__page_layout = page_layout

    @property
    def layout_group(self):
        return self.__layout_group

    @layout_group.setter
    def layout_group(self, layout_group):
        self.__layout_group = layout_group

    @property
    def sentence_text(self):
        return self.__sentence_text

    @sentence_text.setter
    def sentence_text(self, sentence_text):
        self.__sentence_text = sentence_text

    @property
    def image_filename(self):
        return self.__image_filename

    @image_filename.setter
    def image_filename(self, image_filename):
        self.__image_filename = image_filename

    @property
    def double_image_filename(self):
        return self.__double_image_filename

    @double_image_filename.setter
    def double_image_filename(self, double_image_filename):
        self.__double_image_filename = double_image_filename

    @property
    def audio_filename(self):
        return self.__audio_filename

    @audio_filename.setter
    def audio_filename(self, audio_filename):
        self.__audio_filename = audio_filename

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        self.__level = level

    @property
    def reader_provider(self):
        return self.__reader_provider

    @reader_provider.setter
    def reader_provider(self, reader_provider):
        self.__reader_provider = reader_provider

    @property
    def question_text(self):
        return self.__question_text

    @question_text.setter
    def question_text(self, question_text):
        self.__question_text = question_text

    @property
    def question_image(self):
        return self.__question_image

    @question_image.setter
    def question_image(self, question_image):
        self.__question_image = question_image

    @property
    def answer_1(self):
        return self.__answer_1

    @answer_1.setter
    def answer_1(self, answer_1):
        self.__answer_1 = answer_1

    @property
    def answer_2(self):
        return self.__answer_2

    @answer_2.setter
    def answer_2(self, answer_2):
        self.__answer_2 = answer_2

    @property
    def answer_3(self):
        return self.__answer_3

    @answer_3.setter
    def answer_3(self, answer_3):
        self.__answer_3 = answer_3

    @property
    def answer_4(self):
        return self.__answer_4

    @answer_4.setter
    def answer_4(self, answer_4):
        self.__answer_4 = answer_4



