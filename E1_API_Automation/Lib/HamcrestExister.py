import jmespath
from hamcrest import assert_that
from hamcrest.core.base_matcher import BaseMatcher


class Exist(BaseMatcher):
    def __init__(self, jemsPath):
        self.jems_path = jemsPath

    def _matches(self, item):
        j = item
        key_path = self.jems_path.split('.')
        for key in key_path:
            flag, result = check_key(j, key)
            if flag:
                j = result
            else:
                return False
        print(result)
        return flag

    def describe_to(self, description):
        description.append_text("Can't find the expected value with jemspath: " + self.jems_path)

def check_key(jdict, key):
    if isinstance(jdict, list):
        for ele in jdict:
            flag, result = check_key(ele, key)
            if flag:
                break
    elif isinstance(jdict, dict):
        if key in jdict.keys():
            if jdict[key]:
                return (True, jdict[key])
            else:
                return(True, "None value")
        else:
            return (False, None)

def exist(obj):
    return Exist(obj)

assert_that({"foo": {"a": None, "b": 2}}, exist("foo.b"))