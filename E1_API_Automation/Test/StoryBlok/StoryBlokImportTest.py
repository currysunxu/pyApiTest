import jmespath
import requests
from PIL import Image
import io
from ptest.decorator import TestClass, Test
import xlrd

from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryBlokUtils import StoryBlokUtils
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils

@TestClass()
class StoryBlokImportCheckTool:
    def __init__(self, env_name="Oneapp"):
        self.root = "Vocabularies"
        self.env_name = env_name
        self.vocab_name = None
        self.category = None
        self.priority = None
        self.phonetics = None
        self.translation = None

    def get_folder_id(self, vocab_path, all_folder):
        parent_id = jmespath.search("asset_folders[?name == '{}'].id".format(self.root), all_folder)[0]
        for path in vocab_path:
            path_id = jmespath.search("asset_folders[?name == '{0}' && parent_id == `{1}`].id".format(path, parent_id),
                                      all_folder)
            if path_id:
                parent_id = path_id[0]
            else:
                parent_id = []
                break
        return parent_id

    def get_asset(self, asset_name, asset_folder_id):
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        new_asset_name = story_blok_service.get_asset(asset_name).json()
        asset = jmespath.search("assets[?asset_folder_id == `{0}`]".format(asset_folder_id), new_asset_name)
        for real_asset in asset:
            asset_filename = real_asset["filename"].split('/')[-1]
            if asset_filename == asset_name:
                return real_asset
        return None

    def asset_check(self, folder_id, file_type, zip_file, root, row, path, type):
        asset_lower = StoryBlokUtils.convert_asset_name(path.split('/')[-1])
        asset = self.get_asset(asset_lower, folder_id)
        error_message = []
        name = root + path
        if type == "Vocab":
            new_path = "/" + self.root + path
        else:
            new_path = path
        if name not in zip_file.namelist():
            error_message.append("The {0} at row {1} is not in the zip file".format(file_type, row + 1))
        elif not asset:
            error_message.append(
                "The {0} at row {1} is not exist in the storyblok but it is in the zip file".format(file_type, row + 1))
        elif asset["title"] != new_path:
            error_message.append("The title is not correct for the {0} at row {1}".format(file_type, row + 1))
        elif file_type == "Image":
            with zip_file.open(name, mode='r') as image_file:
                content = image_file.read()
            image_size_check = Image.open(io.BytesIO(bytearray(content)))
            image_size = str(image_size_check.width) + "x" + str(image_size_check.height)
            if str(image_size) not in asset["filename"]:
                error_message.append("The image size is not correct at row {0}".format(row + 1))
        return error_message

    def vocab_story_check(self, story, image_asset, audio_asset,row):
        error_message = []
        if 'story' not in story:
            error_message.append("There is no word named {0} at row {1} in storyblok".format(name, row))
        else:
            story = story['story']
            if self.vocab_name.strip() != story['name']:
                error_message.append(
                    "The name of the word in the excel is not same as it in the storyblok at row {0}.".format(row))
            if self.category != story['content']['category']:
                error_message.append(
                    "The category of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        self.vocab_name, row))
            if self.priority != story['content']['priority']:
                error_message.append(
                    "The priority of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        self.vocab_name, row))
            if self.phonetics.strip() != story['content']['phonetics'].strip():
                error_message.append(
                    "The phonetics of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        self.vocab_name, row))
            if self.translation != story['content']['translation_zh']:
                error_message.append(
                    "The translation of the word {0} in the excel is not same as it in the storyblok at row {1}.".format(
                        self.vocab_name, row))
            if not image_asset or image_asset not in story['content']['image']['filename']:
                error_message.append(
                    "The image asset of the word {0} in the excel is not same as it in the storyblok at row {1}".format(
                        self.vocab_name, row))
            if not audio_asset or audio_asset not in story['content']['audio']['filename']:
                error_message.append(
                    "The audio asset of the word {0} in the excel is not same as it in the storyblok at row {1}".format(
                        self.vocab_name, row))
        return error_message

    def get_asset_filename(self,vocab_path, all_folder, asset_name):
        asset_folder_id = self.get_folder_id(vocab_path, all_folder)
        if asset_folder_id:
            if asset_name:
                filename = self.get_asset(asset_name, asset_folder_id)
        if not filename:
            return None
        return filename['filename']

    def check_vocab_asset(self):
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        all_folder = story_blok_service.get_all_asset_folder().json()
        zip_file = StoryBlokUtils.get_zip_file()
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
            image_path = row_data[5]  # column 6 is used to stored the image path of a vocab
            audio_path = row_data[6]  # column 7 is used to stored the audio path of a vocab
            if not image_path:
                error_message.append("Image is empty at row {0} ".format(i + 1))
                continue
            if not audio_path:
                error_message.append("Audio is empty at row {0} ".format(i + 1))
                continue
            image_folder_id = self.get_folder_id(image_path.split('/')[1:-1], all_folder)
            audio_folder_id = self.get_folder_id(audio_path.split('/')[1:-1], all_folder)
            if not image_folder_id:
                error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                continue
            if not audio_folder_id:
                error_message.append("The audio path does not exist in the storyblok at row {0}".format(i + 1))
                continue
            error_message.extend(
                self.asset_check(image_folder_id, "Image", zip_file, image_root, i, image_path, "Vocab"))
            error_message.extend(
                self.asset_check(audio_folder_id, "Audio", zip_file, image_root, i, audio_path, "Vocab"))
        return error_message

    def check_reader_asset(self):
        global folder_id
        self.root = "Readers"
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        all_folder = story_blok_service.get_all_asset_folder().json()
        zip_file = StoryBlokUtils.get_zip_file()
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
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            page_number = row_data[3]
            folder_path = [row_data[0], row_data[2]]  # folder name and title
            if page_number == '':  # Check for question
                image_path = row_data[24]
                if image_path == '':
                    continue
                else:
                    if not folder_id:
                        error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                        continue
                    error_message.extend(
                        self.asset_check(folder_id, "Image", zip_file, image_root, i, image_path, "Reader"))
                    continue
            if int(page_number) == 1:  # Check for cover image
                image_path = row_data[10]
                # The asset for each book store in the same folder
                folder_id = self.get_folder_id(folder_path,
                                               all_folder)  # Only get folder id of the asset when page# is 1 for each book
                if not folder_id:
                    error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                    continue
                error_message.extend(
                    self.asset_check(folder_id, "Image", zip_file, image_root, i, image_path, "Reader"))
            elif page_number:
                if last_page_number != page_number:  # Check if there is a new page
                    image_path = row_data[4]
                    if not folder_id:
                        error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                        continue
                    error_message.extend(
                        self.asset_check(folder_id, "Image", zip_file, image_root, i, image_path, "Reader"))
                audio_path = row_data[7]
                error_message.extend(
                    self.asset_check(folder_id, "Audio", zip_file, image_root, i, audio_path, "Reader"))
                last_page_number = page_number

    def check_vocab_story(self):
        error_message = []
        excel_table = StoryBlokUtils.get_excel_file()
        nrows = excel_table.nrows
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'], self.env_name)
        all_folder = story_blok_service.get_all_asset_folder().json()
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            full_slug = "vocabularies/content/"
            full_slug += StoryBlokUtils.convert_slug_name(row_data[0]) + "/" + StoryBlokUtils.convert_slug_name(
                row_data[1]) + "/" + StoryBlokUtils.convert_slug_name(
                row_data[2]) + "/" + StoryBlokUtils.convert_slug_name(row_data[3])
            vocab_story = story_blok_service.get_story_by_full_slug(full_slug).json()
            image_path = row_data[5]  # column 6 is used to stored the image path of a vocab
            audio_path = row_data[6]  # column 7 is used to stored the audio path of a vocab
            image_asset = StoryBlokUtils.convert_asset_name(row_data[5].split('/')[-1])
            audio_asset = StoryBlokUtils.convert_asset_name(row_data[6].split('/')[-1])
            image_asset_filename = self.get_asset_filename(image_path.split('/')[1:-1], all_folder, image_asset)
            audio_asset_filename = self.get_asset_filename(audio_path.split('/')[1:-1], all_folder, audio_asset)
            # assign values to each word
            self.vocab_name = row_data[3]
            self.category = row_data[11]
            self.priority = row_data[13]
            self.phonetics = row_data[4]
            self.translation = row_data[8]
            error_message.extend(self.vocab_story_check(vocab_story,image_asset_filename, audio_asset_filename, i))
        return error_message


if __name__ == '__main__':
    test_type = "Vocab"  # Switch between Reader and Vocab
    env_name = "Oneapp"  # Switch between Oneapp and Dev
    test = StoryBlokImportCheckTool(env_name)
    '''
    if test_type == "Reader":
        error_message = test.check_reader_asset()
    else:
        error_message = test.check_vocab_asset()
    if not error_message:
        print("No error")
    else:
        for error_message in error_message:
            print("Error %d" % error_message.index(error_message) + ": " + error_message)
    error_message = []
    '''
    if test_type == "Reader":
        error_message = test.check_reader_asset()
    else:
        error_message = test.check_vocab_story()
    if not error_message:
        print("No error")
    else:
        for each_error_message in error_message:
            print("Error %d" % error_message.index(each_error_message) + ": " + each_error_message)
