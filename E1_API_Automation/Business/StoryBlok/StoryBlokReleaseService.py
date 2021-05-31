from E1_API_Automation.Business.BaseService import BaseService


class StoryBlokReleaseService(BaseService):

    def get_storyblok_release_history(self, release_type=None):
        if release_type is None:
            release_type = ''
        api_url = "/admin/api/v1/releases?program={0}".format(release_type)
        return self.mou_tai.get(api_url)