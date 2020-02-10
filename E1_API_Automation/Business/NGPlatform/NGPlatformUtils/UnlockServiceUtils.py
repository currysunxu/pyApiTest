import datetime
import json
import random
import string
import copy

from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningCommonUtils import LearningCommonUtils
from E1_API_Automation.Business.NGPlatform.UnlockSessionEntity import UnlockSessionLessonEntity, UnlockSessionEntity
from E1_API_Automation.Test_Data.UnlockServiceData import UnlockServiceData


class UnlockServiceUtils:
    @staticmethod
    def construct_session_entity(lesson_number):
        reservation_id = 'reservationIdTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        sequence_number = random.randint(1, 10)
        session_type = 'sessionTypeTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        group_id = 'groupIdTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        program = 'HFV3Plus'
        program_level = ''.join(random.sample('CDEFGH', 1))
        start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        replay_id = random.randint(50, 1000)

        lesson_entity_list = []
        for i in range(lesson_number):
            lesson = UnlockSessionLessonEntity(random.randint(1, 5), random.randint(1, 7))
            lesson_entity_list.append(lesson)

        unlock_session = UnlockSessionEntity(reservation_id, sequence_number, session_type, group_id, program,
                                             program_level)
        unlock_session.is_deleted = 'false'
        unlock_session.start_time = start_time
        unlock_session.end_time = end_time
        unlock_session.lessons = lesson_entity_list
        unlock_session.replay_id = replay_id
        return unlock_session

    @staticmethod
    def convert_session_lessons_to_str(unlock_session):
        session_lesson_dict_list = []
        for i in range(len(unlock_session.lessons)):
            session_lesson = unlock_session.lessons[i]
            session_lesson_dict = {}
            session_lesson_dict['UnitNumber'] = str(session_lesson.unit_number)
            session_lesson_dict['LessonNumber'] = str(session_lesson.lesson_number)
            session_lesson_dict_list.append(json.dumps(session_lesson_dict))

        session_lessons_str = '[' + (",".join(session_lesson_dict_list)) + ']'
        return session_lessons_str

    @staticmethod
    def get_session_session_member_format_kafka_msg(is_session, unlock_entity):
        if is_session:
            unlock_kafka_msg = copy.deepcopy(UnlockServiceData.session_content)
        else:
            unlock_kafka_msg = copy.deepcopy(UnlockServiceData.session_member_content)

        unformat_kafka_msg_payload = unlock_kafka_msg.get('payload').get('Content__c')

        if is_session:
            session_lessons_str = UnlockServiceUtils.convert_session_lessons_to_str(unlock_entity)
            format_kafka_msg_payload = ('{' + unformat_kafka_msg_payload + '}').format(unlock_entity,
                                                                                       session_lessons_str)
        else:
            format_kafka_msg_payload = ('{' + unformat_kafka_msg_payload + '}').format(unlock_entity)

        unlock_kafka_msg.get('payload')['Content__c'] = format_kafka_msg_payload
        unlock_kafka_msg.get('event')['replayId'] = unlock_entity.replay_id

        return unlock_kafka_msg

    @staticmethod
    def verify_session_entity_with_db(expected_entity_list, db_return_list, expected_is_unlocked=None):
        error_message = ''

        if len(db_return_list) != len(expected_entity_list):
            error_message = "result return from DB's size not as expected!"

        for i in range(len(db_return_list)):
            actual_db_session = db_return_list[i]
            expected_entity = expected_entity_list[i]
            for key in actual_db_session.keys():
                actual_value = actual_db_session[key]

                if key == '_id':
                    expected_field_value = expected_entity.reservation_id
                elif key == 'bookNumber':
                    expected_field_value = ord(expected_entity.course_level) - ord('C') + 1
                elif key == 'isUnlocked':
                    expected_field_value = expected_is_unlocked
                elif key == 'lessons':
                    expected_field_value = expected_entity.lessons
                elif key not in ('_id', 'bookNumber', 'isUnlocked', 'lessons'):
                    entity_class_name = expected_entity.__class__.__name__
                    lower_case_key = LearningCommonUtils.convert_name_from_camel_case_to_lower_case(key)
                    entity_private_field_name = '_' + entity_class_name + '__' + lower_case_key
                    expected_field_value = getattr(expected_entity, entity_private_field_name)

                is_value_same = False
                if 'Time' in key:
                    entity_time_format = '%Y-%m-%dT%H:%M:%SZ'
                    expected_time = datetime.datetime.strptime(str(expected_field_value), entity_time_format)
                    db_time_format = '%Y-%m-%d %H:%M:%S'
                    actual_time = datetime.datetime.strptime(str(actual_value), db_time_format)

                    if actual_time == expected_time:
                        is_value_same = True
                elif key == 'lessons':
                    error_message = error_message + \
                                    UnlockServiceUtils.verify_session_entity_with_db(expected_entity.lessons,
                                                                                     actual_db_session[key])
                elif key == 'isDeleted':
                    if str(actual_value).lower() == str(expected_field_value):
                        is_value_same = True
                else:
                    if str(actual_value) == str(expected_field_value):
                        is_value_same = True

                if key != 'lessons' and not is_value_same:
                    error_message = error_message + " key:" + key + "'s value in DB not as expected as what we constructed in entity." \
                                                                    "The actual value is:" + str(actual_value) \
                                    + ", but the expected value is:" + expected_field_value

        return error_message

    @staticmethod
    def get_expected_session_member_entity(db_session_member, expected_entity_list):
        for i in range(len(expected_entity_list)):
            expected_entity = expected_entity_list[i]
            if db_session_member['sessionId'] == expected_entity.session_id and db_session_member[
                'studentId'] == expected_entity.student_id:
                return expected_entity

    @staticmethod
    def get_actual_session_member_dict(db_return_list, expected_entity):
        for i in range(len(db_return_list)):
            actual_session_member = db_return_list[i]
            if actual_session_member['sessionId'] == expected_entity.session_id and actual_session_member[
                'studentId'] == expected_entity.student_id:
                return actual_session_member

    @staticmethod
    def verify_session_member_entity_with_db(expected_entity_list, db_return_list):
        error_message = ''

        if len(db_return_list) != len(expected_entity_list):
            error_message = "result return from DB's size not as expected!"

        for i in range(len(expected_entity_list)):
            expected_entity = expected_entity_list[i]
            actual_db_result = UnlockServiceUtils.get_actual_session_member_dict(db_return_list, expected_entity)
            if actual_db_result is None:
                error_message = error_message + "sessionId: {0.session_id}, studentId: {0.student_id} not been found in DB".format(
                    expected_entity)
            else:
                for key in actual_db_result.keys():
                    actual_value = actual_db_result[key]
                    if key in ('_id', 'modifiedAt'):
                        if actual_value is None:
                            error_message = error_message + " key:" + key + "'s value should not be null in DB!"
                        continue

                    entity_class_name = expected_entity.__class__.__name__
                    lower_case_key = LearningCommonUtils.convert_name_from_camel_case_to_lower_case(key)
                    entity_private_field_name = '_' + entity_class_name + '__' + lower_case_key
                    expected_field_value = getattr(expected_entity, entity_private_field_name)

                    is_value_same = False

                    if key == 'isRemoved':
                        if str(actual_value).lower() == str(expected_field_value):
                            is_value_same = True
                    else:
                        if str(actual_value) == str(expected_field_value):
                            is_value_same = True

                    if not is_value_same:
                        error_message = error_message + " key:" + key + "'s value in DB not as expected as what we constructed in entity." \
                                                                        "The actual value is:" + str(actual_value) \
                                        + ", but the expected value is:" + expected_field_value
        return error_message
