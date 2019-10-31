
class ContentMapQueryEntity:
    def __init__(self, course_name, schema_version, child_types=None, content_id=None, region_ach=None, tree_revision=None):
        self.__course_name = course_name
        self.__schema_version = schema_version
        self.__child_types = child_types
        self.__content_id = content_id
        self.__region_ach = region_ach
        self.__tree_revision = tree_revision

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, course_name):
        self.__course_name = course_name

    @property
    def schema_version(self):
        return self.__schema_version

    @schema_version.setter
    def schema_version(self, schema_version):
        self.__schema_version = schema_version

    @property
    def child_types(self):
        return self.__child_types

    @child_types.setter
    def child_types(self, child_types):
        self.__child_types = child_types

    @property
    def content_id(self):
        return self.__content_id

    @content_id.setter
    def content_id(self, content_id):
        self.__content_id = content_id

    @property
    def region_ach(self):
        return self.__region_ach

    @region_ach.setter
    def region_ach(self, region_ach):
        self.__region_ach = region_ach

    @property
    def tree_revision(self):
        return self.__tree_revision

    @tree_revision.setter
    def tree_revision(self, tree_revision):
        self.__tree_revision = tree_revision
