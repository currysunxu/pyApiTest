from ptest.test_filter import TestFilter
from ptest.config import get_list_property


class Filter(TestFilter):
    def filter(self, test_ref):
        return hasattr(test_ref, "__tags__") and all(elem in test_ref.__tags__ for elem in get_list_property("tags"))