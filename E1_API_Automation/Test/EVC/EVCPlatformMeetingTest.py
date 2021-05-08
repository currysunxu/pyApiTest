from datetime import datetime, timedelta
from ptest.decorator import TestClass, Test, BeforeClass
from ptest.plogger import preporter
from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_DEMO_PAGE_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCLayoutCode



@TestClass()
class EVCPlatformMediaTest:
    @BeforeClass()
    def before_method(self):
        self.evc_meeting_service = EVCPlatformMeetingService(EVC_DEMO_PAGE_ENVIRONMENT)

    @Test(tags="stg")
    def test_agora_pl_recorded(self):
        start_time = datetime.now()
        class_duration = 5
        real_start_time = start_time + timedelta(minutes=1)
        end_time = real_start_time + timedelta(minutes=class_duration)

        # create meeting
        meeting_response = self.evc_meeting_service.meeting_create(int(start_time.timestamp() * 1000),
                                                                   int(end_time.timestamp() * 1000),
                                                                   int(real_start_time.timestamp() * 1000),
                                                                   layout_code=EVCLayoutCode.Agora_Kids_PL)
        meeting_token = (meeting_response["componentToken"])
        preporter.info("----Meeting token----: {0}".format(meeting_token))

        self.evc_meeting_service.trigger_record_class(meeting_token)
        self.evc_meeting_service.update_record_flag(meeting_token)
