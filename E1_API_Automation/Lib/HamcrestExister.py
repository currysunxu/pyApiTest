import jmespath
from hamcrest import assert_that
from hamcrest.core.base_matcher import BaseMatcher


class Exist(BaseMatcher):
    def __init__(self, jemsPath):
        self.jems_path = jemsPath

    def _matches(self, item):
        if len(self.jems_path.split('.')) > 1:
            last_key = self.jems_path.split('.')[-1]
            contains_key = self.jems_path[:self.jems_path.rindex('.')]
            search_value = "contains(keys(%s),'%s')" % (contains_key, last_key)
        else:
            search_value = "contains(keys(@),'%s')" % self.jems_path

        return jmespath.search(search_value, item)

    def describe_to(self, description):
        description.append_text("Can't find the expected value with jemspath: " + self.jems_path)


def exist(obj):
    return Exist(obj)


assert_that({"foo": {"a": None, "c": 2}, "b": None}, exist("foo.a"))
