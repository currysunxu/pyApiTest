import tkinter as tk
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

    @Test(tags="qa")
    def reader_or_vocab(self):
        reader_box = tk.messagebox.askyesno(title='Check reader or vocab',
                                            message='Choose Yes if you want to test reader, No if you want to test '
                                                    'vocab')
        if reader_box:
            return "reader"
        else:
            return "vocab"

    @Test(tags="qa")
    def get_zip_file(self):
        zip_name = askopenfilename()
        if '.zip' not in zip_name:
            print("Not a zip file")
            exit()
        zip_file = zipfile.ZipFile(zip_name, 'r')
        return zip_file

    @Test(tags="qa")
    def get_vocab_folder_id(self, vocab_path):
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        all_folder = story_blok_service.get_all_asset_folder().json()
        for parent_folder in all_folder["asset_folders"]:
            if parent_folder["name"] == "Vocabularies" and parent_folder["parent_id"] is None:
                parent_id = parent_folder["id"]
        for path in vocab_path:
            for parent_folder in all_folder["asset_folders"]:
                if parent_folder["parent_id"] == parent_id and parent_folder["name"] == path:
                    parent_id = parent_folder["id"]
        return parent_id

    @Test(tags="qa")
    def get_asset(self, asset_name, asset_folder_id):
        story_blok_service = StoryBlokService(StoryBlokData.StoryBlokService['host'])
        new_asset_name = story_blok_service.get_asset(asset_name).json()
        for each_asset in new_asset_name["assets"]:
            if each_asset["asset_folder_id"] == asset_folder_id:
                return each_asset
        return None

    @Test(tags="qa")
    def check_vocab_asset(self):
        zip_file = self.get_zip_file()
        image_root = zip_file.namelist()[0]
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
            image_path = row_data[5]
            audio_path = row_data[6]
            image_asset_lower = image_path.split('/')[-1]
            image_asset_lower = re.sub(r'\W', "-", image_asset_lower.rsplit('.', 1)[0]) + "." + \
                                image_asset_lower.rsplit('.', 1)[1]
            audio_asset_lower = audio_path.split('/')[-1]
            audio_asset_lower = re.sub(r'\W', "-", audio_asset_lower.rsplit('.', 1)[0]) + "." + \
                                audio_asset_lower.rsplit('.', 1)[1]
            image_folder_id = self.get_vocab_folder_id(image_path.split('/')[1:-1])
            audio_folder_id = self.get_vocab_folder_id(audio_path.split('/')[1:-1])
            image_asset = self.get_asset(image_asset_lower, image_folder_id)
            audio_asset = self.get_asset(audio_asset_lower, audio_folder_id)
            assert_that(image_asset is not None)
            assert_that(audio_asset is not None)
            assert_that(image_asset["title"], equal_to("/Vocabularies" + image_path))
            assert_that(audio_asset["title"], equal_to("/Vocabularies" + audio_path))
            image_name = image_root + image_path
            with zip_file.open(image_name, mode='r') as image_file:
                content = image_file.read()
                image_size_check = Image.open(io.BytesIO(bytearray(content)))
            assert_that(str(image_size_check.width) in image_asset["filename"])
            assert_that(str(image_size_check.height) in image_asset["filename"])
