import time
import arrow
import jmespath

from E1_API_Automation.Lib.Moutai import Moutai, Token
from E1_API_Automation.Settings import Environment


class SmallStarService():
    def __init__(self, host):
        self.host = host
        print(self.host)
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def login(self, username, password):
        user_info = {
            "UserName": username,
            "Password": password,
            "DeviceId": "",
            "DeviceType": "",
            "Platform": 0
        }
        return self.mou_tai.set_request_context("post", user_info, "/api/v2/Authentication/SS/")

    def get_student_profile(self):
        return self.mou_tai.get("/api/v2/StudentProfile/SS/")

    def get_small_star_unlock(self, book_key):
        return self.mou_tai.get("/api/v2/CourseUnlock/SmallStar/{}".format(book_key))

    def get_activity_sync(self, product_code, book_key, upserts_only=True):
        body = {
            "BookKey": book_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": 2147483646
        }
        response = self.mou_tai.post("/api/v2/Activity/Synchronize/", json=body)
        return jmespath.search("Upserts", response.json())

    def course_node(self, book_key, upserts_only=True, last_synchronized_key=None, last_Synchronized_Stamp=None):
        body = {
            "BookKey": book_key,
            "ProductCode": product_code,
            "UpsertsOnly": upserts_only,
            "Amount": 2147483646
        }
        if last_synchronized_key and last_synchronized_key is not None:
            body['LastSynchronizedStamp'] = last_Synchronized_Stamp
            body['LastSynchronizeKey'] = last_synchronized_key
        response = self.mou_tai.post("/api/v2/CourseNode/Synchronize/", json=body)
        return jmespath.search("Upserts", response.json())

    def submit_small_star_student_answers(self, pass_perfect, activity_key, student_id, group_id):
        body = SubmitActivityAnswerBody.generate_activity_answer(pass_perfect, activity_key, student_id, group_id)
        return self.mou_tai.post("/api/v2/ActivityAnswer/SmallStar/", json=body)


class SubmitActivityAnswerBody():

    @staticmethod
    def set_answers(pass_perfect, activity_key, activity_course_key, question_key, total_star):

        activity_type = get_activity_type(activity_key)
        answers = {
            "ActivityCourseKey": activity_course_key,
            "ActivityKey": activity_key,
            "Attempts": None,
            "Detail": {"moduleData": None},
            "Duration": 2,
            "LocalEndStamp": arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssZZ'),
            "LocalStartStamp": None,
            "QuestionKey": question_key,
            "Key": None,
            "TotalScore": total_star,
            "TotalStar": total_star,
        }
        if pass_perfect:
            answers["Star"] = total_star
            answers["Score"] = total_star
        elif activity_type == 'ssTracingWord':
            answers["Star"] = total_star
            answers["Score"] = total_star
        elif activity_type == 'dialogue':
            answers["Star"] = total_star
            answers["Score"] = total_star
        elif activity_type == 'reader':
            answers["Star"] = total_star
            answers["Score"] = total_star
        elif activity_type == 'readerLongText':
            answers["Star"] = total_star
            answers["Score"] = total_star
        elif activity_type == 'ssTracingLetter':
            answers["Star"] = total_star
            answers["Score"] = total_star
        else:
            answers["Star"] = 0
            answers["Score"] = 0.0
        return answers

    @staticmethod
    def generate_activity_answer(pass_perfect, activity_key, student_id, group_id):
        def split(li: list, new_list=[]):
            for ele in li:
                if isinstance(ele, list):
                    split(ele)
                else:
                    new_list.append(ele)
            return new_list

        li = get_question_key(activity_key)
        question_keys = split(li)
        activity_answer_body = {
            "ActivityCourseKey": get_activity_course_key(activity_key),
            "ActivityKey": activity_key,
            "StudentId": student_id,
            "GroupId": group_id
        }
        answers = [
            SubmitActivityAnswerBody.set_answers(pass_perfect,
                                                 activity_key,
                                                 get_activity_course_key(activity_key),
                                                 question_key,
                                                 get_total_star(question_key, activity_key))
            for question_key in question_keys]
        activity_answer_body["Answers"] = answers
        print(activity_answer_body)
        return activity_answer_body


def get_unlock_lesson_keys():
    unlock_lesson_keys = small_star_service.get_small_star_unlock(book_key).json()
    return unlock_lesson_keys


def get_lesson_nodes():
    course_node = small_star_service.course_node(book_key)
    return jmespath.search("@[?Level ==`8`]", course_node)


