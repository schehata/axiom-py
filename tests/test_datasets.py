"""This module contains the tests for the DatasetsClient."""
import os
import unittest
from logging import getLogger
from datetime import datetime, timedelta
from axiom import Client, DatasetCreateRequest, DatasetUpdateRequest, Query, \
                    QueryOptions, QueryKind, QueryResult, QueryStatus, Entry, Timeseries
from .helpers import get_random_name, parse_time


class TestDatasets(unittest.TestCase):

    dataset_name: str
    client: Client

    @classmethod
    def setUpClass(cls):
        cls.dataset_name = get_random_name()
        cls.client = Client(
            os.getenv("AXIOM_DEPLOYMENT_URL"),
            os.getenv("AXIOM_TOKEN"),
            os.getenv("AXIOM_ORG_ID"),
        )
        cls.logger = getLogger()
        cls.logger.info(f"generated random dataset name is: {cls.dataset_name}")

    def test_step1_create(self):
        """Tests create dataset endpoint"""
        req = DatasetCreateRequest(
            name=self.dataset_name,
            description="create a dataset to test the python client",
        )
        res = self.client.datasets.create(req)
        self.logger.debug(res)
        assert res.name == self.dataset_name

    def test_step2_ingest(self):
        """Tests the ingest endpoint"""
        res = self.client.datasets.ingest(
            self.dataset_name, [{"foo": "bar"}, {"bar": "baz"}]
        )
        self.logger.debug(res)

        assert (
            res.ingested == 2
        ), f"expected ingested count to equal 2, found {res.ingested}"

    def test_step3_get(self):
        """Tests get dataset endpoint"""
        dataset = self.client.datasets.get(self.dataset_name)
        self.logger.debug(dataset)

        assert dataset.name == self.dataset_name

    def test_step4_list(self):
        """Tests list datasets endpoint"""
        datasets = self.client.datasets.get_list()
        self.logger.debug(datasets)

        assert len(datasets) > 0

    def test_step5_update(self):
        """Tests update dataset endpoint"""
        updateReq = DatasetUpdateRequest("updated name through test")
        ds = self.client.datasets.update(self.dataset_name, updateReq)

        assert ds.description == updateReq.description

    def test_step6_query(self):
        """Test querying a dataset"""
        expec_result = self._build_expected_query_result()

        q = Query(startTime=datetime.now(), endTime=datetime.now())
        opts = QueryOptions(streamingDuration=timedelta(seconds=1), nocache=True, saveAsKind=QueryKind.ANALYTICS)
        self.client.datasets.query(self.dataset_name, q, opts)

    def test_step7_delete(self):
        """Tests delete dataset endpoint"""
        self.client.datasets.delete(self.dataset_name)

        datasets = self.client.datasets.get_list()

        self.assertEqual(len(datasets), 0, "expected test dataset to be deleted")

    def _build_expected_query_result(self) -> QueryResult:
        status = QueryStatus(
            elapsedTime=542114,
            blocksExamined=4,
            rowsExamined=142655,
            rowsMatched=142655,
            numGroups=0,
            isPartial=False,
            minBlockTime=parse_time("2020-11-19T11:06:31.569475"),
            maxBlockTime=parse_time("2020-11-27T12:06:38.966791"),
        )

        matches = [
            Entry(_time=datetime.now(), _sysTime=datetime.now(), _rowId="c776x1uafkpu-4918f6cb9000095-0",
                data = {
                    "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)",
                    "bytes":       0,
                    "referrer":    "-",
                    "remote_ip":   "93.180.71.3",
                    "remote_user": "-",
                    "request":     "GET /downloads/product_1 HTTP/1.1",
                    "response":    304,
                    "time":        "17/May/2015:08:05:32 +0000",
                }),
            Entry(_time=datetime.now(), _sysTime=datetime.now(), _rowId="c776x1uafnvq-4918f6cb9000095-1",
                data = {
                    "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)",
                    "bytes":       0,
                    "referrer":    "-",
                    "remote_ip":   "93.180.71.3",
                    "remote_user": "-",
                    "request":     "GET /downloads/product_1 HTTP/1.1",
                    "response":    304,
                    "time":        "17/May/2015:08:05:32 +0000",
                })
        ]

        query_intervals: List[Interval] = []
        totals: List[EntryGroup] = []
        buckets = Timeseries(query_intervals, totals)
        r = QueryResult(
            status=status,
            matches=matches,
            buckets=buckets,
        )

        return r
