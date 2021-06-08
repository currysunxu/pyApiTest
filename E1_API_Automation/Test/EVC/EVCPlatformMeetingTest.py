import jmespath
from datetime import datetime, timedelta

from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass
from ptest.plogger import preporter
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Lib.HamcrestExister import Exist
from E1_API_Automation.Settings import EVC_DEMO_PAGE_ENVIRONMENT, EVC_PROXY_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCLayoutCode, EVCMeetingRole, EVCComponent, RTCProvider


@TestClass()
class EVCPlatformMediaTest:

    @Test(data_provider={"SG", "UK", "US"})
    def test_china_pl(self, teacher_location):
        cn_pl_meeting = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT["CN"])
        start_time = datetime.now()
        class_duration = 10
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = cn_pl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Agora_Kids_PL)
        meeting_token = (meeting_response["componentToken"])
        teacher_info = cn_pl_meeting.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER,
                                                      "teacher")
        student_info = cn_pl_meeting.meeting_register("CN", meeting_token,
                                                      EVCMeetingRole.STUDENT,
                                                      "student")
        cn_pl_meeting.meeting_update(meeting_token, "10999")
        cn_student_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[teacher_location])
        teacher_url = teacher_service.get_class_entry_url(teacher_info["attendanceToken"])
        stu_classurl = cn_student_service.get_class_entry_url(student_info["attendanceToken"])

        cn_pl_meeting.trigger_record_class(meeting_token)
        stu_bootstrap = cn_student_service.meeting_bootstrap(student_info["attendanceToken"])

        assert_that(jmespath.search('layout.template', stu_bootstrap) == 'kids', 'The layout template should be kids')
        assert_that(sorted(jmespath.search('components[].componentTypeCode', stu_bootstrap)) == sorted(EVCComponent.PL),
                    'the component list is not correct')

        assert_that(jmespath.search('roleCode', stu_bootstrap) == EVCMeetingRole.STUDENT, 'shold be student role')
        assert_that(stu_bootstrap, match_to("rtcProvider"))

        teacher_bootstrap = teacher_service.meeting_bootstrap(teacher_info["attendanceToken"])
        assert_that(jmespath.search('roleCode', teacher_bootstrap) == EVCMeetingRole.TEACHER, 'shold be teacher role')
        assert_that(jmespath.search('layout.template', teacher_bootstrap) == 'kids',
                    'The layout template should be kids')

    @Test(data_provider={"SG"})
    def test_id_gl(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = 15
        class_num = 10
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_HF_GL)

        meeting_token = (meeting_response["componentToken"])
        teacher_info = sg_gl_meeting.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER,
                                                      "teacheret er irueiiuwouei uorueiiuwoue")
        student_list = []
        for i in range(0, class_num):
            student = sg_gl_meeting.meeting_register("SG", meeting_token,
                                                     EVCMeetingRole.STUDENT,
                                                     "student ier eoeuwiu nt ier eoeuwiu ooiowruorowruoowr_" + str(i))
            student_list.append(student)

        sg_gl_meeting.meeting_update_by_material(meeting_token)
        cn_student_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[teacher_location])

        teacher_url = teacher_service.get_class_entry_url(teacher_info["attendanceToken"])

        for stu in student_list:
            stu_classurl = cn_student_service.get_class_entry_url(stu["attendanceToken"])
            stu_bootstrap = cn_student_service.meeting_bootstrap(stu["attendanceToken"])
            assert_that(jmespath.search('layout.template', stu_bootstrap) == 'kids',
                        'The layout template should be kids')
            assert_that(
                sorted(jmespath.search('components[].componentTypeCode', stu_bootstrap)) == sorted(EVCComponent.GL),
                'the component list is not correct')

            assert_that(jmespath.search('roleCode', stu_bootstrap) == EVCMeetingRole.STUDENT, 'shold be student role')
            assert_that(stu_bootstrap, match_to("rtcProvider"))

        sg_gl_meeting.trigger_record_class(meeting_token)

        teacher_bootstrap = teacher_service.meeting_bootstrap(teacher_info["attendanceToken"])
        assert_that(jmespath.search('roleCode', teacher_bootstrap) == EVCMeetingRole.TEACHER, 'shold be teacher role')
        assert_that(jmespath.search('layout.template', teacher_bootstrap) == 'kids',
                    'The layout template should be kids')

    @Test(tags="stg")
    def test_agora_pl_recorded(self):
        evc_meeting_service = EVCPlatformMeetingService(EVC_DEMO_PAGE_ENVIRONMENT)
        start_time = datetime.now()
        class_duration = 5
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=class_duration)

        # create meeting
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              layout_code=EVCLayoutCode.Agora_Kids_PL)
        meeting_token = (meeting_response["componentToken"])

        preporter.info("----Meeting token----: {0}".format(meeting_token))

        evc_meeting_service.trigger_record_class(meeting_token)
        evc_meeting_service.update_record_flag(meeting_token)

    @Test(
        data_provider={EVCLayoutCode.CN_HF_PL, EVCLayoutCode.CN_SS_PL, EVCLayoutCode.CN_TB_PL, EVCLayoutCode.Indo_HF_GL,
                       EVCLayoutCode.Indo_SS_GL, EVCLayoutCode.Indo_TB_GL, EVCLayoutCode.Indo_Phonics_GL,
                       EVCLayoutCode.Indo_Speak_Up_GL, EVCLayoutCode.Indo_Story_Teller_GL})
    def test_layoutcode(self, layout_code):
        meeting = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT["CN"])
        start_time = datetime.now()
        class_duration = 10
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                  int(end_time.timestamp() * 1000),
                                                  int(real_start_time.timestamp() * 1000),
                                                  layout_code)

        assert_that(meeting_response, Exist("componentToken"))
