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

act_json ={
      "Stimulus": [
        {
          "Key": "bac3c25a-f0ad-47d1-99a9-c3bbac72ee4b",
          "ContentKey": None,
          "Body": {
            "item": {
              "text": "How are you ？",
              "image": "resource://cb73bcc3-ba84-e811-80d8-0050569a01b3"
            }
          },
          "Tags": [],
          "Type": None
        }
      ],
      "Questions": [
        {
          "Key": "b9265e35-f4e6-4049-bd20-dd18a21c1c09",
          "ContentKey": None,
          "Body": {
            "version": 1,
            "tests": [
              {
                "text": "<p>The <span data-gap-value=\"whether\">whether</span> is warm.</p>"
              }
            ],
            "answers": [
              [
                "0"
              ]
            ],
            "options": [
              {
                "id": "0",
                "text": "whether"
              }
            ],
            "tags": [
              {
                "CompassTags": [],
                "SubSkillSet": "",
                "Vocabulary": []
              }
            ],
            "additionalLength": 0
          },
          "Tags": [],
          "Type": None
        }
      ],
      "Title": "Shirley_GapF 1: Image and Long Text",
      "IsDynamicallyOrganized": False,
      "Key": "d830c00f-a973-4dcc-8be5-9b05c54a9372",
      "ContentKey": None,
      "Body": {
        "mappings": [
          {
            "s": "bac3c25a-f0ad-47d1-99a9-c3bbac72ee4b",
            "q": "b9265e35-f4e6-4049-bd20-dd18a21c1c09"
          }
        ],
        "instruction": {
          "texts": [
            {
              "text": "Shirley_GapF 1: Image and Long Text : instruction"
            }
          ]
        },
        "tags": {
          "Key": "tb16/book-1/unit-1/activities/homework/gapfillimageandlongtext-shirley-gapf1-imageandlongtext/tags",
          "SkillType": "listening",
          "ageGroupL": 0,
          "ageGroupH": 0,
          "ActivityType": "",
          "ActivitySubType": "",
          "CefrLevels": [],
          "CompassTags": [],
          "SecondaryCompassTags": [],
          "TotalCompassTags": [],
          "LearningFocus": ""
        },
        "theme": {
          "BackGroundImages": [],
          "Summary": {
            "keepTrying": [
              "resource://b786aa3a-ed0e-4e3a-9b46-d40ceff0c760",
              "resource://e0da01fd-bcb8-45d8-aaae-698e9efba336"
            ],
            "notBad": [
              "resource://37b632de-dab8-4624-83b5-c3d3a78f97ca",
              "resource://7f001d17-b675-4f0f-a8e0-4fa322ada114"
            ],
            "excellent": [
              "resource://acf005f5-812a-4c6a-abea-3b08f2460043",
              "resource://55f05624-a9b4-4f87-b5c8-d155aecfa96e",
              "resource://04360d14-dcf7-4ee2-83e0-0b5407309a3f",
              "resource://5cae27dc-916b-4b2f-a871-265c0c3908e7"
            ],
            "goodJob": [
              "resource://8fa5429d-31ea-4639-ab82-add5b1b6e704",
              "resource://cd60097e-2dd4-41b6-a5c7-01776e95e0ce",
              "resource://b6b04082-375f-4a81-83d7-54f6c8b90f94",
              "resource://3ec9466a-a23e-4c9b-b64a-4a6225788525"
            ],
            "wellDone": [
              "resource://62e25fa4-40b0-450d-8e23-315b079daa05",
              "resource://727fb5d4-1768-43c2-8373-22121f57c248",
              "resource://5307db95-7b99-4e5b-a583-442c15c1f97c",
              "resource://26d5ae79-e4bd-4818-b6aa-cb0aa582bc23"
            ]
          },
          "IntroPage": {
            "audio": [
              "resource://e6dc5cb1-14c5-4a10-9816-dcce25b5ba7b"
            ],
            "nonAudio": [
              "resource://f31dcb2b-8d18-472b-a0c9-94fdea0c0a05"
            ]
          }
        }
      },
      "Tags": [],
      "Type": "gapFillImageAndLongText"
    }
if __name__ == '__main__':
    aa = Activity().create_activity(act_json)
    print(aa)



