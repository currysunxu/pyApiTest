from datetime import datetime, timedelta
from time import sleep

import jmespath
from hamcrest import assert_that
from hamcrest import is_not
from ptest.decorator import TestClass, Test, BeforeClass
from ptest.plogger import preporter

from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Lib.HamcrestMatcher import match_to
from E1_API_Automation.Settings import EVC_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCComponent
from E1_API_Automation.Test_Data.EVCData import EVCMeetingRole, EVCLayoutCode


@TestClass()
class EVCPlatformMeetingTest:

    @BeforeClass()
    def before_method(self):
        self.meeting_duration = 5

    # @Test(tags="stg", data_provider={"SG", "UK", "US"})
    def test_china_tb_pl(self, teacher_location):
        cn_pl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        start_time = datetime.now()
        class_duration = 10
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = cn_pl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.CN_TB_PL)
        meeting_token = (meeting_response["componentToken"])
        teacher_info = cn_pl_meeting.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER, "teacher")
        student_info = cn_pl_meeting.meeting_register("CN", meeting_token, EVCMeetingRole.STUDENT, "student")

        cn_pl_meeting.meeting_update(meeting_token, "10999")
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])
        teacher_url = teacher_service.get_class_entry_url(teacher_info["attendanceToken"])
        stu_classurl = cn_student_service.get_class_entry_url(student_info["attendanceToken"])
        stu_bootstrap = cn_student_service.meeting_bootstrap(student_info["attendanceToken"])

        assert_that(jmespath.search('layout.template', stu_bootstrap) == 'kids', 'The layout template should be kids')
        assert_that(sorted(jmespath.search('components[].componentTypeCode', stu_bootstrap)) == sorted(EVCComponent.PL),
                    'the component list is not correct')

        assert_that(jmespath.search('roleCode', stu_bootstrap) == EVCMeetingRole.STUDENT, 'should be student role')
        assert_that(stu_bootstrap, match_to("rtcProvider"))

        teacher_bootstrap = teacher_service.meeting_bootstrap(teacher_info["attendanceToken"])
        assert_that(jmespath.search('roleCode', teacher_bootstrap) == EVCMeetingRole.TEACHER, 'should be teacher role')
        assert_that(jmespath.search('layout.template', teacher_bootstrap) == 'kids',
                    'The layout template should be kids')

    # @Test(tags="stg", data_provider={"SG", "UK", "US"})
    def test_china_ss_pl(self, teacher_location):
        cn_pl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        start_time = datetime.now()
        class_duration = 10
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = cn_pl_meeting.meeting_create(int(start_time.timestamp() * 1000),
                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.CN_SS_PL)
        meeting_token = (meeting_response["componentToken"])
        teacher_info = cn_pl_meeting.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER, "teacher")
        student_info = cn_pl_meeting.meeting_register("CN", meeting_token, EVCMeetingRole.STUDENT, "student")

        cn_pl_meeting.meeting_update(meeting_token, "10999")
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])
        teacher_url = teacher_service.get_class_entry_url(teacher_info["attendanceToken"])
        stu_classurl = cn_student_service.get_class_entry_url(student_info["attendanceToken"])
        stu_bootstrap = cn_student_service.meeting_bootstrap(student_info["attendanceToken"])

        assert_that(jmespath.search('layout.template', stu_bootstrap) == 'kids', 'The layout template should be kids')
        assert_that(sorted(jmespath.search('components[].componentTypeCode', stu_bootstrap)) == sorted(EVCComponent.PL),
                    'the component list is not correct')

        assert_that(jmespath.search('roleCode', stu_bootstrap) == EVCMeetingRole.STUDENT, 'shold be student role')
        assert_that(stu_bootstrap, match_to("rtcProvider"))

        teacher_bootstrap = teacher_service.meeting_bootstrap(teacher_info["attendanceToken"])
        assert_that(jmespath.search('roleCode', teacher_bootstrap) == EVCMeetingRole.TEACHER, 'should be teacher role')
        assert_that(jmespath.search('layout.template', teacher_bootstrap) == 'kids',
                    'The layout template should be kids')

    # @Test(tags="stg", data_provider={"SG", "UK", "US"})
    def test_china_hf_pl(self, teacher_location):
        cn_pl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        start_time = datetime.now()
        class_duration = self.meeting_duration
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = cn_pl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.CN_HF_PL)
        meeting_token = (meeting_response["componentToken"])
        teacher_info = cn_pl_meeting.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER, "teacher")
        student_info = cn_pl_meeting.meeting_register("CN", meeting_token, EVCMeetingRole.STUDENT, "student")

        cn_pl_meeting.meeting_update(meeting_token, "10999")
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])
        teacher_url = teacher_service.get_class_entry_url(teacher_info["attendanceToken"])
        stu_classurl = cn_student_service.get_class_entry_url(student_info["attendanceToken"])
        stu_bootstrap = cn_student_service.meeting_bootstrap(student_info["attendanceToken"])

        assert_that(jmespath.search('layout.template', stu_bootstrap) == 'kids', 'The layout template should be kids')
        assert_that(sorted(jmespath.search('components[].componentTypeCode', stu_bootstrap)) == sorted(EVCComponent.PL),
                    'the component list is not correct')

        assert_that(jmespath.search('roleCode', stu_bootstrap) == EVCMeetingRole.STUDENT, 'shold be student role')
        assert_that(stu_bootstrap, match_to("rtcProvider"))

        teacher_bootstrap = teacher_service.meeting_bootstrap(teacher_info["attendanceToken"])
        assert_that(jmespath.search('roleCode', teacher_bootstrap) == EVCMeetingRole.TEACHER, 'should be teacher role')
        assert_that(jmespath.search('layout.template', teacher_bootstrap) == 'kids',
                    'The layout template should be kids')

    # @Test(tags="stg", data_provider={"SG"})
    def test_id_hf_gl(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = self.meeting_duration
        class_num = 10
        real_start_time = start_time
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
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

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

    # @Test(tags="stg", data_provider={"SG"})
    def test_id_fr_gl(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = 15
        class_num = 10
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_FR_GL)

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
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

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

    # @Test(tags="stg", data_provider={"SG"})
    def test_id_tb_gl(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = 5
        class_num = 3
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_TB_GL)

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
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

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

    @Test(tags="stg", data_provider={"SG"})
    def test_id_ss_gl(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = 5
        class_num = 3
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_SS_GL)

        meeting_token = (meeting_response["componentToken"])
        teacher_info = sg_gl_meeting.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER,
                                                      "teacheret er irueiiuwouei uorueiiuwoue")
        student_list = []
        for i in range(0, class_num):
            sleep(1)
            student = sg_gl_meeting.meeting_register("SG", meeting_token,
                                                     EVCMeetingRole.STUDENT,
                                                     "student ier eoeuwiu nt ier eoeuwiu ooiowruorowruoowr_" + str(i))
            student_list.append(student)

        sg_gl_meeting.meeting_update_by_material(meeting_token)
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

        teacher_url = teacher_service.get_class_entry_url(teacher_info["attendanceToken"])

        for stu in student_list:
            stu_classurl = cn_student_service.get_class_entry_url(stu["attendanceToken"])
            sleep(1)
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

    # @Test(tags="stg, live", data_provider=["SG"])
    def test_indo_phonics_gl_meeting_create(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = 5
        class_num = 2
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_Phonics_GL)

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
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

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

    # @Test(tags="stg", data_provider=["SG"])
    def test_indo_speak_up_gl_meeting_create(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = self.meeting_duration
        class_num = 2
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_Speak_Up_GL)

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
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

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

    # @Test(tags="stg", data_provider=["SG"])
    def test_indo_story_teller_gl_meeting_create(self, teacher_location):
        sg_gl_meeting = EVCPlatformMeetingService(EVC_ENVIRONMENT["SG"])
        start_time = datetime.now()
        class_duration = self.meeting_duration
        class_num = 2
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)
        # create meeting
        meeting_response = sg_gl_meeting.meeting_create(int(start_time.timestamp() * 1000),

                                                        int(end_time.timestamp() * 1000),
                                                        int(real_start_time.timestamp() * 1000),
                                                        EVCLayoutCode.Indo_Story_Teller_GL)

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
        cn_student_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        teacher_service = EVCPlatformMeetingService(EVC_ENVIRONMENT[teacher_location])

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
        evc_meeting_service = EVCPlatformMeetingService(EVC_ENVIRONMENT["CN"])
        start_time = datetime.now()
        class_duration = 5
        real_start_time = start_time
        end_time = real_start_time + timedelta(minutes=class_duration)

        # create meeting
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              layout_code=EVCLayoutCode.Kids_PL)
        meeting_token = (meeting_response["componentToken"])
        preporter.info("----Meeting token----: {0}".format(meeting_token))

        evc_meeting_service.trigger_record_class(meeting_token)
        evc_meeting_service.update_record_flag(meeting_token)
