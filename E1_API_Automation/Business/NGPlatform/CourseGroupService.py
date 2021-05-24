from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils


class CourseGroupService(BaseService):

    def get_unlock_progress(self, student_id, book_content_id):
        api_url = '/api/v1/unlocked-progress?studentId={0}&bookContentId={1}'.format(student_id, book_content_id)
        return self.mou_tai.get(api_url)

    def get_current_unlock(self, student_id):
        api_url = '/api/v1/unlocked-progress/current?studentId={0}'.format(student_id)
        return self.mou_tai.get(api_url)

    def get_core_current_group(self, student_id):
        api_url = '/api/v2/students/{0}/groups/current-core-program-group'.format(student_id)
        return self.mou_tai.get(api_url)

    def put_unlock_practice(self, student_id, content_path, unlock_at=CommonUtils.datetime_format(), product=2):
        api_url = '/admin/api/v1/unlocked-progress'
        unlock_body = {
            "studentId": student_id,
            "product": product,
            "contentPath": content_path,
            "unlockedAt": unlock_at
        }
        return self.mou_tai.put(api_url, unlock_body)
