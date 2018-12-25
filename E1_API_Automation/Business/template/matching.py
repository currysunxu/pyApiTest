from E1_API_Automation.Business.template.base_audio_template import BaseAudioTemplate


class Matching(BaseAudioTemplate):
  def __init__(self, activity_json):
    self.json = activity_json

