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