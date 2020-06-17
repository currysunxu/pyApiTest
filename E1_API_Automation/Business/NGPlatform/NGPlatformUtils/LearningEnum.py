from enum import Enum


class LearningPlanAPIType(Enum):
    TypeInsert = 'InsertAPI'
    TypeBatchInsert = 'BatchInsertAPI'
    TypeUpdate = 'UpdateAPI'


class LearningResultProduct(Enum):
    SMALLSTAR = 1
    HIGHFLYER = 2
    TRAILBLAZERS = 4
    FRONTRUNNER = 8
    GRAMMARPRO = 16
    MOCKTEST = 32
    REMEDIATION = 64


class LearningResultProductModule(Enum):
    HOMEWORK = 1
    QUIZ = 2
    PRACTICE = 4
    DIAGNOSTICTEST = 8
    PROGRESSTEST = 16
    MOCKTEST = 32
    REMEDIATION = 64
    VOCABULARY = 128