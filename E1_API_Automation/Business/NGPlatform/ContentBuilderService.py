from E1_API_Automation.Business.BaseService import BaseService


class ContentBuilderService(BaseService):

	def get_release_by_status(self, status='PROCESSED'):
		api_url = "/admin/api/v1/releases?status={0}".format(status)
		return self.mou_tai.get(api_url)
