import json
import string
import random

from kafka import KafkaProducer
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.UnlockServiceUtils import UnlockServiceUtils
from E1_API_Automation.Business.NGPlatform.UnlockSessionEntity import UnlockSessionLessonEntity
from E1_API_Automation.Test_Data.UnlockServiceData import UnlockServiceData, UnlockKafkaServer
from E1_API_Automation.Business.NGPlatform.UnlockSessionMemberEntity import UnlockSessionMemberEntity
from E1_API_Automation.Lib.db_mongo import MongoHelper
from E1_API_Automation.Settings import MONGO_DATABASE
from E1_API_Automation.Settings import env_key

from hamcrest import assert_that


@TestClass()
class UnlockServiceTestCases:
    # test session and session member message process
    def test_session_session_member_kafka_valid_message_process(self, session_lesson_number, session_member_number):
        session_topic_name = UnlockServiceData.session_topic_name
        session_member_topic_name = UnlockServiceData.session_member_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]

        unlock_session = UnlockServiceUtils.construct_session_entity(session_lesson_number)
        session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)

        producer = KafkaProducer(bootstrap_servers=kafka_broker)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())

        # send session member message
        session_member_entity_list = []
        for i in range(session_member_number):
            student_id = random.randint(1, 1000)
            session_member = UnlockSessionMemberEntity(unlock_session.reservation_id, student_id, 'false', unlock_session.replay_id)
            session_member_entity_list.append(session_member)
            session_member_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member)
            producer.send(topic=session_member_topic_name, value=json.dumps(session_member_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        find_condition = {"_id": unlock_session.reservation_id}
        # check session db record
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
        error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list)
        assert_that(error_message == '', error_message)
        # check session member db record
        find_condition = {"sessionId": unlock_session.reservation_id}
        session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members', find_condition)
        error_message = UnlockServiceUtils.verify_session_member_entity_with_db(session_member_entity_list, session_member_db_dict_list)
        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_session_with_one_lesson_one_session_member_kafka_message_process(self):
        self.test_session_session_member_kafka_valid_message_process(1, 1)

    @Test(tags="qa")
    def test_session_with_multiple_lesson_multiple_session_member_kafka_message_process(self):
        self.test_session_session_member_kafka_valid_message_process(random.randint(2, 6), random.randint(2, 8))

    def test_session_fields_update_with_different_replayid(self, is_replayid_greater):
        session_topic_name = UnlockServiceData.session_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]

        unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
        session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)

        producer = KafkaProducer(bootstrap_servers=kafka_broker)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        find_condition = {"_id": unlock_session.reservation_id}
        # check session db record
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
        error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list)
        assert_that(error_message == '', error_message)

        # construct another session, with same reservation id, greater/lesser replay id
        if is_replayid_greater:
            replay_id_update = unlock_session.replay_id + 1
        else:
            replay_id_update = unlock_session.replay_id - 1

        unlock_session_diff_replayid = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
        unlock_session_diff_replayid.reservation_id = unlock_session.reservation_id
        unlock_session_diff_replayid.replay_id = replay_id_update
        session_kafka_msg_less_replayid = \
            UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session_diff_replayid)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg_less_replayid).encode())

        # get the db data, to check if the fields will be updated or not
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)

        # when replayid is greater, session fields will be updated, otherwise, they will not be updated
        if is_replayid_greater:
            expected_session_entity = unlock_session_diff_replayid
        else:
            expected_session_entity = unlock_session

        error_message = UnlockServiceUtils.verify_session_entity_with_db([expected_session_entity], session_db_dict_list)
        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_session_kafka_valid_message_same_sessionid_greater_replayid(self):
        self.test_session_fields_update_with_different_replayid(True)

    @Test(tags="qa")
    def test_session_kafka_valid_message_same_sessionid_lesser_replayid(self):
        self.test_session_fields_update_with_different_replayid(False)

    def test_session_member_fields_update_with_different_replayid(self, is_replayid_greater):
        session_member_topic_name = UnlockServiceData.session_member_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
        producer = KafkaProducer(bootstrap_servers=kafka_broker)

        session_id = 'sessionIdTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        student_id = random.randint(1, 1000)
        replay_id = random.randint(50, 1000)
        session_member = UnlockSessionMemberEntity(session_id, student_id, 'false', replay_id)
        session_member_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member)
        producer.send(topic=session_member_topic_name, value=json.dumps(session_member_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        # check session member db record
        find_condition = {"sessionId": session_id}
        session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members',
                                                                                   find_condition)
        error_message = \
            UnlockServiceUtils.verify_session_member_entity_with_db([session_member], session_member_db_dict_list)
        assert_that(error_message == '', error_message)

        # construct another session member, with same session id, student id, greater/lesser replay id
        if is_replayid_greater:
            replay_id_update = replay_id + 1
        else:
            replay_id_update = replay_id - 1
        session_member_diff_replayid = UnlockSessionMemberEntity(session_id, student_id, 'true', replay_id_update)
        session_member_kafka_msg_less_replayid = \
            UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member_diff_replayid)
        # send session message
        producer.send(topic=session_member_topic_name,
                      value=json.dumps(session_member_kafka_msg_less_replayid).encode())
        # get the db data, to check if the field will be updated or not
        session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members',
                                                                                   find_condition)

        # when replayid is greater, session_member fields will be updated, otherwise, they will not be updated
        if is_replayid_greater:
            expected_session_member = session_member_diff_replayid
        else:
            expected_session_member = session_member
        error_message = \
            UnlockServiceUtils.verify_session_member_entity_with_db([expected_session_member], session_member_db_dict_list)
        assert_that(error_message == '', error_message)

    @Test(tags="qa")
    def test_session_member_kafka_valid_message_same_sessionid_studentid_greater_replayid(self):
        self.test_session_member_fields_update_with_different_replayid(True)

    @Test(tags="qa")
    def test_session_member_kafka_valid_message_same_sessionid_studentid_lesser_replayid(self):
        self.test_session_member_fields_update_with_different_replayid(False)

    # if the session already been processed, that is, the isUnlock is true,
    # then, even when the replayid is greater than the previous one, the session record will not be updated
    @Test(tags="qa")
    def test_if_processed_session_fields_not_updated_with_greater_replayid(self):
        session_topic_name = UnlockServiceData.session_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]

        unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
        session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)

        producer = KafkaProducer(bootstrap_servers=kafka_broker)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        find_condition = {"_id": unlock_session.reservation_id}
        # check session db record
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
        error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list)
        assert_that(error_message == '', error_message)

        update_is_unlock = {'isUnlocked': True}
        mongo_sql_server.exec_update('offline_sessions', find_condition, update_is_unlock)

        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
        assert_that(session_db_dict_list[0]['isUnlocked']==True)

        # prepare another session with same session id, and greater replay id
        unlock_session_diff_replayid = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
        unlock_session_diff_replayid.reservation_id = unlock_session.reservation_id
        unlock_session_diff_replayid.replay_id = unlock_session.replay_id + 1
        session_kafka_msg_less_replayid = \
            UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session_diff_replayid)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg_less_replayid).encode())

        # get the db data, to check if the fields will be updated or not
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)

        # session will not be updated, as the session record have been processed
        error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list, True)
        assert_that(error_message == '', error_message)

    # if the session type is CLASSROOM, the kafka message will not be processed
    @Test(tags="qa")
    def test_classroom_type_session_kafka_msg_will_not_be_processed(self):
        session_topic_name = UnlockServiceData.session_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]

        unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
        unlock_session.type = 'CLASSROOM'
        session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)

        producer = KafkaProducer(bootstrap_servers=kafka_broker)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        find_condition = {"_id": unlock_session.reservation_id}
        # check session db record
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
        assert_that(len(session_db_dict_list) == 0)

    @Test(tags="qa")
    def test_invalid_session_kafka_msg_will_not_be_processed(self):
        session_topic_name = UnlockServiceData.session_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]

        # make lesson's unit_name, lesson_number with non-int value
        unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(1, 3))

        invalid_lesson = UnlockSessionLessonEntity(''.join(random.sample(string.ascii_letters, 10)), ''.join(random.sample(string.ascii_letters, 10)))
        unlock_session.lessons.append(invalid_lesson)

        session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)

        producer = KafkaProducer(bootstrap_servers=kafka_broker)
        # send session message
        producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        find_condition = {"_id": unlock_session.reservation_id}
        # check session db record
        session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
        assert_that(len(session_db_dict_list) == 0)

    @Test(tags="qa")
    def test_invalid_session_member_kafka_msg_will_not_be_processed(self):
        session_member_topic_name = UnlockServiceData.session_member_topic_name
        kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
        producer = KafkaProducer(bootstrap_servers=kafka_broker)

        session_id = 'sessionIdTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        student_id = 'invalidStudentId_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        replay_id = 'invalidReplayId_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
        session_member = UnlockSessionMemberEntity(session_id, student_id, 'false', replay_id)
        session_member_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member)
        producer.send(topic=session_member_topic_name, value=json.dumps(session_member_kafka_msg).encode())

        # verify db data with expected entity
        mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
        # check session member db record
        find_condition = {"sessionId": session_id}
        session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members',
                                                                                   find_condition)
        assert_that(len(session_member_db_dict_list) == 0)
