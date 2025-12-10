from enum import Enum


class TimesheetBaseEnum(Enum):
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)


class Tasktype(TimesheetBaseEnum):
    Development_New_Feature = 1
    Development_Maintanace = 5
    Development_Bug_Fixes = 6
    Meeting_Internal = 8
    Requirement = 11
    Review_Code_Design = 12
    Training_learning = 13

    @property
    def task_type(self):
        return self.value
