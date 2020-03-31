from ..Lib.Moutai import Moutai


class E1TPIService:
    def __init__(self, host):
        self.host = host
        print(host)
        self.mou_tai = Moutai(host=self.host)

    def get_pt_viewer_link(self, pt_viewer_data):
        return self.mou_tai.post("/ptviewer/getptviewerlink?userId={userId}&students={studentsId}&ptPrimaryKey={ptPrimaryKey}".format(**pt_viewer_data))