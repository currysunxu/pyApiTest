
import jmespath
from PIL import Image
import io
from tkinter import Tk,Button
from ptest.decorator import TestClass, Test
from tkinter.filedialog import askopenfilename
import xlrd
import zipfile
from E1_API_Automation.Business.StoryBlok.StoryBlokService import StoryBlokService
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData
import re


@TestClass()
class StoryBlokImportCheckTool:
    def __init__(self):
        self.root = "Vocabularies"
        self.env_name = "Oneapp"
        self.mywindow = Tk()

    def get_zip_file(self):
        zip_name = askopenfilename()
        if '.zip' not in zip_name:
            print("Not a zip file")
            exit()
        zip_file = zipfile.ZipFile(zip_name, 'r')
        return zip_file

    def get_folder_id(self, vocab_path, all_folder):
        parent_id = jmespath.search("asset_folders[?name == '{}'].id".format(self.root), all_folder)[0]
        for path in vocab_path:
            path_id = jmespath.search("asset_folders[?name == '{0}' && parent_id == `{1}`].id".format(path, parent_id), all_folder)
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

    def set_env_oneapp(self):
        self.env_name = "Oneapp"

    def set_env_dev(self):
        self.env_name = "Dev"


    def get_env(self):
        self.mywindow.title("Please select the environment")
        self.mywindow.geometry("%dx%d+%d+%d" % (300, 100, 200, 200))
        b1 = Button(self.mywindow, text='set env to Oneapp', relief='raised', width=16, height=1, command=lambda :self.set_env_oneapp(self))
        b2 = Button(self.mywindow, text='set env to Dev', relief='raised', width=16, height=1, command=self.set_env_dev(self))
        b3 = Button(self.mywindow, text='Quit', relief='raised', width=16, height=1, command=self.mywindow.quit)
        b1.grid(row=1, column=1, padx=2, pady=10)
        b2.grid(row=1, column=2, padx=2, pady=10)
        b3.grid(row=2, column=1, padx=2, pady=10)
        self.mywindow.mainloop()

    def vocab_asset_check(self, asset, imagetype, zip_file, name, row, path):
        error_message = []
        if name not in zip_file.namelist():
            error_message.append("The {0} at row {1} is not in the zip file".format(imagetype, row + 1))
        elif not asset:
            error_message.append("The {0} at row {1} is not exist in the storyblok but it is in the zip file".format(imagetype, row + 1))
        elif asset["title"] != ("/" + self.root + path):
            error_message.append("The title is not correct for the {0} at row {1}".format(imagetype, row + 1))
        elif imagetype == "Image":
            with zip_file.open(name, mode='r') as image_file:
                content = image_file.read()
            image_size_check = Image.open(io.BytesIO(bytearray(content)))
            image_size = str(image_size_check.width) + "x" + str(image_size_check.height)
            if str(image_size) not in asset["filename"]:
                error_message.append("The image size is not correct at row {0}".format(row + 1))
        return error_message

    def convert_asset_name(self, asset_name):
        if len(asset_name.rsplit('.', 1)) == 2:
            asset_name = re.sub(r'\W', "-", asset_name.rsplit('.', 1)[0]).rstrip('-') + "." + asset_name.rsplit('.', 1)[1]
            new_asset_name = [""]
            for str in asset_name:
                if str != new_asset_name[-1] or str != '-':
                    new_asset_name.append(str)
            convert_name = ''.join(new_asset_name).lower()
            return convert_name
        return None

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
            if not image_path:
                error_message.append("Image is empty at row {0} ".format(i+1))
                continue
            if not audio_path:
                error_message.append("Audio is empty at row {0} ".format(i+1))
                continue
            image_asset_lower = self.convert_asset_name(self, image_path.split('/')[-1])
            audio_asset_lower = self.convert_asset_name(self, audio_path.split('/')[-1])

            image_folder_id = self.get_folder_id(self, image_path.split('/')[1:-1], all_folder)
            audio_folder_id = self.get_folder_id(self, audio_path.split('/')[1:-1], all_folder)
            if not image_folder_id:
                error_message.append("The image path does not exist in the storyblok at row {0}".format(i+1))
                continue
            if not audio_folder_id:
                error_message.append("The audio path does not exist in the storyblok at row {0}".format(i+1))
                continue
            image_asset = self.get_asset(self, image_asset_lower, image_folder_id)
            audio_asset = self.get_asset(self, audio_asset_lower, audio_folder_id)
            image_name = image_root + image_path
            audio_name = image_root + audio_path
            error_message.extend(self.vocab_asset_check(self, image_asset, "Image", zip_file, image_name, i, image_path))
            error_message.extend(self.vocab_asset_check(self, audio_asset, "Audio", zip_file, audio_name, i, audio_path))
        return error_message

    def check_book(self, folder, book_type):
        if 'Level' in folder:
            self.root = "Readers"
        elif book_type == "Highlights China":
            self.root = "Assigned readers"
        else:
            self.root = "EF readers"

    def reader_asset_check(self, asset, imagetype, zip_file, name, row, path):
        error_message = []
        if name not in zip_file.namelist():
            error_message.append("The {0} at row {1} is not in the zip file".format(imagetype, row + 1))
        elif not asset:
            error_message.append("The {0} at row {1} is not exist in the storyblok but it is in the zip file".format(imagetype, row + 1))
        elif asset["title"] != path:
            error_message.append("The title is not correct for the {0} at row {1}".format(imagetype, row + 1))
        elif imagetype == "Image":
            with zip_file.open(name, mode='r') as image_file:
                content = image_file.read()
            image_size_check = Image.open(io.BytesIO(bytearray(content)))
            image_size = str(image_size_check.width) + "x" + str(image_size_check.height)
            if str(image_size) not in asset["filename"]:
                error_message.append("The image size is not correct at row {0}".format(row + 1))
        return error_message

    def check_reader_asset(self):
        global image_folder_id
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
                print(excel_name)
                excel_data = xlrd.open_workbook(file_contents=x.read())
                break
        excel_table = excel_data.sheets()[0]
        nrows = excel_table.nrows
        last_page_number = 0
        for i in range(1, nrows):
            row_data = excel_table.row_values(i)
            self.check_book(self, row_data[0], row_data[9])
            page_number = row_data[3]
            folder_path = [row_data[0], row_data[2]]
            if page_number == '':
                continue
            if int(page_number) == 1:
                image_path = row_data[10]
                image_asset_lower = self.convert_asset_name(self, image_path.split('/')[-1])
                image_folder_id = self.get_folder_id(self, folder_path, all_folder)
                if not image_folder_id:
                    error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                    continue
                image_asset = self.get_asset(self, image_asset_lower, image_folder_id)
                image_name = image_root + image_path
                error_message.extend(self.reader_asset_check(self, image_asset, "Image", zip_file, image_name, i, image_path))
            elif page_number:
                if last_page_number != page_number:
                    image_path = row_data[4]
                    image_asset_lower = self.convert_asset_name(self, image_path.split('/')[-1])
                    if not image_folder_id:
                        error_message.append("The image path does not exist in the storyblok at row {0}".format(i + 1))
                        continue
                    image_asset = self.get_asset(self, image_asset_lower, image_folder_id)
                    image_name = image_root + image_path
                    error_message.extend(self.reader_asset_check(self, image_asset, "Image", zip_file, image_name, i, image_path))
                audio_path = row_data[7]
                audio_asset_lower = self.convert_asset_name(self, audio_path.split('/')[-1])
                audio_asset = self.get_asset(self, audio_asset_lower, image_folder_id)
                audio_name = image_root + audio_path
                error_message.extend(self.reader_asset_check(self, audio_asset, "Audio", zip_file, audio_name, i, audio_path))
                last_page_number = page_number

if __name__ == '__main__':
    test_type = "Vocab"
    test = StoryBlokImportCheckTool
    test.__init__(test)
    test.get_env(test)
    if test_type == "Reader":
        error_message = test.check_reader_asset(test)
    else:
        error_message = test.check_vocab_asset(test)
    if not error_message:
        print("No error")
    else:
        for error_message in error_message:
            print("Error %d"  %error_message.index(error_message) + ": "+error_message)
