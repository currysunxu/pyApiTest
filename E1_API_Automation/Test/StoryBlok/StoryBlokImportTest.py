import jmespath
from PIL import Image
import io
from tkinter import Tk, Button
from ptest.decorator import TestClass, Test
import xlrd

from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData
from E1_API_Automation.Business.StoryBlok.StoryBlokUtils.StoryBlokUtils import StoryBlokUtils


#@TestClass()
class StoryBlokImportCheckTool:
    def __init__(self, test_type = "Vocabularies", env_name = "Oneapp"):
        self.root = test_type
        self.env_name = env_name
        self.mywindow = Tk()

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
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        new_asset_name = story_blok_service.get_asset(self.env_name, asset_name).json()
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
        print(name)
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

    def check_vocab_asset(self):
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        all_folder = story_blok_service.get_all_asset_folder(self.env_name).json()
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
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        all_folder = story_blok_service.get_all_asset_folder(self.env_name).json()
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


if __name__ == '__main__':
    test_type = "Vocab"
    #ttype = "Readers"
    #env_name = "Oneapp"
    test = StoryBlokImportCheckTool()
    if test_type == "Reader":
        error_message = test.check_reader_asset()
    else:
        error_message = test.check_vocab_asset()
    if not error_message:
        print("No error")
    else:
        for error_message in error_message:
            print("Error %d" % error_message.index(error_message) + ": " + error_message)
