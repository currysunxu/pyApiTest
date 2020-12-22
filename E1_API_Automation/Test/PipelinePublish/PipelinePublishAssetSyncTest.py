import json
import os

from hamcrest import assert_that

from E1_API_Automation.Business.PipelinePublish.MediaService import MediaService
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils
from E1_API_Automation.Test_Data.PipelinePublishData import AEMData


class PipelinePublishAssetSyncCheck:
    def __init__(self, source_env, target_env):
        self.source_env = source_env
        self.target_env = target_env

    '''
    test the assets have been synced from source to target for a specific file
    '''

    def test_asset_sync(self, source_file):
        media_host_source = AEMData.CSEMediaService[self.source_env]['host']
        media_api_key_source = AEMData.CSEMediaService[self.source_env]['x-api-key']
        media_service_source = MediaService(media_host_source, media_api_key_source)

        media_host_target = AEMData.CSEMediaService[self.target_env]['host']
        media_api_key_target = AEMData.CSEMediaService[self.target_env]['x-api-key']
        media_service_target = MediaService(media_host_target, media_api_key_target)

        with open(source_file, 'r') as f:
            source_file_dict = json.load(f)

        url_list = []
        for key in source_file_dict.keys():
            value = source_file_dict[key]
            self.get_media_url(value, url_list)

        # remove the duplicate ones
        url_list = list(set(url_list))

        exit_url_list = []
        count = 0
        print('The total number of url need to be verified is:' + str(len(url_list)))
        for media_url in url_list:
            print('----Start verifing media_url:' + media_url)
            cn_response = media_service_source.get_media(media_url)
            assert_that(cn_response.status_code == 200)
            media_stg_cn_sha1 = CommonUtils.get_asset_sha1(cn_response.content)

            sg_response = media_service_target.get_media(media_url)
            assert_that(sg_response.status_code == 200)
            # if sg_response.status_code == 200:
            #     exit_url_list.append(media_url)

            media_stg_sg_sha1 = CommonUtils.get_asset_sha1(sg_response.content)

            assert_that(media_stg_cn_sha1 == media_stg_sg_sha1,
                        'url {0} not consistent between cn and sg'.format(media_url))
            count = count + 1
        print('---End of the verifing, the total number is:' + str(count))

        print('exit url list:' + str(exit_url_list))

    def get_media_url(self, source_value, url_list):
        if isinstance(source_value, list):
            for i in range(len(source_value)):
                source_list_item = source_value[i]
                self.get_media_url(source_list_item, url_list)
        elif isinstance(source_value, dict):
            if 'mimeType' in source_value.keys() and len(source_value['mimeType']) != 0:
                url_list.append(source_value['url'])

            for key in source_value.keys():
                self.get_media_url(source_value[key], url_list)


if __name__ == '__main__':
    source_env = 'QA'
    target_env = 'STG_SG'
    test = PipelinePublishAssetSyncCheck(source_env, target_env)
    path = os.getcwd()

    # put a source file under /Test_Data to validate, the source file was generated after pipeline publish, you can download from AWS
    source_file = path + '/../../Test_Data/hf35-qa-bookI-ru-2-1221.json'
    test.test_asset_sync(source_file)