def get_lesson_keys_by_unit_key():
    unit_key = get_unit_keys_by_unit_name()
    lesson_node = get_lesson_nodes()
    lesson_keys = jmespath.search("@[?ParentNodeKey=='{0}'].Key".format(unit_key), lesson_node)
    return lesson_keys


def get_unit_nodes():
    course_node = small_star_service.course_node(book_key)
    return jmespath.search("@[?Level ==`4`]", course_node)


def get_unit_keys_by_unit_name():
    unit_node = get_unit_nodes()
    unit_key = jmespath.search("@[?Name == '{}'].Key".format(unit_name), unit_node)[0]
    return unit_key


def get_activity_nodes():
    course_node = small_star_service.course_node(book_key)
    return jmespath.search("@[?Level ==`16`]", course_node)


def get_activity_keys(lesson_key):
    course_node = get_activity_nodes()
    activity_keys = jmespath.search("@[?ParentNodeKey=='{0}'].ActivityKeys[0]".format(lesson_key), course_node)
    return activity_keys


def get_activity_type(activity_key):
    activity_sync = small_star_service.get_activity_sync(product_code, book_key)
    activity_type = jmespath.search("@[?Key=='{}'].Type".format(activity_key), activity_sync)[0]
    return activity_type


def get_activity_course_key(activity_key):
    curse_node = small_star_service.course_node(book_key)
    activity_nodes = jmespath.search("@[?Level ==`16`]", curse_node)
    activity_course_key = jmespath.search("@[?ActivityKeys[0]=='{0}'].Key".format(activity_key), activity_nodes)[0]
    return activity_course_key


def get_question_key(activity_key):
    response = small_star_service.get_activity_sync(product_code, book_key)
    question_keys = jmespath.search("@[?Key=='{}'].Questions[*].Key".format(activity_key), response)
    return question_keys


def get_total_star(question_key, activity_key):
    response = small_star_service.get_activity_sync(product_code, book_key)
    question_answer = jmespath.search("@[*].Questions[?Key=='{0}'].Body.answers[]".format(question_key), response)
    activity_type = get_activity_type(activity_key)

    def split(li: list, new_list=[]):
        for ele in li:
            if isinstance(ele, list):
                split(ele)
            else:
                new_list.append(ele)
        return new_list

    li = question_answer
    star = split(li)
    if activity_type == 'ssTracingWord':
        total_star = 1
    elif activity_type == 'dialogue':
        total_star = 1
    elif activity_type == 'reader':
        total_star = 1
    elif activity_type == 'readerLongText':
        total_star = 1
    elif activity_type == 'ssTracingLetter':
        total_star = 1
    else:
        total_star = len(star)
    return total_star


def submit_data(pass_perfect, lesson_keys):
    for lesson_key in lesson_keys:
        activity_keys = get_activity_keys(lesson_key)
        for activity_key in activity_keys:
            print(small_star_service.submit_small_star_student_answers(pass_perfect, activity_key, user_id, group_id))


def run(pass_perfect):
    lesson_keys = get_lesson_keys_by_unit_key()
    unlock_lesson_keys = get_unlock_lesson_keys()
    if lesson_keys[0] in unlock_lesson_keys:
        submit_data(pass_perfect, lesson_keys)
    elif unit_name == 'Unit 0':
        submit_data(pass_perfect, lesson_keys)
    else:
        print('This unit is not unlocked. Please use the unlock tool to unlock the unit first!')


if __name__ == '__main__':
    start = time.time()
    username = 'ss3.cn.02'  # login username
    password = '12345'  # login password
    book_name = 'Book 1'  # The book that needs to be executed
    unit_name = 'Unit 1'  # The unit that needs to be executed
    small_star_service = SmallStarService(Environment.STAGING)
    # Environment: QA / STAGING / STAGING_SG / LIVE / LIVE_SG

    small_star_service.login(username, password)
    response = small_star_service.get_student_profile().json()
    book_key = jmespath.search("CourseGroups[?Book.Name=='{}'].Book.Key".format(book_name), response)[0]
    product_code = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.ProductCode".format(book_key), response)[0]
    group_id = jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.OdinId".format(book_key), response)[0]
    user_id = jmespath.search('UserId', response)
    course_plan_key = \
        jmespath.search("CourseGroups[?Group.BookKey=='{}'].Group.CoursePlanKey".format(book_key), response)[0]
    #  No changes are needed

    run(pass_perfect=False)
    # pass_perfect = True   make all the activities correct
    # pass_perfect = False  make all the activities wrong

    end = time.time()
    print(end - start)
