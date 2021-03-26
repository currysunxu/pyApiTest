import hashlib
import json
import random
import string
import time
import urllib


class CommonUtils:
    @staticmethod
    def get_asset_sha1(asset_encode):
        s1 = hashlib.sha1()
        s1.update(asset_encode)
        return s1.hexdigest()

    '''
    encode url for specific string between //, 
    for example input: highflyers/cn-3-144/book, output: highflyers%2Fcn-3-144%2Fbook
    '''

    @staticmethod
    def encode_url_content_path(content_path):
        cn_content_path_list = content_path.split('/')
        cn_content_path = cn_content_path_list[1]
        encoded_cn = urllib.parse.quote('/' + cn_content_path + '/', safe="")
        encoded_content_path = cn_content_path_list[0] + encoded_cn + cn_content_path_list[2]
        return encoded_content_path

    @staticmethod
    def random_gen_str(length=8):
        return ''.join(random.sample(string.ascii_letters + string.digits, length))

    '''
    print or log formatted json string when debug
    '''

    @staticmethod
    def beautify_json(obj):
        formatted_json_str = json.dumps(obj, indent=4)
        print(formatted_json_str)

    '''
    formatted datetime yyyy-mm-ddTH:M:S.Z
    default localtime
    '''

    @staticmethod
    def datetime_format(date_time=time.localtime()):
        formatted_date_time = time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", date_time)
        return formatted_date_time

    '''
    randomly str from 1 to specific range
    '''
    @staticmethod
    def randomIntToString(range):
        return str(random.randint(1, range))

    @staticmethod
    def randomFloatToString(startIndex,endIndex):
        return format(random.uniform(startIndex, endIndex), '.2f')
