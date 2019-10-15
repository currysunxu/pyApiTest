
class ContentMapNodeEntity:
    def __init__(self, type, content_id, content_revision):
        self.__type = type
        self.__content_id = content_id
        self.__content_revision = content_revision
        self.__children = None
        self.__dynamic_field_one = None
        self.__dynamic_field_two = None

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def content_id(self):
        return self.__content_id

    @content_id.setter
    def content_id(self, content_id):
        self.__content_id = content_id

    @property
    def content_revision(self):
        return self.__content_revision

    @content_revision.setter
    def content_revision(self, content_revision):
        self.__content_revision = content_revision

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children

    @property
    def dynamic_field_one(self):
        return self.__dynamic_field_one

    @dynamic_field_one.setter
    def dynamic_field_one(self, dynamic_field_one):
        self.__dynamic_field_one = dynamic_field_one

    @property
    def dynamic_field_two(self):
        return self.__dynamic_field_two

    @dynamic_field_two.setter
    def dynamic_field_two(self, dynamic_field_two):
        self.__dynamic_field_two = dynamic_field_two
