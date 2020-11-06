from enum import Enum


class StoryBlokVersion(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'


class StoryblokReleaseProgram(Enum):
    READERS = 'Readers'
    VOCABULARIES = 'Vocabularies'
    HIGHFLYERS = 'Highflyers'


class StoryBlokData:
    StoryBlokService = {
        'host': 'https://app.storyblokchina.cn'
    }

    StoryBlokAPIKey = {
        'QA': '29I3YNawIfQdKvVpoM6wJAtt',
        'Staging': 'yFrA18ZTbgK3VkHv0pyk9gtt',
        'Live': '3dm4HVQWmuA7ASgkKixgYQtt'
    }

    StoryBlokEnv = {
        'Oneapp': '187',
        'Dev': '215'
    }