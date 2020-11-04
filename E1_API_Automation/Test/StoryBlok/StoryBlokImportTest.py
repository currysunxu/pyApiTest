import tkinter as tk

import jmespath
from PIL import Image
import io
from tkinter import messagebox
from ptest.decorator import TestClass, Test
from tkinter.filedialog import askopenfilename
import xlrd
import zipfile
from hamcrest import assert_that, equal_to
from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData
import re


@TestClass()
class StoryBlokImportTestCases:
    def __init__(self):
        self.vocab_root = "Vocabularies"
        self.env_name = "Oneapp"

    def get_zip_file(self):
        zip_name = askopenfilename()
        if '.zip' not in zip_name:
            print("Not a zip file")
            exit()
        zip_file = zipfile.ZipFile(zip_name, 'r')
        return zip_file

    def get_vocab_folder_id(self, vocab_path, all_folder):
        parent_id = jmespath.search("asset_folders[?name == '{}'].id".format(self.vocab_root), all_folder)[0]
        for path in vocab_path:
            path_id = jmespath.search("asset_folders[?name == '{0}' && parent_id == `{1}`].id".format(path, parent_id), all_folder)[0]
            parent_id = path_id
        return parent_id

    def get_asset(self, asset_name, asset_folder_id):
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        new_asset_name = story_blok_service.get_asset('Oneapp', asset_name).json()
        asset = jmespath.search("assets[?asset_folder_id == `{0}`] | [0]".format(asset_folder_id), new_asset_name)
        return asset

    @Test(tags="qa")
    def check_vocab_asset(self):
        error_message = []
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        all_folder = story_blok_service.get_all_asset_folder(self.env_name).json()
        zip_file = self.get_zip_file(self)
        self.namelist_ = zip_file.namelist()[0]
        image_root = self.namelist_
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
            image_asset_lower = image_path.split('/')[-1]
            image_asset_lower = re.sub(r'\W', "-", image_asset_lower.rsplit('.', 1)[0]) + "." + \
                                image_asset_lower.rsplit('.', 1)[1]
            audio_asset_lower = audio_path.split('/')[-1]
            audio_asset_lower = re.sub(r'\W', "-", audio_asset_lower.rsplit('.', 1)[0]) + "." + \
                                audio_asset_lower.rsplit('.', 1)[1]
            image_folder_id = self.get_vocab_folder_id(self, image_path.split('/')[1:-1], all_folder)
            audio_folder_id = self.get_vocab_folder_id(self, audio_path.split('/')[1:-1], all_folder)
            image_asset = self.get_asset(self, image_asset_lower, image_folder_id)
            audio_asset = self.get_asset(self, audio_asset_lower, audio_folder_id)
            if image_asset is None:
                error_message.append("The image at row {0} is not exist".format(i+1))
            elif image_asset["title"] != ("/" + self.vocab_root + image_path):
                error_message.append("The title is not correct for the image at row {0}".format(i+1))
            else:
                image_name = image_root + image_path
                with zip_file.open(image_name, mode='r') as image_file:
                    content = image_file.read()
                    image_size_check = Image.open(io.BytesIO(bytearray(content)))
                image_size = str(image_size_check.height) + "x" + str(image_size_check.width)
                if str(image_size) not in image_asset["filename"]:
                    error_message.append("The image size is not correct at row {0}".format(i+1))
            if audio_asset is None:
                error_message.append("The audio at row {0} is not exist".format(i+1))
            elif audio_asset["title"] != ("/" + self.vocab_root + audio_path):
                error_message.append("The title is not correct for the audio at row {0}".format(i+1))


if __name__ == '__main__':
    test = StoryBlokImportTestCases
    test.__init__(test)
    error_message_vocab = test.check_vocab_asset(test)
