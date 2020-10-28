from E1_API_Automation.Lib.Moutai import Moutai


class StoryBlokReleaseService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_storyblok_release_history(self, release_type):
        api_url = "/admin/api/v1/releases?program={0}".format(release_type)
        return self.mou_tai.get(api_url)