import re
from tkinter.filedialog import askopenfilename
import zipfile
import xlrd


class StoryBlokImportUtils:

    @staticmethod
    def get_zip_file():
        zip_name = askopenfilename()
        if '.zip' not in zip_name:
            print("Not a zip file")
            exit()
        zip_file = zipfile.ZipFile(zip_name, 'r')
        return zip_file

    @staticmethod
    def convert_asset_name(asset_name):
        if len(asset_name.rsplit('.', 1)) == 2:
            asset_name = re.sub(r'\W', "-", asset_name.rsplit('.', 1)[0]).rstrip('-') + "." + asset_name.rsplit('.', 1)[
                1]
            new_asset_name = [""]
            for str in asset_name:
                if str != new_asset_name[-1] or str != '-':
                    new_asset_name.append(str)
            convert_name = ''.join(new_asset_name).lower()
            return convert_name
        return None

    @staticmethod
    def get_excel_file():
        excel_name = askopenfilename()
        excel_data = xlrd.open_workbook(excel_name)
        return excel_data.sheets()[0]

    @staticmethod
    def convert_slug_name(slug_name):
        slug_name = re.sub(r'\W', "-", slug_name).rstrip('-')
        new_asset_name = [""]
        for str in slug_name:
            if str != new_asset_name[-1] or str != '-':
                new_asset_name.append(str)
        convert_name = ''.join(new_asset_name).lower()
        return convert_name
