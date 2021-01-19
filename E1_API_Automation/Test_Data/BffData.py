from enum import Enum

class BffProduct(Enum):
    HFV35 = 'HFV35'
    TBV3 = 'TBV3'
    SSV3 = 'SSV3'
    FRV1 = 'FRV1'
    HFV2 = 'HFV2'
    HFV3 = 'HFV3'


class BffUsers:
    BffUserPw = {
        'QA': {
            BffProduct.HFV35.value: [{'username': 'hf3.cn.02', 'password': '12345'}],
            BffProduct.TBV3.value: [{'username': 'tb3.cn.01', 'password': '12345'}],
            BffProduct.SSV3.value: [{'username': 'ss3.cn.01', 'password': '12345'}],
            BffProduct.FRV1.value: [{'username': 'fr.cn.02', 'password': '12345'}],
            BffProduct.HFV2.value: [{'username': 'hf2.cn.02', 'password': '12345'}],
            BffProduct.HFV3.value: [{'username': 'hf3.cn.01', 'password': '12345'}]
        },
        'Staging': {
            # Todo need to do data refactor once Staging is ready
            BffProduct.HFV35.value: [{'username': 'hf3.cn.02', 'password': '12345'}],
            BffProduct.TBV3.value: [{'username': 'tb3.cn.01', 'password': '12345'}],
            BffProduct.SSV3.value: [{'username': 'ss3.cn.01', 'password': '12345'}],
            BffProduct.FRV1.value: [{'username': 'fr.cn.01', 'password': '12345'}],
            BffProduct.HFV2.value: [{'username': 'hf2.cn.01', 'password': '12345'}]
        },
        'Live': {
            # Todo need to do data refactor once Staging is ready
            BffProduct.HFV35.value: [{'username': 'hf.test3', 'password': '12345', 'userid': 101548688}],
            BffProduct.TBV3.value: [{'username': 'tb3.cn.01', 'password': '12345'}],
            BffProduct.FRV1.value: [{'username': 'fr.cn.01', 'password': '12345'}],
            BffProduct.HFV2.value: [{'username': 'hf2.cn.01', 'password': '12345'}]
        }
    }


class HF35DependService:
    provisioning_service = {
        'QA': {
            'host': 'https://provisioning-qa.ef.cn',
            'ios-app-key': '6591032B-DF1F-405F-93B3-482371A99A13',
            'android-app-key': '43CF3DBD-FC07-4CE1-A319-F81D3BB17AAC'
        },
        'Staging': {
            'host': 'https://provisioning.ef.cn',
            'ios-app-key': 'a3362077-30d5-4941-af3c-730fc2d6fab7',
            'android-app-key': 'f6925fb9-0101-4fc9-8b6d-839f7045451b'
        },
        'Live': {
            'host': 'https://provisioning.ef.cn',
            'ios-app-key': 'd978ecfa-07c3-435f-9a88-ad5cdcc9c0f5',
            'android-app-key': 'b792a26f-e8a4-461d-9ae7-f82a2a5a6d51'
        }
    }

    ksd_internal_service = {
        'QA': {
            'host': 'https://internal-e1-evc-booking-qa-cn.ef.com'
        },
        'Staging': {
            'host': 'https://internal-e1-evc-booking-stg-cn.ef.com'
        },
        'Live': {
            'host': 'https://internal-e1-evc-booking-cn.ef.com'
        }
    }

    ups_service = {
        'QA': {
            'host': 'https://internal-e1-ups-privacy-stg.ef.cn'
        },
        'Staging': {
            'host': 'https://internal-e1-ups-privacy-stg.ef.cn'
        },
        'Live': {
            'host': 'https://internal-e1-ups-privacy.ef.cn'
        }
    }


