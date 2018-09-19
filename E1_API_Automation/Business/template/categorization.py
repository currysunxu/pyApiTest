import jmespath
from functools import reduce

from E1_API_Automation.Business.template.base_text_template import BaseTextTemplate


class Categorization(BaseTextTemplate):
    def __init__(self, activity_json):
        self.json = activity_json

    def get_correct_answer(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers", question_json)
        anwser_match = [list(
            map(lambda x: {"id": x,
                           "text": jmespath.search("Body.options[?id=='{0}'].text".format(x), question_json)[0]},
                answer_option)) for answer_option in answer_ids]

        return anwser_match

    def get_question_score(self, question_key):
        question_json = jmespath.search("Questions[?Key=='{0}']".format(question_key), self.json)[0]
        answer_ids = jmespath.search("Body.answers", question_json)
        total_score = reduce(lambda x, y: len(x) + len(y), answer_ids)
        return total_score


act_json = {
    "Stimulus": [
        {
            "Key": "8cdc0e81-b350-4af8-a12c-1e9c316223cc",
            "ContentKey": None,
            "Body": {
                "item": {
                    "text": "<p>This is a test:</p>\n<p>fruit: apple , grape</p>\n<p>animal: cat , dog</p>"
                }
            },
            "Tags": [],
            "Type": None
        }
    ],
    "Questions": [
        {
            "Key": "b16fd07b-3158-4038-932c-4cd51737d1a4",
            "ContentKey": None,
            "Body": {
                "version": 1,
                "tests": [
                    {
                        "text": "Fruit"
                    },
                    {
                        "text": "Animal"
                    }
                ],
                "answers": [
                    [
                        "0",
                        "1"
                    ],
                    [
                        "2",
                        "3"
                    ]
                ],
                "options": [
                    {
                        "id": "0",
                        "text": "Apple"
                    },
                    {
                        "id": "1",
                        "text": "Banana"
                    },
                    {
                        "id": "2",
                        "text": "Pig"
                    },
                    {
                        "id": "3",
                        "text": "Dog"
                    }
                ],
                "title": {},
                "tags": [
                    {
                        "CompassTags": [],
                        "SubSkillSet": "",
                        "Vocabulary": []
                    },
                    {
                        "CompassTags": [],
                        "SubSkillSet": "",
                        "Vocabulary": []
                    }
                ]
            },
            "Tags": [],
            "Type": None
        }
    ],
    "Title": "99",
    "IsDynamicallyOrganized": False,
    "Key": "cac7eaf6-041d-44a0-9a06-2499f1dc3bba",
    "ContentKey": None,
    "Body": {
        "mappings": [
            {
                "s": "8cdc0e81-b350-4af8-a12c-1e9c316223cc",
                "q": "b16fd07b-3158-4038-932c-4cd51737d1a4"
            }
        ],
        "instruction": {
            "texts": [
                {
                    "text": "g fnh rdf g"
                }
            ]
        },
        "tags": {
            "Key": "tb16/book-1/unit-2/activities/homework/categorization-99/tags",
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
    "Type": "categorization"
}

if __name__ == '__main__':
    activity = Categorization(act_json)
    answer = activity.get_correct_answer(activity.question_key_list[0])
    print(activity.get_question_score(activity.question_key_list[0]))
    print(answer)
