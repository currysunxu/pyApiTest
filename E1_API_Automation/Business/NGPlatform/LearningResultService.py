from E1_API_Automation.Business.BaseService import BaseService
from E1_API_Automation.Business.NGPlatform.NGPlatformUtils.LearningResultUtils import LearningResultUtils


class LearningResultService(BaseService):

    def post_learning_result_insert(self, learning_result):
        learning_result_insert_dict = LearningResultUtils.construct_learning_result_dict(learning_result)
        return self.mou_tai.post("/api/v1/results/", learning_result_insert_dict)

    def get_partition_result_without_limit(self, learning_result):
        api_url = '/api/v1/results/{0}/{1}'.format(learning_result.product, learning_result.student_key)
        return self.mou_tai.get(api_url)

    def get_partition_result_with_limit(self, learning_result, limit):
        if limit is None:
            limit = ''
        api_url = '/api/v1/results/{0}/{1}?limit={2}'.format(learning_result.product,
                                                             learning_result.student_key, limit)
        return self.mou_tai.get(api_url)

    def get_user_result_without_limit(self, learning_result):
        api_url = '/api/v1/results/{0}/{1}?productmodule={2}'.format(learning_result.product,
                                                                       learning_result.student_key,
                                                                       learning_result.product_module)
        return self.mou_tai.get(api_url)

    def get_user_result_with_limit(self, learning_result, limit):
        if limit is None:
            limit = ''

        api_url = '/api/v1/results/{0}/{1}?productmodule={2}&limit={3}'.format(learning_result.product,
                                                                                 learning_result.student_key,
                                                                                 learning_result.product_module,
                                                                                 limit)
        return self.mou_tai.get(api_url)

    def get_specific_result(self, learning_result):
        api_url = '/api/v1/results/{0}/{1}?productmodule={2}&businesskey={3}'.format(learning_result.product,
                                                                                         learning_result.student_key,
                                                                                         learning_result.product_module,
                                                                                         learning_result.business_key)
        return self.mou_tai.get(api_url)

    def post_learning_result_batch_insert(self, learning_result_list):
        learning_result_batch_insert = LearningResultUtils.construct_batch_learning_result_dict(learning_result_list)
        return self.mou_tai.post("/api/v1/results/batch", learning_result_batch_insert)
