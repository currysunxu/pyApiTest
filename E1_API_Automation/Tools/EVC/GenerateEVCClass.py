import time
from datetime import datetime, timedelta

from ptest.plogger import preporter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from E1_API_Automation.Business.EVC.EVCPlatformMeetingService import EVCPlatformMeetingService
from E1_API_Automation.Settings import EVC_DEMO_PAGE_ENVIRONMENT
from E1_API_Automation.Test_Data.EVCData import EVCMeetingRole, EVCLayoutCode

class_duration = 5

platform_service = EVCPlatformMeetingService(EVC_DEMO_PAGE_ENVIRONMENT)


def generate_chrome_option():
    options = ChromeOptions()
    options.add_argument("use-fake-ui-for-media-stream")  # grant the permissions of micro and camera
    options.add_argument("use-fake-device-for-media-stream")  # use fake video & audio
    options.add_argument("ignore-certificate-errors")  # ignore certificate errors
    options.headless = False
    return options


def click_auto_play(web_driver):
    wait = WebDriverWait(web_driver, 15)
    try:
        auto_play_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='classroom-splash']/div[2]/div[1]")))
        preporter.info("Auto play button shows.")
        auto_play_button.click()
    except:
        preporter.info("Auto play button doesn't not show.")


def register_user(meeting_token, amount):
    student_info_list = []

    if meeting_token is not None or meeting_token != "" and amount > 0:
        for i in range(amount):
            student_info = platform_service.meeting_register("SG", meeting_token, EVCMeetingRole.STUDENT,
                                                             "test student {0}".format(i))
            platform_service.meeting_bootstrap(student_info["attendanceToken"])
            student_info_list.append(student_info["attendanceToken"])

    return student_info_list


def mock_omni_class_booking(layout_code, student_amount):
    start_time = datetime.now()
    real_start_time = start_time + timedelta(minutes=1)
    end_time = real_start_time + timedelta(minutes=class_duration)

    # create meeting
    meeting_response = platform_service.meeting_create(int(start_time.timestamp() * 1000),
                                                       int(end_time.timestamp() * 1000),
                                                       int(real_start_time.timestamp() * 1000),
                                                       layout_code)
    meeting_token = (meeting_response["componentToken"])
    preporter.info("----Meeting token----: {0}".format(meeting_token))

    # update material
    if layout_code == EVCLayoutCode.Kids_PL:
        platform_service.meeting_update(meeting_token, 10999)
    else:
        platform_service.meeting_update_by_material(meeting_token)

    # register meeting & bootstrap
    teacher_info = platform_service.meeting_register("SG", meeting_token, EVCMeetingRole.TEACHER, "test teacher")
    teacher_bootstrap = platform_service.meeting_bootstrap(teacher_info["attendanceToken"])

    # register student & bootstrap
    student_info_list = register_user(meeting_token, student_amount)

    # get loadstate
    teacher_loadstate = platform_service.meeting_loadstate(teacher_info["attendanceToken"])

    # enter classroom
    options = generate_chrome_option()
    teacher_web_driver = webdriver.Chrome(chrome_options=options)
    teacher_web_driver.get(platform_service.get_class_entry_url(teacher_info["attendanceToken"]))
    click_auto_play(teacher_web_driver)

    student_web_driver = webdriver.Chrome(chrome_options=options)

    for i in range(student_amount):
        if i > 0:
            student_web_driver.execute_script("window.open('');")
            student_web_driver.switch_to.window(student_web_driver.window_handles[i])
        student_web_driver.get(platform_service.get_class_entry_url(student_info_list[i]))

        # set local storage to skip tech check
        student_web_driver.execute_script(
            "window.localStorage.setItem('evc15_tech_check_last_timestamp','{0}');".format(
                str(start_time.timestamp() * 1000)))

        click_auto_play(student_web_driver)

    preporter.info("----Trigger recording with token----: {0}".format(meeting_token))
    platform_service.trigger_record_class(meeting_token)

    time.sleep(class_duration * 60 - 160)


if __name__ == "__main__":
    mock_omni_class_booking(EVCLayoutCode.Indo_FR_GL, 5)
    # mock_omni_class_booking(EVCLayoutCode.Kids_PL, 1)
