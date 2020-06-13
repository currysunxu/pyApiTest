import json
import string
import random

from kafka import KafkaProducer, KafkaConsumer
from ptest.decorator import TestClass, Test
import time

# from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.UnlockServiceUtils import UnlockServiceUtils
# from E1_API_Automation.Business.NGPlatform.UnlockSessionEntity import UnlockSessionLessonEntity
# from E1_API_Automation.Test_Data.UnlockServiceData import UnlockServiceData, UnlockKafkaServer
# from E1_API_Automation.Business.NGPlatform.UnlockSessionMemberEntity import UnlockSessionMemberEntity
# from E1_API_Automation.Lib.db_mongo import MongoHelper
# from E1_API_Automation.Settings import MONGO_DATABASE
# from E1_API_Automation.Settings import env_key
#
# from hamcrest import assert_that


@TestClass()
class UnlockServiceTestCases:
    # test session and session member message process
    # def test_session_session_member_kafka_valid_message_process(self, session_lesson_number, session_member_number):
    #     session_topic_name = UnlockServiceData.session_topic_name
    #     session_member_topic_name = UnlockServiceData.session_member_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #
    #     unlock_session = UnlockServiceUtils.construct_session_entity(session_lesson_number)
    #     session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)
    #
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())
    #
    #     # send session member message
    #     session_member_entity_list = []
    #     for i in range(session_member_number):
    #         student_id = random.randint(1, 1000)
    #         session_member = UnlockSessionMemberEntity(unlock_session.reservation_id, student_id, 'false', unlock_session.replay_id)
    #         session_member_entity_list.append(session_member)
    #         session_member_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member)
    #         producer.send(topic=session_member_topic_name, value=json.dumps(session_member_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     find_condition = {"_id": unlock_session.reservation_id}
    #     # check session db record
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #     # check session member db record
    #     find_condition = {"sessionId": unlock_session.reservation_id}
    #     session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members', find_condition)
    #     error_message = UnlockServiceUtils.verify_session_member_entity_with_db(session_member_entity_list, session_member_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #
    # @Test(tags="qa")
    # def test_session_with_one_lesson_one_session_member_kafka_message_process(self):
    #     self.test_session_session_member_kafka_valid_message_process(1, 1)
    #
    # @Test(tags="qa")
    # def test_session_with_multiple_lesson_multiple_session_member_kafka_message_process(self):
    #     self.test_session_session_member_kafka_valid_message_process(random.randint(2, 6), random.randint(2, 8))
    #
    # def test_session_fields_update_with_different_replayid(self, is_replayid_greater):
    #     session_topic_name = UnlockServiceData.session_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #
    #     unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
    #     session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)
    #
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     find_condition = {"_id": unlock_session.reservation_id}
    #     # check session db record
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #
    #     # construct another session, with same reservation id, greater/lesser replay id
    #     if is_replayid_greater:
    #         replay_id_update = unlock_session.replay_id + 1
    #     else:
    #         replay_id_update = unlock_session.replay_id - 1
    #
    #     unlock_session_diff_replayid = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
    #     unlock_session_diff_replayid.reservation_id = unlock_session.reservation_id
    #     unlock_session_diff_replayid.replay_id = replay_id_update
    #     session_kafka_msg_less_replayid = \
    #         UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session_diff_replayid)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg_less_replayid).encode())
    #
    #     # get the db data, to check if the fields will be updated or not
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #
    #     # when replayid is greater, session fields will be updated, otherwise, they will not be updated
    #     if is_replayid_greater:
    #         expected_session_entity = unlock_session_diff_replayid
    #     else:
    #         expected_session_entity = unlock_session
    #
    #     error_message = UnlockServiceUtils.verify_session_entity_with_db([expected_session_entity], session_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #
    # @Test(tags="qa")
    # def test_session_kafka_valid_message_same_sessionid_greater_replayid(self):
    #     self.test_session_fields_update_with_different_replayid(True)
    #
    # @Test(tags="qa")
    # def test_session_kafka_valid_message_same_sessionid_lesser_replayid(self):
    #     self.test_session_fields_update_with_different_replayid(False)
    #
    # def test_session_member_fields_update_with_different_replayid(self, is_replayid_greater):
    #     session_member_topic_name = UnlockServiceData.session_member_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #
    #     session_id = 'sessionIdTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
    #     student_id = random.randint(1, 1000)
    #     replay_id = random.randint(50, 1000)
    #     session_member = UnlockSessionMemberEntity(session_id, student_id, 'false', replay_id)
    #     session_member_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member)
    #     producer.send(topic=session_member_topic_name, value=json.dumps(session_member_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     # check session member db record
    #     find_condition = {"sessionId": session_id}
    #     session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members',
    #                                                                                find_condition)
    #     error_message = \
    #         UnlockServiceUtils.verify_session_member_entity_with_db([session_member], session_member_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #
    #     # construct another session member, with same session id, student id, greater/lesser replay id
    #     if is_replayid_greater:
    #         replay_id_update = replay_id + 1
    #     else:
    #         replay_id_update = replay_id - 1
    #     session_member_diff_replayid = UnlockSessionMemberEntity(session_id, student_id, 'true', replay_id_update)
    #     session_member_kafka_msg_less_replayid = \
    #         UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member_diff_replayid)
    #     # send session message
    #     producer.send(topic=session_member_topic_name,
    #                   value=json.dumps(session_member_kafka_msg_less_replayid).encode())
    #     # get the db data, to check if the field will be updated or not
    #     session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members',
    #                                                                                find_condition)
    #
    #     # when replayid is greater, session_member fields will be updated, otherwise, they will not be updated
    #     if is_replayid_greater:
    #         expected_session_member = session_member_diff_replayid
    #     else:
    #         expected_session_member = session_member
    #     error_message = \
    #         UnlockServiceUtils.verify_session_member_entity_with_db([expected_session_member], session_member_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #
    # @Test(tags="qa")
    # def test_session_member_kafka_valid_message_same_sessionid_studentid_greater_replayid(self):
    #     self.test_session_member_fields_update_with_different_replayid(True)
    #
    # @Test(tags="qa")
    # def test_session_member_kafka_valid_message_same_sessionid_studentid_lesser_replayid(self):
    #     self.test_session_member_fields_update_with_different_replayid(False)
    #
    # # if the session already been processed, that is, the isUnlock is true,
    # # then, even when the replayid is greater than the previous one, the session record will not be updated
    # @Test(tags="qa")
    # def test_if_processed_session_fields_not_updated_with_greater_replayid(self):
    #     session_topic_name = UnlockServiceData.session_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #
    #     unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
    #     session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)
    #
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     find_condition = {"_id": unlock_session.reservation_id}
    #     # check session db record
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list)
    #     assert_that(error_message == '', error_message)
    #
    #     update_is_unlock = {'isUnlocked': True}
    #     mongo_sql_server.exec_update('offline_sessions', find_condition, update_is_unlock)
    #
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     assert_that(session_db_dict_list[0]['isUnlocked']==True)
    #
    #     # prepare another session with same session id, and greater replay id
    #     unlock_session_diff_replayid = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
    #     unlock_session_diff_replayid.reservation_id = unlock_session.reservation_id
    #     unlock_session_diff_replayid.replay_id = unlock_session.replay_id + 1
    #     session_kafka_msg_less_replayid = \
    #         UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session_diff_replayid)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg_less_replayid).encode())
    #
    #     # get the db data, to check if the fields will be updated or not
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #
    #     # session will not be updated, as the session record have been processed
    #     error_message = UnlockServiceUtils.verify_session_entity_with_db([unlock_session], session_db_dict_list, True)
    #     assert_that(error_message == '', error_message)
    #
    # # if the session type is CLASSROOM, the kafka message will not be processed
    # @Test(tags="qa")
    # def test_classroom_type_session_kafka_msg_will_not_be_processed(self):
    #     session_topic_name = UnlockServiceData.session_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #
    #     unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
    #     unlock_session.type = 'CLASSROOM'
    #     session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)
    #
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     find_condition = {"_id": unlock_session.reservation_id}
    #     # check session db record
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     assert_that(len(session_db_dict_list) == 0)
    #
    # # if the course is not HFV3Plus, the kafka message will not be processed
    # @Test(tags="qa")
    # def test_invalid_program_session_kafka_msg_will_not_be_processed(self):
    #     session_topic_name = UnlockServiceData.session_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #
    #     unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(2, 6))
    #     unlock_session.course = 'HFV3Plus_Test'
    #     session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)
    #
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     find_condition = {"_id": unlock_session.reservation_id}
    #     # check session db record
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     assert_that(len(session_db_dict_list) == 0)
    #
    # @Test(tags="qa")
    # def test_invalid_session_kafka_msg_will_not_be_processed(self):
    #     session_topic_name = UnlockServiceData.session_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #
    #     # make lesson's unit_name, lesson_number with non-int value
    #     unlock_session = UnlockServiceUtils.construct_session_entity(random.randint(1, 3))
    #
    #     invalid_lesson = UnlockSessionLessonEntity(''.join(random.sample(string.ascii_letters, 10)), ''.join(random.sample(string.ascii_letters, 10)))
    #     unlock_session.lessons.append(invalid_lesson)
    #
    #     session_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(True, unlock_session)
    #
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #     # send session message
    #     producer.send(topic=session_topic_name, value=json.dumps(session_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     find_condition = {"_id": unlock_session.reservation_id}
    #     # check session db record
    #     session_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_sessions', find_condition)
    #     assert_that(len(session_db_dict_list) == 0)
    #
    # @Test(tags="qa")
    # def test_invalid_session_member_kafka_msg_will_not_be_processed(self):
    #     session_member_topic_name = UnlockServiceData.session_member_topic_name
    #     kafka_broker = UnlockKafkaServer.kafka_broker[env_key]
    #     producer = KafkaProducer(bootstrap_servers=kafka_broker)
    #
    #     session_id = 'sessionIdTest_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
    #     student_id = 'invalidStudentId_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
    #     replay_id = 'invalidReplayId_' + ''.join(random.sample(string.ascii_letters + string.digits, 10))
    #     session_member = UnlockSessionMemberEntity(session_id, student_id, 'false', replay_id)
    #     session_member_kafka_msg = UnlockServiceUtils.get_session_session_member_format_kafka_msg(False, session_member)
    #     producer.send(topic=session_member_topic_name, value=json.dumps(session_member_kafka_msg).encode())
    #
    #     # verify db data with expected entity
    #     mongo_sql_server = MongoHelper(MONGO_DATABASE, 'homework_qa')
    #     # check session member db record
    #     find_condition = {"sessionId": session_id}
    #     session_member_db_dict_list = mongo_sql_server.exec_query_return_dict_list('offline_session_members',
    #                                                                                find_condition)
    #     assert_that(len(session_member_db_dict_list) == 0)

    @Test(tags="qa")
    def test_kafka_consumer(self):
        topic_name = 'learningresult'
        # topic_name_learner_vector_qa = 'qa_learnerprofile_learner_vector'
        # topic_name_learner_vector_stg = 'stg_learnerprofile_learner_vector'
        # topic_name_learner_vector_live = 'prd_learnerprofile_learner_vector'
        # kafka_broker_qa = '10.179.243.69:9092'
        # kafka_broker_stg = '10.179.243.80:9092'
        kafka_broker_live = '10.179.166.144:9092'
        consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker_live, auto_offset_reset='earliest',
                                 group_id='connietest109')
        i = 0
        for message in consumer:
            i = i + 1
            print("the {0} message is: ".format(i))
            print(message)

    @Test(tags="qa")
    def test_unlock_info_kafka_message_process(self):
        # unlock_info_topic_name = 'omni-unlock-info-topic'
        session_topic_name = 'OMNI-OfflineCourse'
        session_member_topic_name = 'OMNI-SessionMember'
        kafka_broker = ['10.179.243.69:9092']
        # unlockinfo_kafka_msg = {"StudentId": 112, "ContentPath": "highflyers/cn-3/book-7/unit-1/assignment-1",
        #                         "GroupId": "test_group_id", "UnlockAt": "2020-04-19T13:05:21.759342Z"}
        # session_kafka_msg = {"schema": "uc4M56Qn8cIMHUTHUaFuag", "event": {"replayId": 12521409},"payload": {"CreatedById": "00528000007LU4EAAW", "CreatedDate": "2020-04-17T09:41:30Z", "Content__c": "{\"ReservationID\":\"a0G2x000000urVdEAITest0609-05\", \"OfflineReservationID\":\"a0G2x000000olCuEAI-test05\",\"StartTime\":\"2020-04-25T04:30:00Z\", \"EndTime\":\"2020-04-25T06:00:00Z\",\"SessionType\":\"Online Class\",\"SequenceNumber\":1,\"ProgramLevel\":\"D\",\"Program\":\"HFV3Plus\",\"Lessons\":[{\"UnitNumber\":\"1\",\"OnlineLessonTopicId\":\"10286\",\"OnlineLessonTopic\":\"Welcome Home! Lesson 2\",\"LessonNumber\":\"2\"}],\"IsDeleted\":false,\"GroupID\":\"a0B2x00000053OkEAI\",\"CenterCode\":\"SZA\",\"TeacherName\":\"Melody Lee\",\"RoomNumber\":\"3259574\",\"ResourceName\": \"resourceNameTest\",\"ResouceId\": \"resourceId\"}"}}
       # need debug mode to make it send to kafka
        session_kafka_msg = """{\"schema\":\"uc4M56Qn8cIMHUTHUaFuag\",\"event\":{\"replayId\":12521409},\"payload\":{\"CreatedById\":\"00528000007LU4EAAW\",\"CreatedDate\":\"2020-04-17T09:41:30Z\",\"Content__c\":\"{\\"ReservationID\\":\\"a0G2x000000urVdEAITest0609-07\\", \\"OfflineReservationID\\":\\"a0G2x000000olCuEAI-test07\\",\\"StartTime\\":\\"2020-04-25T04:30:00Z\\", \\"EndTime\\":\\"2020-04-25T06:00:00Z\\",\\"SessionType\\":\\"Online Class\\",\\"SequenceNumber\\":1,\\"ProgramLevel\\":\\"D\\",\\"Program\\":\\"HFV3Plus\\",\\"Lessons\\":[{\\"UnitNumber\\":\\"1\\",\\"OnlineLessonTopicId\\":\\"10286\\",\\"OnlineLessonTopic\\":\\"Welcome Home! Lesson 2\\",\\"LessonNumber\\":\\"2\\"}],\\"IsDeleted\\":false,\\"GroupID\\":\\"a0B2x00000053OkEAI\\",\\"CenterCode\\":\\"SZA\\",\\"TeacherName\\":\\"Melody Lee\\",\\"RoomNumber\\":\\"3259574\\",\\"ResourceName\\": \\"resourceNameTest\\",\\"ResouceId\\": \\"resourceId\\"}\"}}"""
        session_member_kafka_msg = """{\"schema\":\"p_OsF3sYTCtPmu5kFcUAVg\",\"event\":{\"replayId\":11549228},\"payload\":{\"CreatedById\":\"0050I000008WoWKQA0\",\"CreatedDate\":\"2020-04-13T16:26:51Z\",\"Content__c\":\"{\\"CustomerID\\":\\"38085140\\",\\"ReservationID\\":\\"a0G0I00001PEIDvUAP\\",\\"GroupNumber\\":\\"100115891\\", \\"GroupId\\":\\"a0B0I00000aCParUAG\\",\\"AttendanceStatus\\":\\"Pending\\",\\"AttendanceResult\\":null,\\"IsRemoved\\":false,\\"LastModifiedDate\\":\\"2020-04-13T16:26:51.000Z\\",\\"SkillFocus\\":null,\\"RoomID\\":\\"a0G2x000000u6BzEAI\\",\\"PAId\\":\\"265351\\",\\"ContactIds\\":[\\"0030I000022z53JQAQ\\"]}\"}}"""
        producer = KafkaProducer(bootstrap_servers=kafka_broker)
        # send session message
        # producer.send(topic=session_topic_name, value=json.dumps(unlockinfo_kafka_msg).encode())
        # producer.send(topic=session_topic_name, value=session_kafka_msg.encode('utf-8'))
        producer.send(topic=session_member_topic_name, value=session_member_kafka_msg.encode('utf-8'))
        # consumer = KafkaConsumer(session_topic_name, bootstrap_servers=kafka_broker, auto_offset_reset='earliest',
        #                          group_id='connietest109')
        # i = 0
        # for message in consumer:
        #     i = i + 1
        #     print("the {0} message is: ".format(i))
        #     print(message)

    @Test(tags="qa")
    def test_unlock_info_produce_stg(self):
        BOOTSTRAP_SERVERS_QA = ['10.179.243.69:9092']
        BOOTSTRAP_SERVERS_STG = ['118.25.170.130:9092']
        BOOTSTRAP_SERVERS_LIVE = ['ckafka-hda06p3e.ap-shanghai.ckafka.tencentcloudmq.com:6092']
        TOPIC_NAME = 'OnlineHomeworkUnlock'
        TOPIC_NAME_QA = 'omni-unlock-info-topic'
        MESSAGE = """
        {
            "StudentId": "1122335678",
            "ContentPath": "highflyers/cn-3/book-2/unit-2/assignment-21",
            "GroupId": "group_id_test0610-01",
            "UnlockAt": "2020-04-18T19:07:01.2291692Z"
        }
        """
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS_LIVE,
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism='PLAIN',
            # staging credential
            # sasl_plain_username='ckafka-epk0cfr4#ksd',
            # sasl_plain_password='ksd',
            # live unlock kafka send credential
            sasl_plain_username='ckafka-hda06p3e#unlock',
            sasl_plain_password='unlock',
            api_version=(0, 10, 0)
        )
        print('sending message')
        producer.send(TOPIC_NAME, MESSAGE.encode('utf-8'))
        print('closing connection')
        producer.close()
        # print("message is put in topic")
        # consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BOOTSTRAP_SERVERS_LIVE,
        #                          security_protocol="SASL_PLAINTEXT",
        #                          sasl_mechanism='PLAIN',
        #                          # sasl_plain_username='ckafka-epk0cfr4#unlock',
        #                          # sasl_plain_username='ckafka-hda06p3e#unlock',
        #                          # sasl_plain_password='unlock',
        #                          sasl_plain_username='ckafka-hda06p3e#ksd',
        #                          sasl_plain_password='PwjhiZV-TGX.B1_1K',
        #                          api_version=(0, 10, 0), auto_offset_reset='earliest',
        #                          group_id='connietest1010')
        # i = 0
        # for message in consumer:
        #     i = i + 1
        #     print("the {0} message is: ".format(i))
        #     print(message)

