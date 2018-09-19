

from E1_API_Automation.Business.template.base_image_template import BaseImageTemplate


class MatchImageToImage(BaseImageTemplate):
  def __init__(self, activity_json):
    self.json = activity_json
