from datetime import datetime, timedelta

from hamcrest import assert_that, is_, equal_to
from ptest.decorator import TestClass, Test, BeforeClass
from ptest.plogger import preporter

from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Lib.HamcrestExister import exist
from E1_API_Automation.Settings import EVC_PROXY_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCMeetingRole, EVCLayoutCode


@TestClass()
class EVCPlatformMediaTest:
    @BeforeClass()
    def before_method(self):
        self.teacher_name = "test teacher"
        self.student_name = "test student"

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_agora_pl_recorded(self, location):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])

        start_time = datetime.now()
        class_duration = 5
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=class_duration)

        # create meeting
        preporter.info("----Create meeting under domain----: {0}".format(EVC_PROXY_ENVIRONMENT[location]))
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              layout_code=EVCLayoutCode.Agora_Kids_PL)
        meeting_token = (meeting_response["componentToken"])
        preporter.info("----Meeting token----: {0}".format(meeting_token))

        evc_meeting_service.trigger_record_class(meeting_token)
        evc_meeting_service.update_record_flag(meeting_token)

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_teacher_bootstrap(self, location):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])

        start_time = datetime.now()
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=5)

        # create meeting
        preporter.info("----Create meeting under {0}----: {1}".format(location, EVC_PROXY_ENVIRONMENT[location]))
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              EVCLayoutCode.Kids_PL)
        meeting_token = meeting_response["componentToken"]
        preporter.info("----Generate {0} Meeting ----: {1}".format(EVCLayoutCode.Kids_PL, meeting_token))

        # register meeting & bootstrap
        teacher_info = evc_meeting_service.meeting_register(location, meeting_token, EVCMeetingRole.TEACHER,
                                                            self.teacher_name)
        bootstrap = evc_meeting_service.meeting_bootstrap(teacher_info["attendanceToken"])
        preporter.info(bootstrap)

        # check material structure is correct
        material_info = bootstrap
        assert_that(bootstrap, exist("layout"))
        assert_that(bootstrap, exist("roles"))
        assert_that(bootstrap, exist("config"))
        assert_that(bootstrap, exist("components"))
        assert_that(bootstrap["useWebSocket"], is_(False))
        assert_that(material_info["roleCode"], equal_to(EVCMeetingRole.TEACHER))
        assert_that(material_info["rtcProvider"], equal_to("agora"))

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_student_bootstrap(self, location):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])

        start_time = datetime.now()
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=30)

        # create meeting
        preporter.info("----Create meeting under {0}----: {1}".format(location, EVC_PROXY_ENVIRONMENT[location]))
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              EVCLayoutCode.Kids_PL)
        meeting_token = (meeting_response["componentToken"])
        preporter.info("----Meeting token----: {0}".format(meeting_token))

        # register meeting & bootstrap
        teacher_info = evc_meeting_service.meeting_register(location, meeting_token, EVCMeetingRole.STUDENT,
                                                            self.student_name)
        bootstrap = evc_meeting_service.meeting_bootstrap(teacher_info["attendanceToken"])
        preporter.info(bootstrap)

        # check material structure is correct
        material_info = bootstrap
        assert_that(bootstrap, exist("layout"))
        assert_that(bootstrap, exist("roles"))
        assert_that(bootstrap, exist("config"))
        assert_that(bootstrap, exist("components"))
        assert_that(bootstrap["useWebSocket"], is_(False))
        assert_that(material_info["roleCode"], equal_to(EVCMeetingRole.STUDENT))
        assert_that(material_info["rtcProvider"], equal_to("agora"))

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_teacher_loadstate(self, location):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])

        start_time = datetime.now()
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=30)

        # create meeting
        preporter.info("----Create meeting under {0}----: {1}".format(location, EVC_PROXY_ENVIRONMENT[location]))
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              EVCLayoutCode.Kids_PL)
        meeting_token = meeting_response["componentToken"]
        preporter.info("----Generate {0} Meeting ----: {1}".format(EVCLayoutCode.Kids_PL, meeting_token))

        # register meeting & bootstrap
        teacher_info = evc_meeting_service.meeting_register(location, meeting_token, EVCMeetingRole.TEACHER,
                                                            self.teacher_name)
        loadstate = evc_meeting_service.meeting_loadstate(teacher_info["attendanceToken"])
        preporter.info(loadstate)

        # check loadstate
        assert_that(loadstate["displayName"], equal_to(self.teacher_name))
        assert_that(loadstate["roleCode"], equal_to(EVCMeetingRole.TEACHER))
        assert_that(loadstate["state"], equal_to(2270))

    @Test(tags="stg, live", data_provider=["CN", "SG", "US", "SG", "CN_NEW", "SG_NEW", "US_NEW", "SG_NEW"])
    def test_student_loadstate(self, location):
        evc_meeting_service = EVCPlatformMeetingService(EVC_PROXY_ENVIRONMENT[location])

        start_time = datetime.now()
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=5)

        # create meeting
        preporter.info("----Create meeting under {0}----: {1}".format(location, EVC_PROXY_ENVIRONMENT[location]))
        meeting_response = evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                              int(end_time.timestamp() * 1000),
                                                              int(real_start_time.timestamp() * 1000),
                                                              EVCLayoutCode.Kids_PL)
        meeting_token = meeting_response["componentToken"]
        preporter.info("----Generate {0} Meeting ----: {1}".format(EVCLayoutCode.Kids_PL, meeting_token))

        # register meeting & bootstrap
        teacher_info = evc_meeting_service.meeting_register(location, meeting_token, EVCMeetingRole.STUDENT,
                                                            self.student_name)
        loadstate = evc_meeting_service.meeting_loadstate(teacher_info["attendanceToken"])
        preporter.info(loadstate)

        # check loadstate
        assert_that(loadstate["displayName"], equal_to(self.student_name))
        assert_that(loadstate["roleCode"], equal_to(EVCMeetingRole.STUDENT))
        assert_that(loadstate["state"], equal_to(1502))
