from E1_API_Automation.Lib.Moutai import Moutai


class ContentBuilderService:
	def __init__(self, host):
		self.host = host
		self.mou_tai = Moutai(host=self.host)

	def get_release_by_status(self, status='PROCESSED'):
		api_url = "/admin/api/v1/releases?status={0}".format(status)
		return self.mou_tai.get(api_url)
