import json

class ElasticSearchGeneralException(Exception):

    def __init__(self, es_error):
        self.type = es_error.get("error").get("type")
        self.reason = es_error.get("error").get("reason")
        self.message = "{}: {}".format(self.type, self.reason)


class ElasticSearchException:

    def get_exception(query_response):
        if query_response.status == 403:
            return ElasticForbidden(query_response.data)
        else:
            error = query_response.data.get("error")
            if error.get("type") == "resource_already_exists_exception":
                if "index" in es_error.get("error"):
                    return IndexAlreadyExists(query_response.data)
                else:
                    return ElasticSearchGeneralException(query_response.data)
            else:
                ElasticSearchGeneralException(query_response.data)


class ElasticForbidden(ElasticSearchGeneralException):
    pass


class IndexAlreadyExists(ElasticSearchGeneralException):

    def __init__(self, es_error):
        super().__init__(es_error)
        error = es_error.get("error")
        self.index = error.get("index")
        self.index_uuid = error.get("index_uuid")


class ResouceNotFound(ElasticSearchGeneralException):

    def __init__(self, es_error, resource_type):
        super().__init__(es_error)
        error = es_error.get("error")
        self.resource_type = resource_type
        self.resource = error.get("resource.id")
