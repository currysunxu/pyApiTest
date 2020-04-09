from ..Lib.Moutai import Moutai


class KSDInternalService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    def get_ksd_oc_context(self, student_id, platform):
        return self.mou_tai.get('/internal/api/v2/oc-context?studentId={0}&platform={1}'.format(student_id, platform))
