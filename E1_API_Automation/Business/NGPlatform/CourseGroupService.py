from E1_API_Automation.Business.BaseService import BaseService


class CourseGroupService(BaseService):

	def get_unlock_progress(self, student_id, book_content_id):
		api_url = '/api/v1/unlocked-progress?studentId={0}&bookContentId={1}'.format(student_id, book_content_id)
		return self.mou_tai.get(api_url)

	def get_current_unlock(self, student_id):
		api_url = '/api/v1/unlocked-progress/current?studentId={0}'.format(student_id)
		return self.mou_tai.get(api_url)

	def get_core_current_group(self,student_id):
		api_url = '/api/v2/students/{0}/groups/current-core-program-group'.format(student_id)
		return self.mou_tai.get(api_url)
