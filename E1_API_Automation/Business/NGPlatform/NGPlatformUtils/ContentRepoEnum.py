from enum import Enum


class ContentRepoGroupType(Enum):
    TypeActivityGroup = 'ACTIVITY_GROUP'
    TypeECAGroup = 'ECA_GROUP'
    TypeAssetGroup = 'ASSET_GROUP'


class ContentRepoContentType(Enum):
    TypeHomework = 'HOMEWORK'
    TypeHandout = 'HANDOUT'
    TypeVocab = 'VOCAB'
