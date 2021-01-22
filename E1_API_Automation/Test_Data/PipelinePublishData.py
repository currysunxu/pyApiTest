from E1_API_Automation.Test_Data.StoryblokData import StoryBlokData


class AEMData:
    AEMHost = {
        'STG': 'https://internal-aem-publisher-staging.ef.cn',
        'LIVE': 'https://internal-aem-publisher.ef.cn'
    }

    CSEMediaService = {
        'QA': {
            'host': 'https://cc3uu1njth.execute-api.cn-north-1.amazonaws.com.cn/qa/',
            'x-api-key': 'x0Ay2BPfQLritFvgxc06seZLUYGOzJkTvhyWBAfY'
        },
        'Staging': {
            'host': 'https://6asc6253pj.execute-api.cn-north-1.amazonaws.com.cn/prod/',
            'x-api-key': 'hUbfPBmQ82DmrhUnqgtrRPMEpVQuVgANXBpCyh4v'
        },
        'Staging_SG': {
            'host': 'https://xhytg03fpa.execute-api.ap-southeast-1.amazonaws.com/prod/',
            'x-api-key': 'MQbsQH6Mp4hc9gsEipQjWIKJsVU9EKOCwHvUIsy5'
        },
        'Live': {
            'host': 'https://6asc6253pj.execute-api.cn-north-1.amazonaws.com.cn/prod/',
            'x-api-key': 'hUbfPBmQ82DmrhUnqgtrRPMEpVQuVgANXBpCyh4v'
        }
    }

    # course data is same as StoryBlokData.StoryBlokProgram, it will config with both course name in AEM(source-name) and content_map(target-name)
    CourseData = StoryBlokData.StoryBlokProgram
