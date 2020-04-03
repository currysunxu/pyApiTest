from ..Lib.Moutai import Moutai, Token


class PTViewerService:
    def __init__(self, host):
        self.host = host
        print(host)
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def student_by_batch(self, student_id):
        body = [student_id]
        return self.mou_tai.post('/api/v2/Student/ByBatch/', json=body)

    def progress_test_summary(self, progress_test_key, student_id):
        body = {"ProgressTestKey": progress_test_key,
                "StudentIdCollection": [student_id]}
        return self.mou_tai.post('/api/v2/ProgressTestSummary/Viewer/', json=body)


class HomeworkViewerService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host, token=Token("X-BA-TOKEN", "Token"))

    def homework_viewer_book_structure(self, book_key, region, course_plan_key):
        body = {
            "BookKey": book_key,
            "Region": region,
            "CoursePlanKey": course_plan_key
        }
        return self.mou_tai.post('/api/v2/HomeworkViewer/BookStructure', json=body)

    def homework_viewer_answers(self, student_ids, course_activity_keys):
        body = {
            "StudentIdCollection": [student_ids],
            "CourseActivityKeys": [course_activity_keys]
        }
        return self.mou_tai.post('/api/v2/HomeworkViewer/Answers', json=body)

    def homework_viewer_progress_info(self, student_ids, course_keys):
        body = {
            "StudentIdCollection": [student_ids],
            "CourseKeys": [course_keys]
        }
        return self.mou_tai.post('/api/v2/HomeworkViewer/ProgressInfo', json=body)