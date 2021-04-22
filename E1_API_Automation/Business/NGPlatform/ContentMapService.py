from E1_API_Automation.Lib.Moutai import Moutai


class ContentMapService:
    def __init__(self, host):
        self.host = host
        self.mou_tai = Moutai(host=self.host)

    # query content map, call by other methods
    def post_content_map_query(self, content_map_query_entity, is_by_tree):
        query_body = {
            "childTypes": content_map_query_entity.child_types,
            "contentId": content_map_query_entity.content_id,
            "regionAch": content_map_query_entity.region_ach,
            "treeRevision": content_map_query_entity.tree_revision
        }

        self.mou_tai.headers['X-Schema-Version'] = content_map_query_entity.schema_version
        api_url = "/api/v1/courses/{0}".format(content_map_query_entity.course_name)
        if is_by_tree:
            api_url = api_url + "/tree"
        else:
            api_url = api_url + "/flat"
        api_response = self.mou_tai.post(api_url, query_body)
        # remove the X-Schema-Version as other API may not need this.
        del self.mou_tai.headers['X-Schema-Version']
        return api_response

    # query by tree
    def post_content_map_query_tree(self, content_map_query_entity):
        return self.post_content_map_query(content_map_query_entity, True)

    # query by flat
    def post_content_map_query_flat(self, content_map_query_entity):
        return self.post_content_map_query(content_map_query_entity, False)

    # activate a tree by tree_revision
    def put_activate_content_map_by_revision(self, tree_revision):
        api_url = "/admin/api/v1/trees/{0}/activations".format(tree_revision)
        return self.mou_tai.put(api_url)

    def post_insert_content_map_tree(self, course, tree_data, schema_version, region_ach):
        insert_body = {
            "course": course,
            "data": tree_data,
            "schemaVersion": schema_version,
            "regionAch": region_ach
        }
        return self.mou_tai.post("/admin/api/v1/trees/", insert_body)

    def get_content_map_course_node(self, content_path):
        api_url = '/api/v2/course-nodes?contentPath={0}&traverse=WITH_ANCESTORS'.format(content_path)
        return self.mou_tai.get(api_url)
