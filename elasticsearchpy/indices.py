import logging
from .exceptions import ElasticForbidden, ElasticSearchException
from .exceptions import IndexAlreadyExists, ResouceNotFound
from .bases import _ElasticBase


class ElasticSearchIndices(_ElasticBase):
    _indices = []

    def __init__(self, es_host, indice_prefix=None, system_indices=False):
        self._indice_prefix = indice_prefix
        self._system_indices = system_indices
        super().__init__(es_host)

    def _get_indices(self):
        query = self._es_host.rest_query("/_cat/indices?v")

        if query.success:
            indice_list = query.data.split("\n")

            for record in indice_list:
                s_rec = record.split()
                if len(s_rec) >= 2:
                    indice_name = s_rec[2]

                    if not self._system_indices:
                        if indice_name.startswith("."):
                            continue

                    if self._indice_prefix is not None:
                        if not indice_name.startswith(self._indice_prefix):
                            continue

                    self._indices.append(indice_name)

        else:
            print(query)

    def indices(self):
        return self._indices

    def get_indice(self, name):
        ret_indice = None
        if name in self._indices:
            ret_indice = ElasticSearchIndice(name, self._es_host)

        return ret_indice

    def count(self):
        return len(self._indices)

    def create_indice(self, name, shards=None, replicas=None, mappings=None, aliases=None):
        data = None
        if shards is not None:
            data = {
                "settings": {
                    "index": {
                        "number_of_shards": shards,
                        "number_of_replicas": 0
                    }
                }
            }

        if replicas is not None:
            if data is not None:
                data["settings"]["index"]["number_of_replicas"] = replicas
            else:
                data = {
                    "settings": {
                        "index": {
                            "number_of_shards": 1,
                            "number_of_replicas": replicas
                        }
                    }
                }

        if mappings is not None:
            if data is not None:
                data["mappings"] = mappings
            else:
                data = {"mappings": mappings}

        if aliases is not None:
            if data is not None:
                data["aliases"] = aliases
            else:
                data = {"aliases": aliases}

        rest_query = self._es_host.rest_query(
            end_point="/{}".format(name),
            method="PUT",
            body=data)

        if rest_query.success:
            self._indices.append(name)
            return ElasticSearchIndice(name, self._es_host)

        else:
            raise(ElasticSearchException(rest_query))

    def delete_indice(self, name):
        rest_query = self._es_host.rest_query(
            end_point="/{}".format(name),
            method="DELETE"
        )

        if rest_query.success:
            self._indices.remove(name)
            return True
        else:
            raise(ElasticSearchException(rest_query))


class ElasticSearchIndice(_ElasticBase):
    _docs = None
    _deleted_docs = None
    _size = None
    _total_shards = None
    _primary_shards = None
    _replicas = None
    _status = None
    _health = None
    _uuid = None
    _mappings = None

    def __init__(self, name, es_host):
        self.name = name
        super().__init__(es_host)

    def _get_stats(self):
        stats = self._es_host.rest_query(
            "/_cat/indices/{}".format(self.name)
        )

        if stats.success:
            data = stats.data.split()

            self._docs = int(data[6])
            self._deleted_docs = int(data[7])
            self._size = data[8]
            self._primary_shards = int(data[4])
            self._replicas = int(data[5])
            self._status = data[1]
            self._health = data[0]
            self._uuid = data[3]
            self._total_shards = self._primary_shards * (self._replicas + 1)
        else:
            logging.error("Unable to get indice statistics: {}:{}".format(
                stats.status, stats.reason))
            logging.debug("REST ERROR: {}".format(stats.data))

    def _get_mappings(self):
        rest_query = self._es_host.rest_query(
            "/{}/_mapping/_doc".format(self.name)
        )

        if rest_query.success:
            self._mappings = rest_query.data
        else:
            if rest_query.status == 404:
                return None
            else:
                raise(ElasticSearchException(rest_query))

    def to_dict(self):
        if self._docs is None:
            self._get_stats()

        ret_dict = {
            "name": self.name,
            "uuid": self._uuid,
            "docs": self._docs,
            "deleted_docks": self._deleted_docs,
            "size": self._size,
            "primary_shards": self._primary_shards,
            "replicas": self._replicas,
            "total_shards": self._total_shards,
            "status": self._status,
            "health": self._health
        }

        return ret_dict

    def mappings(self):
        if self._mappings is None:
            self._get_mappings()

        return self._mappings

    def docs(self):
        if self._docs is None:
            self._get_stats()

        return self._docs

    def deleted_docs(self):
        if self._deleted_docs:
            self._get_stats()

        return self._deleted_docs

    def size(self):
        if self._size is None:
            self._get_stats()

        return self._size

    def primary_shards(self):
        if self._primary_shards is None:
            self._get_stats()

        return self._primary_shards

    def replicas(self):
        if self._replicas is None:
            self._get_stats()

        return self._replicas

    def total_shards(self):
        if self._total_shards is None:
            self._get_stats()

        return self._total_shards

    def status(self):
        if self._status is None:
            self._get_stats()

        return self._status

    def health(self):
        if self._health is None:
            self._get_stats()

        return self._health

    def uuid(self):
        if self._uuid is None:
            self._get_stats()

        return self._uuid

    def refresh(self):
        self._get_stats()
