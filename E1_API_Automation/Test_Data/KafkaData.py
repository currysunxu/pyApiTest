import random
import time

from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils


class KafkaData:
    BOOTSTRAP_SERVERS = {
        'QA': "10.179.243.71:9092",
        'Staging': "10.179.243.78:9092"
    }

    @staticmethod
    def build_online_homework_unlock_message_by_content_path(content_path):
        online_homework_unlock_message = {
            "StudentId": str(random.randint(9000, 90000)),
            "ContentPath": content_path,
            "GroupId": str(random.randint(1, 90000)),
            "UnlockAt": time.strftime("%Y-%m-%dT%H:%M:%S.%j", time.localtime())
        }
        return online_homework_unlock_message

    @staticmethod
    def build_omni_sessions_message(group_type,product):
        omni_sessions_message = {
            "payload": {
                "Content__c": {
                    "timestamp": "2020-12-06T07:55:41.298Z",
                    "teacherName": "Ciara Brian",
                    "teacherId": "a5R2x000000PEImEAO",
                    "teacherAvatarUrl": "https://cn-prod-salesforce-integration-1258166938.cos.ap-shanghai.myqcloud.com/B25__Staff__c/teacher_upload/68d19e30-062d-4add-934b-b4a881462f75/1c384317-9b1b-4f9d-bf8a-84943c94fe9d.jpeg",
                    "teacherAccent": "British",
                    "studentpwd": None,
                    "startTime": time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", time.localtime()),
                    "skillFocus": None,
                    "sessionType": "Online Classroom",
                    "sessionStatus": "Activated",
                    "sessionId": "124356330",
                    "sequenceNumber": 17,
                    "season": None,
                    "roomId": None,
                    "reservationId": CommonUtils.random_gen_str(),
                    "programLevel": "2",
                    "program": product,
                    "pdDesignation": None,
                    "offlineSessionId": None,
                    "lessons": [
                        {
                            "UnitNumber": "6",
                            "OnlineLessonTopicId": "10301",
                            "OnlineLessonTopic": "Tom's Toys Lesson 1",
                            "LessonNumber": "1",
                            "ContentPath": None
                        },
                        {
                            "UnitNumber": "6",
                            "OnlineLessonTopicId": None,
                            "OnlineLessonTopic": None,
                            "LessonNumber": "1",
                            "ContentPath": None
                        }
                    ],
                    "isRemoved": False,
                    "groupType": group_type,
                    "groupNumber": None,
                    "groupId": "a0B2x000000fWZeEAM",
                    "evcToken": None,
                    "entryLink": "https://global.talk-cloud.net/WebAPI/entry/domain/ef/serial/null/pid/38283472/username/huang_Leo/usertype/2/ts/1607241341/auth/1c9024af019d13cdeb385aa844d7a71e",
                    "endTime": "2021-04-20T10:30:00.000Z",
                    "customerId": str(random.randint(9000, 90000)),
                    "centerCode": "DCNSZX16",
                    "businessUnit": "China Own",
                    "attendanceStatus": "Pending",
                    "attendanceResult": None
                }
            }
        }
        return omni_sessions_message
