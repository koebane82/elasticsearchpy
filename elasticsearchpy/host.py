import http.client
import json
import logging
import ssl
from .indices import ElasticSearchIndices
from .cluster import ElasticSearchCluster


class _RestResponse:
    good_codes = [200,201]

    def __init__(self, http_response):
        self.status = http_response.status
        self.reason = http_response.reason

        if self.status in self.good_codes:
            self.success = True
        else:
            self.success = False

        self.data = None
        self.data = http_response.read().decode("utf-8")

        try:
            self.data = json.loads(self.data)
        except:
            logging.debug("Response is not JSON")

    def to_dict(self):
        return {"status": self.status,
                "reason": self.reason,
                "data": self.data
                }


class ElastiSearchHost:
    _headers = {"Content-Type": "application/json"}

    def __init__(self, address, port=9200, use_ssl=False, cert=None, key=None):
        self._address = address
        self._port = port

        if use_ssl:
            context = ssl.SSLContext()
            context.verify_mode = ssl.CERT_NONE

            self._http_conn = http.client.HTTPSConnection(
                host=self._address,
                port=self._port,
                context=context,
                key_file=key,
                cert_file=cert)
        else:
            self._http_conn = http.client.HTTPConnection(
                host=self._address,
                port=self._port
            )

    def rest_query(self, end_point, method="GET", body=None, headers=None):
        if headers is None:
            headers = self._headers

        self._http_conn.request(method, end_point,
                                body=body,
                                headers=headers
                                )
        logging.debug("REST: Request {}: {}".format(method, end_point))
        resp = _RestResponse(
            self._http_conn.getresponse())

        logging.debug("REST: Response {}".format(resp))
        return resp

    def get_indices(self, indice_prefix=None, system_indices=False):
        return ElasticSearchIndices(self, indice_prefix, system_indices)

    def get_cluster(self):
        return ElasticSearchCluster(self)
