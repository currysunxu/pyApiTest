class EducationRegion:
    cn_city_list = {'Shanghai': '61AEF09D-AFA0-4FC2-96AD-93C72D390653',
                    'Beijing': '8EF7CCD2-8C58-4BC6-8A35-B3FCAE4D0F0D',
                    'Shenzhen': '568CD462-C9D5-48FD-84E8-FE07CAE65EBC',
                    'Foshan': '3120FADB-9800-4394-B272-9F658F7CEA55',
                    'Guangzhou': '163B7979-6413-4194-892D-51726D8EFDE5',
                    'Fuzhou': '22777B07-1296-4F5A-81FA-D14100EF2FE4',
                    }

    ru_city_list = {'Moscow': '045E22BB-E9AB-4BB8-A4FA-F59A7C0A8CDC',
                    'Petersburg': '4A4B9945-D1C8-4A0F-BE69-6965DB61B230',
                    'Novosibirsk': '5E5461C4-5DF4-4E9D-92F6-BC080CEC105D'}

    id_city_list = {'Jakarta': '872DECDC-4969-E811-8149-02BC62143FC0'}


class ShanghaiGradeKey:
    Gth2 = ['2th', '593f86f2-1e21-48bb-ac12-0d1dfba071c8']
    Gth3 = ['3rd', 'e8fee4e0-c180-4e07-b37a-cf91d12df2b4']
    Gth4 = ['4th', '0d05b8bc-62f5-422a-a196-719fe8ab4483']
    Gth5 = ['5th', '9459e5bb-1449-4432-b4b6-84c964959b24']
    Gth6 = ['6th', '7e1025c7-8ea5-4942-ab6b-249d01cb844f']
    Gth7 = ['7th', 'a668a326-a716-4fa5-a2f6-7b1c54712766']
    Gth8 = ['8th', '5da62ca5-f332-419e-b3db-111da15635bd']
    Gth9 = ['9th', '3d5b9a07-f9f5-4ad5-b5a9-e4d383220fed']
    Gth10 = ['10th', '0f9f5634-d6f4-4428-ab02-7bb81f3c289a']
    Gth11 = ['11th', '5760982d-77bc-42d4-8998-0c072e30a9e6']
    Gth12 = ['12th', 'd3a5cd6d-b791-476c-b77c-6c8aa9c85c52']


class MoscowGradeKey:
    Gth3 = ['3rd', 'B5F3E62D-EA22-4FD4-917D-372C36FAE402']
    Gth4 = ['4th', 'C1E850AB-4E96-467C-8396-10F3FB67E749']
    Gth5 = ['5th', 'FB3E9A46-9E0D-40DA-8B5E-BC66CF97065F']
    Gth6 = ['6th', 'A8C8ACAE-8B73-E811-8149-02BC62143FC0']
    Gth7 = ['7th', '1BE0A30D-DC21-43F8-BBD0-41431902EBD5']
    Gth8 = ['8th', '030D33CB-C32D-4490-A141-077A9604773D']
    Gth9 = ['9th', 'CC16DD0A-E034-47C4-ADB2-F79C82DA18AF']
    Gth10 = ['10th', '6B155F3A-AEC5-4856-B750-5E263E1C63CD']


class GP_user:
    GPUsers = {'QA': {'username': 'gpauto', 'password': '12345', 'culture_code': 'zh-CN'},
               'Staging': {'username': 'gp.cn.auto1', 'password': '12345', 'culture_code': 'zh-CN'},
               'Live': {'username': 'gp.cn.auto1', 'password': '12345', 'culture_code': 'zh-CN'},
               'Staging_SG': {'username': 'gp.id.auto1', 'password': '12345', 'culture_code': 'id-ID'},
               'Live_SG': {'username': 'gp.id.auto1', 'password': '12345', 'culture_code': 'id-ID'}}
    GPDTUsers = {'QA': {'username': 'gp02', 'password': '12345', 'culture_code': 'zh-CN'},
                 'Staging': {'username': 'gp.cn.auto1', 'password': '12345', 'culture_code': 'zh-CN'},
                 'Live': {'username': 'gp.cn.auto2', 'password': '12345', 'culture_code': 'zh-CN'},
                 'Staging_SG': {'username': 'gp.ru.auto1', 'password': '12345', 'culture_code': 'ru-RU'},
                 'Live_SG': {'username': 'gp.ru.auto1', 'password': '12345', 'culture_code': 'ru-RU'}}

    GradeList = {'QA': {'lowest_grade': 'Gth2', 'highest_grade': 'Gth12'},
                 'Staging': {'lowest_grade': 'Gth3', 'highest_grade': 'Gth11'},
                 'Live': {'lowest_grade': 'Gth3', 'highest_grade': 'Gth11'},
                 'Staging_SG': {'lowest_grade': 'Gth3', 'highest_grade': 'Gth10'},
                 'Live_SG': {'lowest_grade': 'Gth3', 'highest_grade': 'Gth10'}}
