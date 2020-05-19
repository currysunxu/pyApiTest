
from E1_API_Automation.Lib.Moutai import Moutai


class CourseGroupService:
	def __init__(self, host):
		self.host = host
		self.mou_tai = Moutai(host=self.host, headers={"Content-Type": "application/json;charset=UTF-8"})

	def get_unlock_progress(self, student_id, book_content_id):
		api_url = '/api/v1/unlocked-progress?studentId={0}&bookContentId={1}'.format(student_id, book_content_id)
		return self.mou_tai.get(api_url)
