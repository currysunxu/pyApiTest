from E1_API_Automation.Business.BaseService import BaseService


class UpsPrivacyService(BaseService):

    def get_privacy_policy_document(self, product_id, region_code):
        return self.mou_tai.get('/api/v1/privacy-policy-documents?productId={0}&regionCode={1}'.format(product_id,
                                                                                                       region_code))

    def get_privacy_policy_agreement(self, student_id, product_id, region_code):
        return self.mou_tai.get('/api/v1/privacy-policy-agreements?studentId={0}&productId={1}&regionCode={2}'
                                .format(student_id, product_id, region_code))

    def get_privacy_policy_document_hf35(self):
        # currently, only provide api for CN, will change until code implementation changed
        return self.get_privacy_policy_document(4, 'CN')

    def get_privacy_policy_agreement_hf35(self, student_id):
        # currently, only provide api for CN, will change until code implementation changed
        return self.get_privacy_policy_agreement(student_id, 4, 'CN')