class ExpectedData:
    expected_oc_context_qa = {
        "scope": "OSD",
        "ocConfig": {
            "webUrl": "https://study-online-staging.ef.cn/index.html?platform=webview",
            "svcDomain": "https://omni-apigateway-tc-staging.ef.cn",
            "getTechCheckTokenUrl": "/api/v3/Classroom/TechCheck",
            "getClassEntranceTokenUrl": "/api/v1/classroom/online/link"
        },
        "trackingConfig": {
            "evcTrackingDomain": "https://omni-apigateway-tc-staging.ef.cn",
            "visitorTrackingUrl": "/school/evclog/tracking/VisitorNonToken",
            "behaviorTrackingUrl": "/school/evclog/tracking/BehaviorNonToken",
            "classTrackingUrl": "/school/evclog/tracking/trackevcclass"
        },
        "evcConfig": {
            "webBootstrapUrl": "/evc15/meeting/api/bootstrap",
            "loggingUrl": "/evc15/meeting/api/log",
            "evcDomainMappings": {
                "EvcCN1": "https://evc-ts-qa.bj-englishtown.com",
                "EvcCN2": "https://evc-ts-qa.bj-englishtown.com",
                "EvcUS1": "https://qa-evc.ef.com"
            }
        },
        "staticResource": {
            "resourceCdnDomain": "https://evc-fe-qa.bj-englishtown.com",
            "webResourceVersionUrl": "/_shared/evc15-fe-android-bundle_kids/version.json",
            "agoraWebResourceVersionUrl": "/evc15/meeting/api/clientversion?platform=android",
            "agoraResourceCdnDomain": "https://evc-fe-qa.bj-englishtown.com"
        }
    }

    expected_oc_context_stg = {
        "scope": "OSD",
        "ocConfig": {
            "webUrl": "https://study-online-staging.ef.cn/index.html?platform=webview",
            "svcDomain": "https://omni-apigateway-tc-staging.ef.cn",
            "getTechCheckTokenUrl": "/api/v3/Classroom/TechCheck",
            "getClassEntranceTokenUrl": "/api/v1/classroom/online/link"
        },
        "trackingConfig": {
            "evcTrackingDomain": "https://omni-apigateway-tc-staging.ef.cn",
            "visitorTrackingUrl": "/school/evclog/tracking/VisitorNonToken",
            "behaviorTrackingUrl": "/school/evclog/tracking/BehaviorNonToken",
            "classTrackingUrl": "/school/evclog/tracking/trackevcclass"
        },
        "evcConfig": {
            "webBootstrapUrl": "/evc15/meeting/api/bootstrap",
            "loggingUrl": "/evc15/meeting/api/log",
            "evcDomainMappings": {
                "EvcCN2": "https://evc-ts-staging.ef.com.cn",
                "EvcCN1": "https://evc-ts-staging.ef.com.cn",
                "EvcUS1": "https://qa-evc.ef.com"
            }
        },
        "staticResource": {
            "resourceCdnDomain": "https://evc-fe-staging.bj-englishtown.com",
            "agoraWebResourceVersionUrl": "/evc15/meeting/api/clientversion?platform=ios",
            "webResourceVersionUrl": "/_shared/evc15-fe-ios-bundle_kids/version.json",
            "agoraResourceCdnDomain": "https://evc-fe-staging.bj-englishtown.com"
        }
    }

    expected_oc_context = {
        'QA': expected_oc_context_qa,
        'Staging': expected_oc_context_stg,
        'Live': {
            "scope": "OSD",
            "ocConfig": {
                "webUrl": "https://study-online.ef.cn/index.html?platform=webview",
                "svcDomain": "https://omni-apigateway-tc.ef.cn",
                "getTechCheckTokenUrl": "/api/v3/Classroom/TechCheck",
                "getClassEntranceTokenUrl": "/api/v1/classroom/online/link"
            },
            "trackingConfig": {
                "evcTrackingDomain": "https://omni-apigateway-tc.ef.cn",
                "visitorTrackingUrl": "/school/evclog/tracking/VisitorNonToken",
                "behaviorTrackingUrl": "/school/evclog/tracking/BehaviorNonToken",
                "classTrackingUrl": "/school/evclog/tracking/trackevcclass"
            },
            "evcConfig": {
                "webBootstrapUrl": "/evc15/meeting/api/bootstrap",
                "loggingUrl": "/evc15/meeting/api/log",
                "evcDomainMappings": {
                    "EvcCN1": "https://evc-ts.ef.com.cn",
                    "EvcCN2": "https://evc-ts.ef.com.cn",
                    "EvcUS1": "https://evc.ef.com"
                }
            },
            "staticResource": {
                "resourceCdnDomain": "https://evc-fe.bj-englishtown.com",
                "webResourceVersionUrl": "/_shared/evc15-fe-ios-bundle_kids/version.json",
                "agoraWebResourceVersionUrl": "/evc15/meeting/api/clientversion?platform=ios",
                "agoraResourceCdnDomain": "https://evc-fe.bj-englishtown.com"
            }
        }
    }


class BffSQLString:
    get_study_plan_by_student_id_sql = {
        'QA': "SELECT * FROM study_plan_qa.study_plan WHERE student_id = '{0}' and product_module = '{1}' and ref_content_path = '{2}'",
        'Staging': "SELECT * FROM study_plan_stg.study_plan WHERE student_id = '{0}' and product_module = '{1}' and ref_content_path = '{2}'",
        'Live': ""
    }

    get_count_study_plan_by_student_id_sql = {
        'QA': "SELECT count(*) FROM study_plan_qa.study_plan WHERE student_id = '{0}' and product_module = '{1}' and ref_content_path = '{2}'",
        'Staging': "SELECT count(*) FROM study_plan_stg.study_plan WHERE student_id = '{0}' and product_module = '{1}' and ref_content_path = '{2}'",
        'Live': ""
    }

    get_count_completed_study_plan_by_student_id_content_path_sql = {
        'QA': "SELECT count(*) FROM study_plan_qa.study_plan WHERE student_id = '{0}'and ref_content_path = '{1}' AND complete_at IS NOT NULL",
        'Staging': "SELECT count(*) FROM study_plan_stg.study_plan WHERE student_id = '{0}'and ref_content_path = '{1}' AND complete_at IS NOT NULL",
        'Live': ""
    }
