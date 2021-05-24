from ptest.decorator import TestClass, Test

from E1_API_Automation.Business.NGPlatform.ContentMapService import ContentMapService
from E1_API_Automation.Business.NGPlatform.GeneralTestService import GeneralTestService
from E1_API_Automation.Settings import CONTENT_MAP_ENVIRONMENT, GENERAL_TEST_ENVIRONMENT


@TestClass()
class UnlockSSUnitQuiz:

    @Test()
    def unlock_ss_unit_quiz(self):
        cm_service = ContentMapService(CONTENT_MAP_ENVIRONMENT)
        global unlock_response
        # from book start_index to end_index+1
        for book in range(1, 3):
            # from unit start_index to end_index+1
            for unit in range(1, 11):
                SS_EACH_BOOK = "smallstar/cn-3/book-{0}/unit-{1}".format(str(book), str(unit))
                course_node_response = cm_service.get_content_map_course_node(SS_EACH_BOOK,
                                                                              "WITH_DESCENDANTS").json()
                last_assignment_content_path = course_node_response['children'][course_node_response['childCount'] - 1][
                    'contentPath']
                general_test_svc = GeneralTestService(GENERAL_TEST_ENVIRONMENT)
                general_test = general_test_svc.get_test_by_student_and_content_path(1047,
                                                                                     SS_EACH_BOOK)
                if general_test.status_code == 204:
                    # 204 mean no unlock for current test
                    unlock_response = general_test_svc.put_unlock_unit_quiz(1047, last_assignment_content_path,"2021-05-27T06:41:01.000Z")
                    if unlock_response.status_code == 204:
                        print("content not exist: {0}".format(SS_EACH_BOOK), end='\n')
                        print("content not exist: {0}".format(last_assignment_content_path), end='\n')
