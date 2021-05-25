import os

EVC_AGORA_FRONTEND_VERSION = os.environ['agora_fe_version']
EVC_FM_FRONTEND_VERSION = os.environ['fm_fe_version']
EVC_TECH_CHECK_VERSION = os.environ['techcheck_version']
EVC_INDO_DEMO_VERSION = os.environ['indo_demo_version']


# EVC_AGORA_FRONTEND_VERSION = "0.3.9-cdac249"
# EVC_FM_FRONTEND_VERSION = "0.1.39-bfed4c1"
# EVC_TECH_CHECK_VERSION = "0.2.3-f14927a"
# EVC_INDO_DEMO_VERSION = "0.1.0-05a01fa"


class EVCContentMaterialType:
    FM_Kids_PL = "kids_pl"
    Agora_Kids_PL = "kids_pl2"


class EVCLayoutCode:
    CN_HF_PL = "cn_hf_pl"
    CN_SS_PL = "cn_ss_pl"
    CN_TB_PL = "cn_tb_pl"
    Kids_PL = "kids_pl"
    Indo_FR_GL = "indo_fr_gl"
    Indo_HF_GL = "indo_hf_gl"
    Indo_SS_GL = "indo_ss_gl"
    Indo_TB_GL = "indo_tb_gl"
    Indo_Phonics_GL = "indo_phonics_gl"
    Indo_Story_Teller_GL = "indo_storytellers_gl"
    Indo_Speak_Up_GL = "indo_speakup_gl"


class EVCMeetingRole:
    TEACHER = "host"
    STUDENT = "participant"


class EVCPlatform:
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"

class EVCMediaType:
    AGORA = "agora"
    FM = "IceLink"
    TRTC = "trtc"


class EVCComponentType:
    MEETING = 'meeting'
    MEDIA = 'media'
    WHITEBOARD = 'whiteboard'
    CHAT = 'chat'
    NOTE = 'note'


class EVCProxyLocation:
    CN = "CN"
    SG = "SG"
    UK = "UK"
    US = "US"


class EVCCenterCode:
    CN = "S"
    SG = "SG"
    UK = "UK"
    US = "US"
