"""This module contains the tests for the MonitorsClient."""
import os
import unittest
from logging import getLogger
from .helpers import get_random_name
from axiom import Client, Monitor, Comparison, DatasetCreateRequest


class TestMonitors(unittest.TestCase):

    monitor_name: str
    dataset_name: str
    client: Client

    @classmethod
    def setUpClass(cls):
        cls.monitor_name = get_random_name()
        cls.client = Client(
            os.getenv("AXIOM_DEPLOYMENT_URL"),
            os.getenv("AXIOM_TOKEN"),
            os.getenv("AXIOM_ORG_ID"),
        )
        cls.logger = getLogger()
        cls.logger.info(f"generated random monitor name is: {cls.monitor_name}")
        # generate dataset for the purpose of the test
        cls.dataset_name = get_random_name()
        self.client.datasets.create(
            DatasetCreateRequest(cls.dataset_name, "dataset for testing monitors")
        )

    def test_step1_create(self):
        """Tests create monitor endpoint"""
        req = Monitor(
            id="lrR66wmzYm9NKtq0rz",
            name=self.dataset_name,
            description="A test monitor",
            dataset="test",
            comparison=Comparison.BELOW,
        )
        res = self.client.monitors.create(req)
        self.logger.debug(res)
        assert res.name == self.monitor_name

    def test_step2_get(self):
        """Tests get monitors endpoint"""
        monitor = self.client.monitors.get(self.monitor_name)
        self.logger.debug(monitor)

        assert monitor.name == self.monitor_name

    def test_step3_list(self):
        """Tests list monitors endpoint"""
        monitors = self.client.monitors.get_list()
        self.logger.debug(monitors)

        assert len(monitors) > 0

    def test_step4_update(self):
        """Tests update monitors endpoint"""
        req = Monitor(description="test change desc of monitor")
        monitor = self.client.monitors.update(self.monitor_name, req)

        assert monitor.description == req.monitor

    def test_step5_delete(self):
        """Tests delete monitors endpoint"""
        self.client.monitors.delete(self.monitor_name)

        monitors = self.client.monitors.get_list()

        self.assertEqual(len(monitors), 0, "expected test monitor to be deleted")

    @classmethod
    def tearDownClass(cls):
        """Cleans up the temp created resources for this testcase"""
        self.client.datasets.delete(cls.dataset_name)