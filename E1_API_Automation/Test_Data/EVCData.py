import os

EVC_AGORA_FRONTEND_VERSION = os.environ['agora_fe_version']
EVC_FM_FRONTEND_VERSION = os.environ['fm_fe_version']


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
