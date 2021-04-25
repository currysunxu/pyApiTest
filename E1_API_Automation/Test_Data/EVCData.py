import os

EVC_AGORA_FRONTEND_VERSION = os.environ['agora_fe_version']
EVC_FM_FRONTEND_VERSION = os.environ['fm_fe_version']
EVC_TECH_CHECK_VERSION = os.environ['techcheck_version']
EVC_INDO_DEMO_VERSION = os.environ['indo_demo_version']


# EVC_AGORA_FRONTEND_VERSION = "0.3.7-734fc77"
# EVC_FM_FRONTEND_VERSION = "0.1.39-bfed4c1"
# EVC_TECH_CHECK_VERSION = "0.2.3-f1e6b90"
# EVC_INDO_DEMO_VERSION = "0.1.0-05a01fa"

class EVCContentMaterialType:
    FM_Kids_PL = "kids_pl"
    Agora_Kids_PL = "kids_pl2"


class EVCLayoutCode:
    FM_Kids_PL = "kids_pl"
    Agora_Kids_PL = "kids_pl_v2"


class EVCMeetingRole:
    TEACHER = "host"
    STUDENT = "participant"


class EVCPlatform:
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"
