class UnlockServiceData:
    session_topic_name = 'OMNI-OfflineCourse'
    session_member_topic_name = 'OMNI-SessionMember'
    session_content = {"schema": "JJMZL8Q33SrEcmVRvXRklgooo","payload": {"CreatedById": "00528000007M5dbAAC","CreatedDate": "2019-10-25T04:04:40Z","Content__c": "{\"TeacherName\":\"Milanda Gumede\",\"StartTime\":\"{0.start_time}\",\"SessionType\":\"{0.type}\",\"SequenceNumber\":\"{0.sequence}\",\"ResourceName\":\"Amazing\",\"ResouceId\":\"a0J0I00000PRVMfUAP\",\"ReservationID\":\"{0.reservation_id}\",\"ProgramLevel\":\"{0.course_level}\",\"Program\":\"{0.course}\",\"Lessons\":{1},\"IsDeleted\":{0.is_deleted},\"GroupID\":\"{0.group_id}\",\"EndTime\":\"{0.end_time}\",\"CenterCode\":\"BJJ\"}"},"event": {"replayId": 20120235}}
    session_member_content = {"schema": "p_OsF3sYTCtPmu5kFcUAVg","payload": {"CreatedById": "0050I000008LIs9QAG","CreatedDate": "2019-09-28T14:16:05Z","Content__c": "{\"ReservationID\":\"{0.session_id}\",\"PAId\":null,\"LastModifiedDate\":\"2019-09-28T14:16:02.000Z\",\"IsRemoved\":{0.is_removed},\"GroupId\":null,\"CustomerID\":\"{0.student_id}\",\"ContactIds\":[],\"AttendanceStatus\":\"Completed\",\"AttendanceResult\":\"Absent\"}"},"event": {"replayId": 92534}}


class UnlockKafkaServer:
    kafka_broker = {'QA': '10.178.86.209:9092'}
