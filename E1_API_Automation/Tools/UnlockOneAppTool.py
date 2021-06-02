from hamcrest import assert_that
from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.NGPlatform.CourseGroupService import CourseGroupService
from E1_API_Automation.Business.NGPlatform.GeneralTestService import GeneralTestService
from E1_API_Automation.Business.Utils.CommonUtils import CommonUtils


@TestClass()
class UnlockSSUnitQuiz:

    @Test()
    def unlock_ss_unit_quiz(self):
        cm_service = ContentMapService()
        student_id = 101334620
        global unlock_response
        # from book start_index to end_index+1
        for book in range(3, 4):
            # from unit start_index to end_index+1
            for unit in range(1, 11):
                SS_EACH_BOOK = "smallstar/cn-3/book-{0}/unit-{1}".format(str(book), str(unit))
                course_node_response = cm_service.get_content_map_course_node(SS_EACH_BOOK,
                                                                              "WITH_DESCENDANTS").json()
                last_assignment_content_path = course_node_response['children'][course_node_response['childCount'] - 1][
                    'contentPath']
                general_test_svc = GeneralTestService()
                general_test = general_test_svc.get_test_by_student_and_content_path(student_id,
                                                                                     SS_EACH_BOOK)
                if general_test.status_code == 204:
                    # 204 mean no unlock for current test
                    unlock_response = general_test_svc.put_unlock_unit_quiz(1047, last_assignment_content_path,
                                                                            "2021-05-26T06:41:01.000Z")
                    if unlock_response.status_code == 204:
                        print("content not exist: {0}".format(SS_EACH_BOOK), end='\n')
                        print("content not exist: {0}".format(last_assignment_content_path), end='\n')

    @Test()
    def unlock_course_group(self):
        student_id = 100211067
        unlock_content_path = "smallstar/cn-3/book-4/unit-{0}/assignment-{1}"
        cm_service = ContentMapService()
        # from unit start_index to end_index+1
        for unit in range(1, 11):
            # from unit start_index to end_index+1
            unit_path = unlock_content_path.format(str(unit), "")
            end_index = CommonUtils.last_index_of(unit_path, "/") - 1
            course_node_response = cm_service.get_content_map_course_node(unit_path[:end_index],
                                                                          "WITH_DESCENDANTS").json()
            lesson_count = course_node_response['childCount']+1
            for lesson in range(1, lesson_count):
                content_path = unlock_content_path.format(str(unit), str(lesson))
                course_group_service = CourseGroupService()
                response = course_group_service.put_unlock_practice(student_id, content_path,"2021-06-01T06:41:01.000Z")
                assert_that(response.status_code == 200)
