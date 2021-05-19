from E1_API_Automation.Lib.Moutai import Moutai


class AEMService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_aem_book(self, course, book):
        api_url = '/apps/adam/course.json/content/adam/courses/{0}/{1}'.format(course, book)
        if course == 'smallstars-35':
            api_url = '/apps/adam/flexible/course.json/content/adam/courses/{0}/{1}'.format(course, book)
        return self.mou_tai.get(api_url)
