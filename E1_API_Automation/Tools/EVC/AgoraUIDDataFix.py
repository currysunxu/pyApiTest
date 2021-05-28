import concurrent.futures
from datetime import datetime
from multiprocessing.dummy import Pool

import requests
from hamcrest import assert_that, equal_to


# platform_service = EVCPlatformMeetingService("https://evc-ts-staging.kids.ef.cn")


def meeting_agora_uid_data_fix(meeting_token):
    url = 'https://evc-ts-staging.kids.ef.cn' + "/evc15/meeting/api/agorauiddatafix?meetingToken={0}".format(
        meeting_token)
    print("\n", url, "\n")
    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-accesskey': '414d95a5-b338-4356-adac-eacce520b114'
    }
    print("\n", datetime.now(), "\n")
    response = requests.request("POST", url, headers=headers, data=payload)
    assert_that(response.status_code, equal_to(200))
    print("\n", datetime.now(), "\n")
    return response


if __name__ == "__main__":
    # # mock_omni_class_booking(EVCLayoutCode.Indo_FR_GL, 9)
    # # time.sleep(class_duration * 60 - 160)
    # # for i in range(10):
    # meeting_token_list = ['f7f0cabb-3011-46e8-858d-0a204f05068a', '4f3abffe-e891-4ee2-ac20-6f8ddcbd5c7e',
    #                       '61cdeb71-b33b-4b08-bcdd-ad4bfca739a4']
    #
    # # meeting_token_list = ['bb72b470-829e-446f-9c05-f983bb606526','cb75aaa9-b6d0-4928-9897-87ecd9e395d6',
    # #                         'c6680776-7b4a-44aa-ba48-90476a910445']
    #
    # # meeting_token_list = ['4f3abffe-e891-4ee2-ac20-6f8ddcbd5c7e']
    #
    # # platform_service.meeting_agora_uid_data_fix(meeting_token_list[1])
    #
    # for i in meeting_token_list:
    #     # print(i)
    #     platform_service.meeting_agora_uid_data_fix(i)
    #     # sleep(1)

    pool = Pool(30)
    futures = []
    meeting_token_list = ['f7f0cabb-3011-46e8-858d-0a204f05068a', '4f3abffe-e891-4ee2-ac20-6f8ddcbd5c7e',
                          '61cdeb71-b33b-4b08-bcdd-ad4bfca739a4']
    # for i in range(30):
    #     token = meeting_token_list[i % 3]
    #     futures.append(pool.apply_async(meeting_agora_uid_data_fix, [token]))
    # for future in futures:
    #     print(future.get())

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        fus = [executor.submit(meeting_agora_uid_data_fix, meeting_token_list[i % 3]) for i in range(100)]
        for fu in concurrent.futures.as_completed(fus):
            try:
                data = fu.result()
            except Exception as exc:
                print(exc)
            else:
                print(data)
