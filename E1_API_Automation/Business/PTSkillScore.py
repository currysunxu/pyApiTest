from enum import Enum


class PTSkillScore:
    def __init__(self, skill_code, origin_score, overwrite_score, total_sore):
        self.skillCode = skill_code
        self.originScore = origin_score
        self.overwriteScore = overwrite_score
        self.totalScore = total_sore


class SkillCode(Enum):
    Grammar = 'Grammar'
    Listening = 'Listening'
    Reading = 'Reading'
    Vocabulary = 'Vocabulary'
    Speaking = 'Speaking'
    Writing = 'Writing'


class SubSkillCode(Enum):
    CommunicativeCompetence = 'CommunicativeCompetence'
    GrammaticalControl = 'GrammaticalControl'
    LexicalCommand = 'LexicalCommand'
    Punctuation = 'Punctuation'
