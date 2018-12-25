from E1_API_Automation.Business.template.base_template import BaseTemplate
from E1_API_Automation.Business.template.base_text_template import BaseTextTemplate
from E1_API_Automation.Business.template.categorization import Categorization
from E1_API_Automation.Business.template.gap_fill_image_and_long_text import GapFillImageAndLongText
from E1_API_Automation.Business.template.gap_fill_long_text import GapFillLongText
from E1_API_Automation.Business.template.gap_fill_short_text import GapFillShortText
from E1_API_Automation.Business.template.match_audio_to_image import MatchAudioToImage
from E1_API_Automation.Business.template.match_image_audio_to_text import MatchImageAudioToText
from E1_API_Automation.Business.template.match_image_to_image import MatchImageToImage
from E1_API_Automation.Business.template.match_text_to_text import MatchTextToText
from E1_API_Automation.Business.template.matching import Matching
from E1_API_Automation.Business.template.multiple_select_audio import MultipleSelectAudio
from E1_API_Automation.Business.template.multiple_select_audio_image import MultipleSelectAudioImage
from E1_API_Automation.Business.template.multiple_select_image import MultipleSelectImage
from E1_API_Automation.Business.template.multiple_select_long_text import MultipleSelectLongText
from E1_API_Automation.Business.template.multiple_select_long_text_Image import MultipleSelectLongTextImage
from E1_API_Automation.Business.template.multiple_select_tap import MultipleSelectTap
from E1_API_Automation.Business.template.table_audio_text import TableAudioText
from E1_API_Automation.Business.template.unscramble import Unscramble


class Activity:
    def create_activity(self, activity_json):
        base_activity = BaseTemplate(activity_json)
        if base_activity.activity_type == 'categorization':
            return Categorization(activity_json)
        elif base_activity.activity_type == 'gapFillImageAndLongText':
            return GapFillImageAndLongText(activity_json)
        elif base_activity.activity_type == 'gapFillLongText':
            return  GapFillLongText(activity_json)
        elif base_activity.activity_type == 'gapFillShortText':
            return GapFillShortText(activity_json)
        elif base_activity.activity_type == 'matchAudioToImage':
            return MatchAudioToImage(activity_json)
        elif base_activity.activity_type == 'matchImageAudioToText':
            return MatchImageAudioToText(activity_json)
        elif base_activity.activity_type == 'matchImageToImage':
            return MatchImageToImage(activity_json)
        elif base_activity.activity_type == 'matchTextToText':
            return MatchTextToText(activity_json)
        elif base_activity.activity_type == 'multipleSelectAudio':
            return MultipleSelectAudio(activity_json)
        elif base_activity.activity_type == 'multipleSelectImage':
            return MultipleSelectImage(activity_json)
        elif base_activity.activity_type == 'multipleSelectAudioImageResponse':
            return MultipleSelectAudioImage(activity_json)
        elif base_activity.activity_type == 'multipleSelectLongText':
            return MultipleSelectLongText(activity_json)
        elif base_activity.activity_type == 'multipleSelectLongTextImageResponse':
            return MultipleSelectLongTextImage(activity_json)
        elif base_activity.activity_type == 'tableAudioTextResponse':
            return TableAudioText(activity_json)
        elif base_activity.activity_type == 'unscramble':
            return Unscramble(activity_json)
        elif base_activity.activity_type == 'matching':
            return Matching(activity_json)
        elif base_activity.activity_type == 'multiple-select-tap':
            return MultipleSelectTap(activity_json)
        else:
            return BaseTextTemplate(activity_json)








