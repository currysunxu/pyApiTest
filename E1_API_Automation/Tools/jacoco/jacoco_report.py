import requests
from sys import argv


class JacocoReport:

    def __init__(self,service_name, host='http://jacoco-cmd.qa.edtech.kt'):
        self.host = host
        self.service_name = service_name

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, sdch"}

    def reset(self):
        param = {'serviceName': self.service_name}
        response = requests.post(url=self.host + '/api/reset', data=param, headers=self.headers)
        return response.content

    def dump(self, jaoco_path):
        param = {'serviceName': self.service_name,
                 'dataLocation': jaoco_path}
        response = requests.post(url=self.host + '/api/dumpdata', data=param, headers=self.headers)
        return response.content

    def generate_report(self, jaoco_path, report_dir, project_dir):
        param = {
            'dataLocation': jaoco_path,
            'projectDir': project_dir,
            'reportDir': report_dir
        }
        response = requests.post(url=self.host + '/api/generatereport', data=param, headers=self.headers)
        return response.content


if __name__ == '__main__':
    if len(argv) < 2:
        print('need input the parameters')
    else:
        service_name = argv[1]
        jacoco = JacocoReport(service_name)
        action =argv[2]
        if action =='dump':
            data_location = argv[3]
            response = jacoco.dump(data_location)
        elif action == 'report':

            data_location = argv[3]
            report_location = argv[4]
            project_location = argv[5]
            response = jacoco.generate_report(data_location, report_location, project_location)
        elif action == 'reset':
            response = jacoco.reset()
        print(response)


    # jacoco = JacocoReport('PlanService')
    # response = jacoco.reset()
    # response = jacoco.dump('/jacoco-data/learningplan/jacoco.exec')
    # response = jacoco.generate_report('/jacoco-data/learningplan/jacoco.exec','/jacoco-data/learningplan/coveragereport','/jacoco-data/learningplan/projectsource/platform-plan-svc')
