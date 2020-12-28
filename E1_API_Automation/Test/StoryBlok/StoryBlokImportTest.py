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
from E1_API_Automation.Test.StoryBlok.StoryBlokImportVerification import StoryBlokImportVerification


@TestClass()
class StoryBlokImportCheckTool:
    def __init__(self, env_name="Oneapp"):
        self.root = "Vocabularies"
        self.env_name = env_name

    def get_folder_id(self, all_path, all_folder):
        parent_id = jmespath.search("asset_folders[?name == '{}'].id".format(self.root), all_folder)[0]
        for path in all_path:
            if '\'' in path:
                for asset_name in all_folder['asset_folders']:
                    if asset_name['name'] == path and asset_name['parent_id'] == parent_id:
                        path_id = asset_name['id']
            else:
                path_id = jmespath.search(
                    "asset_folders[?name == '{0}' && parent_id == `{1}`].id".format(path.replace("'", "\'"), parent_id),
                    all_folder)[0]
            if path_id:
                parent_id = path_id
            else:
                parent_id = []
                break
        return parent_id

    def get_asset(self, asset_name, asset_folder_id):
        page_number = 1
        page_size = 1000
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        while True:
            new_asset_name = story_blok_service.get_asset(asset_name, page_number, page_size).json()
            asset = jmespath.search("assets[?asset_folder_id == `{0}`]".format(asset_folder_id), new_asset_name)
            for real_asset in asset:
                asset_filename = real_asset["filename"].split('/')[-1]
                if asset_filename == asset_name:
                    return real_asset
            if new_asset_name['assets'] == page_size:
                page_number += 1
            else:
                return None

    def get_asset_filename(self, path, all_folder, asset_name):
        asset_folder_id = self.get_folder_id(path, all_folder)
        filename = None
        if asset_folder_id:
            if asset_name:
                filename = self.get_asset(asset_name, asset_folder_id)
        else:
            return None
        if not filename:
            return None
        return filename['filename']

    def get_reader_type(self, row_data):
        folder_path = [row_data[0].strip(), row_data[3].strip()]  # folder name and title
        if row_data[13] == "EF":
            self.root = "EF readers"
            folder_path = [row_data[1]] + folder_path
            full_slug = "readers/content/" + StoryBlokImportUtils.convert_slug_name(
                self.root) + "/" + StoryBlokImportUtils.convert_slug_name(row_data[1])
        elif not row_data[16]:
            self.root = "Assigned readers"
            folder_path = [row_data[1]] + folder_path
            full_slug = "readers/content/" + StoryBlokImportUtils.convert_slug_name(
                self.root) + "/" + StoryBlokImportUtils.convert_slug_name(row_data[1])
        else:
            self.root = "Unassigned readers"
            full_slug = "readers/content/" + StoryBlokImportUtils.convert_slug_name(
                self.root)
        return folder_path, full_slug

    def asset_check(self, folder_id, file_type, zip_file, root, row, path):
        asset_lower = StoryBlokImportUtils.convert_asset_name(path.split('/')[-1])
        asset = self.get_asset(asset_lower, folder_id)
        error_message = []
        name = root + path
        if name not in zip_file.namelist():
            error_message.append("The {0} at row {1} is not in the zip file".format(file_type, row + 1))
        elif not asset:
            error_message.append(
                "The {0} at row {1} is not exist in the storyblok but it is in the zip file".format(file_type, row + 1))
        elif asset["title"] != path:
            error_message.append("The title is not correct for the {0} at row {1}".format(file_type, row + 1))
        elif file_type == "Image":
            with zip_file.open(name, mode='r') as image_file:
                content = image_file.read()
            image_size_check = Image.open(io.BytesIO(bytearray(content)))
            image_size = str(image_size_check.width) + "x" + str(image_size_check.height)
            if str(image_size) not in asset["filename"]:
                error_message.append("The image size is not correct at row {0}".format(row + 1))
        return error_message

    def check_vocab_asset(self):
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        all_folder = story_blok_service.get_all_asset_folder().json()
        zip_file = StoryBlokImportUtils.get_zip_file()
        namelist_ = zip_file.namelist()[0]
        image_root = namelist_
        image_root = image_root.strip("/")
        for excel_name in zip_file.namelist():
            if '.xlsx' not in excel_name:
                continue
            with zip_file.open(excel_name, 'r') as x:
                excel_data = xlrd.open_workbook(file_contents=x.read())
        excel_table = excel_data.sheets()[0]
        nrows = excel_table.nrows
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            course = row_data[0].strip()  # column 1 is used to store the course information of a vocab
            image_path = row_data[5].strip()  # column 6 is used to store the image path of a vocab
            audio_path = row_data[6].strip()  # column 7 is used to store the audio path of a vocab
            if not image_path:
                error_message.append("Image is empty at row {0} ".format(i + 1))
                continue
            if not audio_path:
                error_message.append("Audio is empty at row {0} ".format(i + 1))
                continue
            image_folder_id = self.get_folder_id([course] + image_path.split('/')[1:-1], all_folder)
            audio_folder_id = self.get_folder_id([course] + audio_path.split('/')[1:-1], all_folder)
            if not image_folder_id:
                error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                continue
            if not audio_folder_id:
                error_message.append("The audio path does not exist in the storyblok at row {0}".format(i + 1))
                continue
            error_message.extend(
                self.asset_check(image_folder_id, "Image", zip_file, image_root, i, image_path))
            error_message.extend(
                self.asset_check(audio_folder_id, "Audio", zip_file, image_root, i, audio_path))
        return error_message

    def check_reader_asset(self):
        global folder_id
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        all_folder = story_blok_service.get_all_asset_folder().json()
        zip_file = StoryBlokImportUtils.get_zip_file()
        namelist_ = zip_file.namelist()[0]
        image_root = namelist_
        image_root = image_root.strip("/")
        for excel_name in zip_file.namelist():
            if '.xlsx' not in excel_name:
                continue
            with zip_file.open(excel_name, 'r') as x:
                excel_data = xlrd.open_workbook(file_contents=x.read())
                break
        excel_table = excel_data.sheets()[0]
        nrows = excel_table.nrows
        last_page_number = 0
        folder_path = []  # folder name and title
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            page_number = row_data[5]
            course = row_data[1]
            if page_number == '':  # Check for question
                image_path = row_data[28]
                if image_path == '':
                    continue
                else:
                    if not folder_id:
                        error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                        continue
                    error_message.extend(
                        self.asset_check(folder_id, "Image", zip_file, image_root, i, image_path.strip()))
                    continue
            if int(page_number) == 1:  # Check for cover image
                folder_path, full_slug = self.get_reader_type(row_data)
                image_path = row_data[14].strip()
                # The asset for each book store in the same folder
                folder_id = self.get_folder_id(folder_path,
                                               all_folder)  # Only get folder id of the asset when page# is 1 for each book
                if not folder_id:
                    error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                    continue
                error_message.extend(
                    self.asset_check(folder_id, "Image", zip_file, image_root, i, image_path))
                if row_data[4] != '':
                    # Check title audio
                    error_message.extend(
                        self.asset_check(folder_id, "Audio", zip_file, image_root, i, row_data[4].strip()))
            elif page_number:
                if last_page_number != page_number:  # Check if there is a new page
                    image_path = row_data[6]
                    double_image = row_data[7]
                    if not folder_id:
                        error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                        continue
                    error_message.extend(
                        self.asset_check(folder_id, "Image", zip_file, image_root, i, image_path))
                    if double_image:
                        # Check double spread image
                        error_message.extend(
                            self.asset_check(folder_id, "Image", zip_file, image_root, i, double_image))
                audio_path = row_data[11]
                error_message.extend(
                    self.asset_check(folder_id, "Audio", zip_file, image_root, i, audio_path))
                last_page_number = page_number
        return error_message

    def check_vocab_story(self):
        error_message = []
        excel_table = StoryBlokImportUtils.get_excel_file()
        nrows = excel_table.nrows
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        all_folder = story_blok_service.get_all_asset_folder().json()
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            full_slug = "vocabularies/content/"
            full_slug += StoryBlokImportUtils.convert_slug_name(row_data[0]) + "/" + StoryBlokImportUtils.convert_slug_name(
                row_data[1]) + "/" + StoryBlokImportUtils.convert_slug_name(
                row_data[2]) + "/" + StoryBlokImportUtils.convert_slug_name(row_data[3])
            vocab_story = story_blok_service.get_story_by_full_slug(full_slug).json()
            image_path = row_data[5].strip()  # column 6 is used to stored the image path of a vocab
            audio_path = row_data[6].strip()  # column 7 is used to stored the audio path of a vocab
            image_asset = StoryBlokImportUtils.convert_asset_name(row_data[5].split('/')[-1]).strip()
            audio_asset = StoryBlokImportUtils.convert_asset_name(row_data[6].split('/')[-1]).strip()
            course = row_data[0]
            image_asset_filename = self.get_asset_filename([course] + image_path.split('/')[1:-1], all_folder,
                                                           image_asset)
            audio_asset_filename = self.get_asset_filename([course] + audio_path.split('/')[1:-1], all_folder,
                                                           audio_asset)
            vocab_entity = StoryblokVocabImportEntity(row_data[3])
            # assign values to each word
            vocab_entity.category = row_data[11]
            vocab_entity.priority = row_data[13]
            vocab_entity.phonetics = row_data[4]
            vocab_entity.translation = row_data[8]
            vocab_entity.image_filename = image_asset_filename
            vocab_entity.audio_filename = audio_asset_filename
            vocab_entity.row = i
            error_message.extend(StoryBlokImportVerification.vocab_story_check(vocab_story, vocab_entity))
        return error_message

    def check_reader_story(self):
        global folder_id
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        all_folder = story_blok_service.get_all_asset_folder().json()
        excel_table = StoryBlokImportUtils.get_excel_file()
        nrows = excel_table.nrows
        last_page_number = 0
        full_slug = ""
        reader_entity = StoryblokReaderImportEntity()
        sentence_number = 0
        quiz_number = 0
        folder_path = []
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            page_number = row_data[5]
            if page_number:
                if int(page_number) == 1:  # get a book, check for cover page
                    last_page_number = 0
                    quiz_number = 0
                    reader_entity = StoryblokReaderImportEntity()
                    folder_path, full_slug = self.get_reader_type(row_data)
                    if row_data[4]:
                        title_audio = StoryBlokImportUtils.convert_asset_name(row_data[4].split('/')[-1])
                        title_audio_filename = self.get_asset_filename(folder_path, all_folder, title_audio)
                        reader_entity.title_audio = title_audio_filename
                    image_path = row_data[14]
                    full_slug += "/" + StoryBlokImportUtils.convert_slug_name(
                        row_data[0]) + "/" + StoryBlokImportUtils.convert_slug_name(row_data[3])
                    reader_story = story_blok_service.get_story_by_full_slug(full_slug).json()
                    reader_entity.reader_story = reader_story
                    reader_entity.reader_name = row_data[3]
                    cover_image = StoryBlokImportUtils.convert_asset_name(image_path.split('/')[-1])
                    cover_image_filename = self.get_asset_filename(folder_path, all_folder, cover_image)
                    reader_entity.cover_image = cover_image_filename
                    reader_entity.level = row_data[16]
                    reader_entity.reader_provider = row_data[13]
                    reader_entity.row = i
                    error_message.extend(StoryBlokImportVerification.cover_page_check(reader_entity))
                    # The asset for each book store in the same folder
                else:   # check for page
                    if last_page_number != page_number:
                        sentence_number = 0
                        image_path = row_data[6]
                        page_image = StoryBlokImportUtils.convert_asset_name(image_path.split('/')[-1])
                        page_image_filename = self.get_asset_filename(folder_path, all_folder, page_image)
                        reader_entity.image_filename = page_image_filename
                        if row_data[7]:
                            double_image = StoryBlokImportUtils.convert_asset_name(row_data[7].split('/')[-1])
                            double_image_filename = self.get_asset_filename(folder_path, all_folder, double_image)
                            reader_entity.double_image_filename = double_image_filename
                    else:
                        sentence_number += 1
                        reader_entity.sentence_text = row_data[9]
                        reader_entity.page_layout = row_data[8]
                        reader_entity.layout_group = row_data[10]
                        audio_path = row_data[11]
                        sentence_audio = StoryBlokImportUtils.convert_asset_name(audio_path.split('/')[-1])
                        sentence_audio_filename = self.get_asset_filename(folder_path, all_folder, sentence_audio)
                        reader_entity.audio_filename = sentence_audio_filename
                        reader_entity.page_number = page_number
                        reader_entity.sentence_number = sentence_number
                        reader_entity.row = i
                        error_message.extend(StoryBlokImportVerification.page_check(reader_entity))
                        last_page_number = page_number
            elif page_number == '':     # check for quiz
                reader_entity.question_text = row_data[22]
                reader_entity.answer_1 = row_data[23]
                reader_entity.answer_2 = row_data[24]
                reader_entity.answer_3 = row_data[25]
                reader_entity.answer_4 = row_data[26]
                answer = ord(row_data[27].lower()) - 97
                if row_data[28]:
                    question_image = StoryBlokImportUtils.convert_asset_name(row_data[28].split('/')[-1])
                    question_image_filename = self.get_asset_filename(folder_path, all_folder, question_image)
                    reader_entity.question_image = question_image_filename
                reader_entity.correct_answer = answer
                reader_entity.quiz_number = quiz_number
                reader_entity.row = i
                error_message.extend((StoryBlokImportVerification.quiz_check(reader_entity)))
                quiz_number += 1
                continue
        return error_message


if __name__ == '__main__':
    test_type = "Reader"  # Switch between Reader and Vocab
    env_name = "Oneapp"  # Switch between Oneapp and Dev
    test = StoryBlokImportCheckTool(env_name)

    if test_type == "Reader":
        error_message = test.check_reader_asset()
    else:
        error_message = test.check_vocab_asset()
    if not error_message:
        print("No error")
    else:
        for each_error_message in error_message:
            print("Error %d" % error_message.index(each_error_message) + ": " + each_error_message)
    error_message = []
    if test_type == "Reader":
        error_message = test.check_reader_story()
    else:
        error_message = test.check_vocab_story()
    if not error_message:
        print("No error")
    else:
        for each_error_message in error_message:
            print("Error %d" % error_message.index(each_error_message) + ": " + each_error_message)
