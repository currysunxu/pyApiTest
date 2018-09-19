from E1_API_Automation.Business.template.base_template import BaseTemplate
from E1_API_Automation.Business.template.categorization import Categorization
from E1_API_Automation.Business.template.gap_fill_image_and_long_text import GapFillImageAndLongText
from E1_API_Automation.Business.template.gap_fill_long_text import GapFillLongText
from E1_API_Automation.Business.template.gap_fill_short_text import GapFillShortText
from E1_API_Automation.Business.template.match_audio_to_image import MatchAudioToImage
from E1_API_Automation.Business.template.match_image_audio_to_text import MatchImageAudioToText
from E1_API_Automation.Business.template.match_image_to_image import MatchImageToImage
from E1_API_Automation.Business.template.match_text_to_text import MatchTextToText
from E1_API_Automation.Business.template.multiple_select_audio import MultipleSelectAudio
from E1_API_Automation.Business.template.multiple_select_audio_image import MultipleSelectAudioImage
from E1_API_Automation.Business.template.multiple_select_image import MultipleSelectImage
from E1_API_Automation.Business.template.multiple_select_long_text import MultipleSelectLongText
from E1_API_Automation.Business.template.multiple_select_long_text_Image import MultipleSelectLongTextImage
from E1_API_Automation.Business.template.table_audio_text import TableAudioText
from E1_API_Automation.Business.template.unscramble import Unscramble


class Activity:
    def create_activity(self, activity_json):
        base_activity = BaseTemplate(activity_json)
        map_ = {
            'categorization': Categorization(activity_json),
            'gapFillImageAndLongText': GapFillImageAndLongText(activity_json),
            'gapFillLongText': GapFillLongText(activity_json),
            'gapFillShortText': GapFillShortText(activity_json),
            'matchAudioToImage': MatchAudioToImage(activity_json),
            'matchImageAudioToText': MatchImageAudioToText(activity_json),
            'matchImageToImage': MatchImageToImage(activity_json),
            'matchTextToText': MatchTextToText(activity_json),
            'multipleSelectAudio': MultipleSelectAudio(activity_json),
            'multipleSelectAudioImageResponse': MultipleSelectAudioImage(activity_json),
            'multipleSelectImage': MultipleSelectImage(activity_json),
            'multipleSelectLongText': MultipleSelectLongText(activity_json),
            'multipleSelectLongTextImageResponse': MultipleSelectLongTextImage(activity_json),
            'tableAudioTextResponse': TableAudioText(activity_json),
            'unscramble': Unscramble(activity_json)
        }
        return map_[base_activity.activity_type]



