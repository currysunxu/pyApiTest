from enum import Enum


class StoryBlokVersion(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'


class StoryblokReleaseProgram(Enum):
    READERS = 'Readers'
    VOCABULARIES = 'Vocabularies'
    HIGHFLYERS_35 = 'Highflyers35'
    MOCKTEST = 'MockTest'
    HIGHFLYERS = 'Highflyers'
    SMALLSTARS_30 = 'Smallstars30'
    SMALLSTARS_35 = 'Smallstars35'
    TRAILBLAZERS_30 = 'Trailblazers30'


class StoryBlokData:
    StoryBlokService = {
        'host': 'https://app.storyblokchina.cn'
    }

    StoryBlokEnvInfo = {
        'Oneapp': {
            'space': '187',
            'token': {
                'QA': '29I3YNawIfQdKvVpoM6wJAtt',
                'Staging': 'yFrA18ZTbgK3VkHv0pyk9gtt',
                'Live': '3dm4HVQWmuA7ASgkKixgYQtt'
            }
        },
        'Dev': {
            'space': '215',
            'token': {
                'QA': 'KjpKJ2NRB6DRPFaMAzrXxAtt'
            }
        },
        'MT': {
            # 'space': '222',
            # 'token': {
            #     'QA': '9wmr7bICxBjVnB5PZ8i38wtt',
            #     'Staging': 'M0TdPuAXkTkSzelnaU8wJwtt',
            #     'Live': 'HdhWXGOS4YriIqAN49KtEQtt'
            # }
            'space': '215',
            'token': {
                'QA': 'KjpKJ2NRB6DRPFaMAzrXxAtt',
                'Staging': 'M0TdPuAXkTkSzelnaU8wJwtt',
                'Live': 'HdhWXGOS4YriIqAN49KtEQtt'
            }
        },
        'TestingOfOneapp': {
            'space': '225',
            'token': {
                'QA': 'AioSrTnsyHPf767iIefweAtt'
            }
        }
    }

    StoryBlokProgram = {
        # key need to consistent with the StoryblokReleaseProgram enum value
        'Highflyers35': {
            'source-name': 'highflyers',
            'target-name': 'HIGH_FLYERS_35',
            'course-config-path': 'Highflyers/course-config'
        },
        'Smallstars30': {
            'source-name': 'smallstar',
            'target-name': 'SMALL_STARS_30',
            'course-config-path': 'Smallstars/course-config'
        },
        'Smallstars35': {
            'source-name': 'small-stars-3-5',
            'target-name': 'SMALL_STARS_35',
            'course-config-path': 'Smallstars/course-config'
        },
        'Trailblazers30': {
            'source-name': 'tb16',
            'target-name': 'TRAILBLAZERS_30',
            'course-config-path': 'Trailblazers/course-config'
        }
    }

class MockTestData:
    MockTest = {
        'ResourceHost': 'https://mt-content-qa.s3.cn-north-1.amazonaws.com.cn/',
        'ActivityInitVersion': 2000
    }


class MTTableSQLString:
    # if the activity already been saved to storyblok, it will not be processed again,
    # so, skip those data with version larger than init version and less than the current version
    get_valid_activity_sql = "SELECT * FROM {0} where is_deleted = 0 and version >= {1} " \
                             "   and (id,version) " \
                             "       in ( select id, max(version) from {0} where is_deleted = 0 group by id)" \
                             "   and id not in " \
                             "          (select id from {0} where is_deleted = 0 and version < {1} and version >={2})"

    get_activity_by_uuid_sql = "SELECT * FROM {0} where uuid = '{1}'"