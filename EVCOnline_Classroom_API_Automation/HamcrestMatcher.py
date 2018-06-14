import jmespath
from hamcrest import assert_that
from hamcrest.core.base_matcher import BaseMatcher


class Matcher(BaseMatcher):
    def __init__(self, jemsPath):
        self.jems_path = jemsPath

    def _matches(self, item):
        if jmespath.search(self.jems_path, item):
            return True
        else:
            return False

    def describe_to(self, description):
        description.append_text("Can't find the expected value with jemspath: " + self.jems_path)


def match_to(obj):
    return Matcher(obj)


assert_that({"foo": [{"a": 1, "b": 2}, {"a": 2, "b": 2}]}, match_to("foo[0].b"))
