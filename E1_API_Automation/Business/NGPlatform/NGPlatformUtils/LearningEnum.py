from enum import Enum


class LearningPlanAPIType(Enum):
    TypeInsert = 'InsertAPI'
    TypeBatchInsert = 'BatchInsertAPI'
    TypeUpdate = 'UpdateAPI'
