from E1_API_Automation.Test_Data.KafkaData import KafkaData
from E1_API_Automation.Business.HighFlyer35.Hf35KafkaService import Kafka_producer,Kafka_consumer
from ptest.decorator import TestClass, Test
from E1_API_Automation.Settings import *
from E1_API_Automation.Business.HighFlyer35.HighFlyerUtils.Hf35BffUtils import Hf35BffUtils
from hamcrest import assert_that, equal_to
import time


@TestClass()
class Hf35KafkaTest():

    @Test(tags="qa, stg",data_provider = ["highflyers/cn-3-144/book-7/unit-1/assignment-2","highflyers/cn-3/book-7/unit-2/assignment-2"])
    def test_insert_from_online_homework_unlock_to_student_unlock_study_plan(self,content_path):
        host = KafkaData.BOOTSTRAP_SERVERS[env_key]
        producer = Kafka_producer(host,'OnlineHomeworkUnlock')
        message = KafkaData.build_online_homework_unlock_message_by_content_path(content_path)
        producer.sendjsondata(message)
        # Todo replace sleep by consumer is over
        time.sleep(8)
        study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(message['StudentId'], 1, content_path)
        assert_that(study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S"), equal_to(message['UnlockAt'][:message['UnlockAt'].index('.')]))
        reader_study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(message['StudentId'], 512, content_path)
        assert_that(reader_study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S"), equal_to(message['UnlockAt'][:message['UnlockAt'].index('.')]))


    @Test(tags="qa, stg", data_provider=["highflyers/cn-3-144/book-7/unit-1/assignment-2","highflyers/cn-3/book-7/unit-2/assignment-2"])
    def test_update_from_online_homework_unlock_to_student_unlock_study_plan(self, content_path):
        host = KafkaData.BOOTSTRAP_SERVERS[env_key]
        producer = Kafka_producer(host, 'OnlineHomeworkUnlock')
        message = KafkaData.build_online_homework_unlock_message_by_content_path(content_path)
        producer.sendjsondata(message)
        time.sleep(2)
        message['UnlockAt'] = time.strftime("%Y-%m-%dT%H:%M:%S.%j", time.localtime())
        producer.sendjsondata(message)
        # Todo replace sleep by consumer is over
        time.sleep(8)
        study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(message['StudentId'], 1, content_path)
        assert_that(study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S"), equal_to(message['UnlockAt'][:message['UnlockAt'].index('.')]))
        reader_study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(message['StudentId'], 512, content_path)
        assert_that(reader_study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S"), equal_to(message['UnlockAt'][:message['UnlockAt'].index('.')]))


    @Test(tags="qa, stg",data_provider = [("highflyers/cn-3/book-2/unit-6/assignment-1","City-Wide Classroom","HFV3Plus"),("highflyers/cn-3/book-2/unit-6/assignment-1","Online Classroom","HFV3Plus"),
                                          ("smallstar/cn-3/book-2/unit-6/assignment-1","Online Classroom","SSV3"),("tb16/cn-3/book-2/unit-6/assignment-1","Online Classroom","TBV3Plus")])
    def test_insert_from_omni_student_sessions_to_student_sessions_study_plan(self,content_path,group_type,product):
        host = KafkaData.BOOTSTRAP_SERVERS[env_key]
        producer = Kafka_producer(host,'OMNI-StudentSession')
        # group type distinguish gl and pl
        message = KafkaData.build_omni_sessions_message(group_type,product)
        producer.sendjsondata(message)
        time.sleep(5)
        payload_message = message['payload']['Content__c']
        study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(payload_message['customerId'], 256, content_path)
        assert_that(study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S"), equal_to(payload_message['startTime'][:payload_message['startTime'].index('.')]))

    @Test(tags="qa, stg",data_provider = [("highflyers/cn-3/book-2/unit-6/assignment-1","City-Wide Classroom","HFV3Plus"),("smallstar/cn-3/book-2/unit-6/assignment-1","Online Classroom","SSV3")])
    def test_update_remove_from_omni_student_sessions_to_student_sessions_study_plan(self,content_path,group_type,product):
        host = KafkaData.BOOTSTRAP_SERVERS[env_key]
        producer = Kafka_producer(host,'OMNI-StudentSession')
        # group type distinguish gl and pl
        message = KafkaData.build_omni_sessions_message(group_type,product)
        producer.sendjsondata(message)
        time.sleep(5)
        message['payload']['Content__c']['startTime'] = time.strftime("%Y-%m-%dT%H:%M:%S.%jZ", time.localtime())
        producer.sendjsondata(message)
        time.sleep(5)
        payload_message = message['payload']['Content__c']
        study_plan = Hf35BffUtils.get_study_plan_by_student_id_from_db(payload_message['customerId'], 256, content_path)
        assert_that(study_plan['effect_at'].strftime("%Y-%m-%dT%H:%M:%S"), equal_to(payload_message['startTime'][:payload_message['startTime'].index('.')]))
        message['payload']['Content__c']['isRemoved'] = True
        producer.sendjsondata(message)
        time.sleep(5)
        study_plan = Hf35BffUtils.get_count_study_plan_by_student_id_from_db(payload_message['customerId'], 256, content_path)
        assert_that(study_plan, equal_to(0))