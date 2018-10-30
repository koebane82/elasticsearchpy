import unittest
from elasticsearchpy.host import ElasticSearchHost, ElasticRestResponse
from elasticsearchpy.indices import ElasticSearchIndices
from elasticsearchpy.cluster import ElasticSearchCluster

from moc_classes import MockHttp


class ElastiSearchHostUnitTest(unittest.TestCase):

    def setUp(self):
        self.http_conn = MockHttp()
        self.address = "1.1.1.1"
        self.port = 9300

        self.http_conn.add_url_response(
            url="testpoint",
            method="GET",
            status=200,
            reason="OK",
            response="{\"Good\":\"Data\"}"
        )

    def test_ElasticSearchHost(self):
        host = ElasticSearchHost(self.address, self.port,
                                http_conn=self.http_conn)
        self.assertTrue(isinstance(host, ElasticSearchHost))

    def test_rest_query(self):
        host = ElasticSearchHost(self.address, self.port,
                                http_conn=self.http_conn)
        response = host.rest_query("testpoint")
        self.assertTrue(isinstance(response, ElasticRestResponse))
        self.assertTrue(response.success)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, "OK")
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data.get("Good"), "Data")

    def test_get_indices(self):
        host = ElasticSearchHost(self.address, self.port,
                                http_conn=self.http_conn)

        indices = host.get_indices()
        self.assertTrue(isinstance(indices, ElasticSearchIndices))

    def test_get_cluster(self):
        host = ElasticSearchHost(self.address, self.port,
                                http_conn=self.http_conn)

        cluster = host.get_cluster()
        self.assertTrue(isinstance(cluster, ElasticSearchCluster))
