import hashlib
import json
import random
import string
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
    def random_gen_str():
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))

    '''
    print or log formatted json string when debug
    '''
    @staticmethod
    def beautify_json(obj):
        formatted_json_str = json.dumps(obj,indent=4)
        print(formatted_json_str)