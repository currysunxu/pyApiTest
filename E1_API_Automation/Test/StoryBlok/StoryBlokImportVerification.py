import jmespath
import requests
from PIL import Image
import io
from ptest.decorator import TestClass, Test
import xlrd

from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryBlokImportUtils import StoryBlokImportUtils
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryblokVocabImportEntity import StoryblokVocabImportEntity
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryblokReaderImportEntity import StoryblokReaderImportEntity


class StoryBlokImportVerification:

    @staticmethod
    def vocab_story_check(story, vocab_entity):
        error_message = []
        if 'story' not in story:
            error_message.append(
                "There is no word named {0} at row {1} in storyblok".format(vocab_entity.vocab_name, vocab_entity.row))
        else:
            story = story['story']
            if vocab_entity.vocab_name.strip() != story['name']:
                error_message.append(
                    "The name of the word in the excel is not same as it in the storyblok at row {0}.".format(vocab_entity.row))
            if vocab_entity.category.strip() != story['content']['category'].strip():
                error_message.append(
                    "The category of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        vocab_entity.vocab_name, vocab_entity.row))
            if vocab_entity.priority.strip() != story['content']['priority'].strip():
                error_message.append(
                    "The priority of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        vocab_entity.vocab_name, vocab_entity.row))
            if vocab_entity.phonetics.strip() != story['content']['phonetics'].strip():
                error_message.append(
                    "The phonetics of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        vocab_entity.vocab_name, vocab_entity.row))
            if vocab_entity.translation.strip() != story['content']['translation_zh'].strip():
                error_message.append(
                    "The translation of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        vocab_entity.vocab_name, vocab_entity.row))
            if not vocab_entity.image_filename or vocab_entity.image_filename != story['content']['image']['filename']:
                print(vocab_entity.image_filename)
                print(story['content']['image']['filename'])
                error_message.append(
                    "The image asset of the word {0} in the excel is not same as it in the storyblok at row {1}".format(
                        vocab_entity.vocab_name, vocab_entity.row))
            if not vocab_entity.audio_filename or vocab_entity.audio_filename != story['content']['audio']['filename']:
                error_message.append(
                    "The audio asset of the word {0} in the excel is not same as it in the storyblok at row {1}".format(
                        vocab_entity.vocab_name, vocab_entity.row))
        return error_message

    @staticmethod
    def cover_page_check(reader_entity):
        error_message = []
        if 'story' not in reader_entity.reader_story:
            error_message.append(
                "There is no reader named {0} at row {1} in storyblok".format(reader_entity.reader_name, reader_entity.row))
        else:
            story = reader_entity.reader_story['story']['content']
            if reader_entity.reader_name.strip() != story['title']:
                error_message.append(
                    "The name of reader in the excel is not same as it in the storyblok at row {0}.".format(reader_entity.row))
            if reader_entity.cover_image.strip() != story['cover_image']['filename'].strip():
                error_message.append(
                    "The cover image of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.level:
                if int(reader_entity.level) != int(story['level']):
                    error_message.append(
                        "The level of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
            if reader_entity.reader_provider.strip() != story['reader_provider'].strip():
                error_message.append(
                    "The provider of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.title_audio:
                if reader_entity.title_audio != story['title_audio']['filename']:
                    error_message.append(
                        "The title audio of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
        return error_message

    @staticmethod
    def page_check(reader_entity):
        error_message = []
        if 'story' not in reader_entity.reader_story:
            error_message.append(
                "There is no reader named {0} at row {1} in storyblok".format(reader_entity.reader_name, reader_entity.row))
        else:
            page = reader_entity.reader_story['story']['content']['pages'][reader_entity.page_number]
            sentence = page['sentences'][reader_entity.sentence_number]
            if reader_entity.sentence_number == 0:
                if reader_entity.image_filename != page['page_image']['filename']:
                    error_message.append(
                        "The page image of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
                if reader_entity.page_layout != page['page_layout']:
                    error_message.append(
                        "The page layout of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
                elif reader_entity.page_layout == "doublespread":
                    if reader_entity.double_image_filename != page['page_image_doublespread']['filename']:
                        error_message.append(
                            "The double spread page image of reader {0} in the excel is not same as it in the "
                            "storyblok at row {1}.".format(
                                reader_entity.reader_name, reader_entity.row))
                    if reader_entity.layout_group != sentence['layout_group']:
                        error_message.append(
                            "The layout group of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                                reader_entity.reader_name, reader_entity.row))
            if reader_entity.sentence_text.strip() != sentence['sentence_text'].strip():
                error_message.append(
                    "The sentence text of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.audio_filename != sentence['sentence_audio']['filename']:
                error_message.append(
                    "The sentence audio of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
        return error_message

    @staticmethod
    def quiz_check(reader_entity):
        error_message = []
        if 'story' not in reader_entity.reader_story:
            error_message.append(
                "There is no reader named {0} at row {1} in storyblok".format(reader_entity.reader_name, reader_entity.row))
        else:
            quiz = reader_entity.reader_story['story']['content']['quiz'][reader_entity.quiz_number]
            if reader_entity.question_text.strip() != quiz['question_text']:
                error_message.append(
                    "The question text of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.answer_1.strip() != quiz['responses'][0]['response_text']:
                error_message.append(
                    "The response 1 of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.answer_2.strip() != quiz['responses'][1]['response_text']:
                error_message.append(
                    "The response 2 of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.answer_3:
                if reader_entity.answer_3.strip() != quiz['responses'][2]['response_text']:
                    error_message.append(
                        "The response 3 of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
            if reader_entity.answer_4:
                if reader_entity.answer_4.strip() != quiz['responses'][3]['response_text']:
                    error_message.append(
                        "The response 4 of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
            if not quiz['responses'][reader_entity.correct_answer]['correct']:
                error_message.append(
                    "The answer of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        reader_entity.reader_name, reader_entity.row))
            if reader_entity.question_image:
                if reader_entity.question_image != quiz['question_image']['filename']:
                    error_message.append(
                        "The question image of reader {0} in the excel is not same as it in the storyblok at row {1}.".format(
                            reader_entity.reader_name, reader_entity.row))
        return error_message

