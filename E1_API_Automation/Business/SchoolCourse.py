import jmespath
import arrow

from E1_API_Automation.Business.template.create_acitivty import Activity


class CourseBook:
    def __init__(self, session, product_code, book_key, course_plan_key):
        self.product_code = product_code
        self.session = session
        self.book_key = book_key
        self.course_plan_key = course_plan_key
        self.content_nodes = self.__get_book_content(book_key, course_plan_key)

    def get_child_nodes_by_parent_key(self, parent_key):
        child_nodes = jmespath.search("@[?ParentNodeKey=='{0}']".format(parent_key), self.content_nodes)
        return child_nodes

    def get_activity_json_by_activity_key(self, activity_keys):
        detail_json = self.session.post("/api/v2/ActivityEntity/Web", json=activity_keys).json()
        return jmespath.search("Activities", detail_json)

    def __get_book_content(self, book_key, course_plan_key):
        body = {"BookKey": book_key,
                "CoursePlanKey": course_plan_key,
                "ProductCode": self.product_code,
                "LastSynchronizedStamp": None,
                "LastSynchronizedKey": None,
                "UpsertsOnly": False,
                "Amount": 1000
                }

        response = self.session.post("/api/v2/CourseNode/Synchronize", json=body)
        return jmespath.search("Upserts", response.json())

    def get_activity_nodes(self):
        return jmespath.search("@[?Level ==`16`]", self.content_nodes)

    def get_activity_keys(self, node_list=None):
        if node_list:
            return jmespath.search("@[*].ActivityKeys[0]", node_list)
        else:
            activity_nodes = jmespath.search("@[?Level ==`16`]", self.content_nodes)
            return jmespath.search("@[*].ActivityKeys[0]", activity_nodes)

    def get_activity_course_keys(self, node_list=None):
        if node_list:
            return jmespath.search("@[*].Key", node_list)
        else:
            activity_nodes = jmespath.search("@[?Level ==`16`]", self.content_nodes)
            return jmespath.search("@[*].Key", activity_nodes)

    def get_lesson_nodes(self):
        return jmespath.search("Upserts[?Level ==`8`]", self.content_nodes)

    def get_unit_nodes(self):

        return jmespath.search("Upserts[?Level ==`4`]", self.content_nodes)

    def generate_lesson_submit_answer(self, lesson_key, group_id, pass_lesson):
        activities_nodes = self.get_child_nodes_by_parent_key(lesson_key.lower())
        activity_keys = self.get_activity_keys(activities_nodes)
        detail_activity = self.get_activity_json_by_activity_key(activity_keys)
        submit_data = {"GroupId": group_id, "LessonKey": lesson_key}
        activity_answers = []
        for activity_json in detail_activity:
            activity = Activity().create_activity(activity_json)
            answers = [self.set_question_anwser(pass_lesson, activity.get_question_score(question), question) for
                       question
                       in activity.question_key_list]
            activity_answer = self.set_activity_answer(activity, answers, activities_nodes)
            activity_answers.append(activity_answer)

        submit_data["ActivityAnswers"] = activity_answers
        return submit_data

    def set_activity_answer(self, activity, answers, lesson_activities):
        activity_answer = {"Answers": answers, "CompletedQuestionCount": None,
                           "correctQuestionCount": activity.total_question_count,
                           "TotalQuestionCount": None,
                           "ActivityKey": activity.key,
                           "ActivityCourseKey":
                               jmespath.search("@[?ActivityKeys[0]=='{0}'].Key".format(activity.key),
                                               lesson_activities)[0]}
        return activity_answer

    def set_question_anwser(self, pass_lesson, total_score, question_key, total_star = None):
        question_answer = {"Attempts": None,
                           "Detail": {"modelData": None},
                           "Duration": 1.3,
                           "Key": None}
        if pass_lesson:
            question_answer["Score"] = total_score
            if self.product_code == 'SS':
                question_answer["Star"] = total_star
            else:
                question_answer["Star"] = None
        else:
            question_answer["Score"] = 0
            question_answer["Star"] = None
        question_answer["TotalScore"] = total_score

        question_answer["TotalStar"] = total_star
        question_answer["LocalStartStamp"] = None
        question_answer["LocalEndStamp"] = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssZZ')
        question_answer["QuestionKey"] = question_key
        return question_answer

    def generate_activity_submit_answer(self, activity_course_key_node, pass_activity):
        activity_key = self.get_activity_keys([activity_course_key_node])
        activity_course_key = self.get_activity_course_keys([activity_course_key_node])
        activity_json = self.get_activity_json_by_activity_key(activity_key)
        activity = Activity().create_activity(activity_json[0])
        submit_data = { "ActivityCourseKey": activity_course_key[0],"ActivityKey": activity.key}
        answers = [self.set_question_anwser(pass_activity, activity.get_question_score(question), question, activity.get_question_score(question)) for
                   question
                   in activity.question_key_list]
        submit_data["Answers"] = answers
        return submit_data
