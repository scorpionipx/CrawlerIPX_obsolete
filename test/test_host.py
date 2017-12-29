import logging
import unittest

from crawler_ipx.host import Host

logger = logging.getLogger('ipx_logger')


class TestHostCreation(unittest.TestCase):

    def test_host_initialization(self):
        logger.info("\n\nRunning TestHostCreation - test_host_initialization\n")
        ipx_host = Host()
        self.assertIsInstance(ipx_host, Host)


class TestHostInformation(unittest.TestCase):

    def test_host_information(self):
        logger.info("\n\nRunning TestHostInformation - test_host_information...\n")
        ipx_host = Host()

        host_info = ipx_host.get_info()
        logger.info(host_info)



