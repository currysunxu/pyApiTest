from E1_API_Automation.Lib.Moutai import Moutai
from E1_API_Automation.Settings import env_key
from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData, StoryBlokVersion


class StoryBlokService:
    def __init__(self, host):
        self.host = host
        headers = {"Content-Type": "application/json",
                   "Authorization": "9aF9jhvq4wbD2bM0xWbjcwtt-110-gNsaz2QyH_zhAsmzPhz_"}
        self.mou_tai = Moutai(host=self.host, headers=headers)

    def get_storyblok_stories(self, starts_with, page_number=1, page_size=25, published_at_start='',
                              published_at_end=''):
        api_token = StoryBlokData.StoryBlokAPIKey[env_key]
        # api_version = StoryBlokUtils.get_storyblok_version_by_env()
        api_version = StoryBlokVersion.PUBLISHED.value
        api_url = "/v1/cdn/stories?token={0}&starts_with={1}&version={2}&sort_by=id&page={3}&per_page={4}&published_at_gt={5}&published_at_lt={6}".format(
            api_token, starts_with, api_version, page_number, page_size, published_at_start, published_at_end)
        return self.mou_tai.get(api_url)

    def get_storyblok_readers(self, page_number=1, page_size=25, published_at_start='', published_at_end=''):
        return self.get_storyblok_stories('readers/content', page_number, page_size, published_at_start,
                                          published_at_end)

    def get_storyblok_reader_levels(self):
        api_token = StoryBlokData.StoryBlokAPIKey[env_key]
        api_version = StoryBlokVersion.PUBLISHED.value
        api_url = "/v1/cdn/stories?token={0}&starts_with=readers/course-config&version={1}&resolve_relations=parent&filter_query[component][in]=reader_level&sort_by=content.code&page=1&per_page=100".format(
            api_token, api_version)
        return self.mou_tai.get(api_url)

    def get_storyblok_vocabs(self, page_number=1, page_size=25, published_at_start='', published_at_end=''):
        return self.get_storyblok_stories('vocabularies', page_number, page_size, published_at_start, published_at_end)

    def get_storyblok_book_by_scope(self, book_release_scope):
        api_token = StoryBlokData.StoryBlokAPIKey[env_key]
        api_version = StoryBlokVersion.PUBLISHED.value
        api_url = "/v1/cdn/stories?token={0}&starts_with=highflyers/course-config/{1}&filter_query[component][in]=book&version={2}".format(
            api_token, book_release_scope, api_version)
        return self.mou_tai.get(api_url)

    def get_storyblok_configs(self, book_release_scope, filter_component):
        api_token = StoryBlokData.StoryBlokAPIKey[env_key]
        api_version = StoryBlokVersion.PUBLISHED.value
        api_url = "/v1/cdn/stories?token={0}&starts_with=highflyers/course-config/{1}&version={2}&resolve_relations=parent&filter_query[component][in]={3}".format(
            api_token, book_release_scope, api_version, filter_component)
        return self.mou_tai.get(api_url)

    def get_storyblok_reader_configs(self, book_release_scope):
        return self.get_storyblok_configs(book_release_scope, 'reader_config')

    def get_storyblok_vocab_configs(self, book_release_scope):
        return self.get_storyblok_configs(book_release_scope, 'vocab_config')

    def get_all_asset_folder(self):
        api_url = "/v1/spaces/187/asset_folders/"
        return self.mou_tai.get(api_url)

    def get_asset(self, asset_name):
        api_url = "/v1/spaces/187/assets?search={0}".format(asset_name)
        return self.mou_tai.get(api_url)
