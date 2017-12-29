import logging
import unittest

from crawler_ipx.host import Host
from crawler_ipx.client import Client

logger = logging.getLogger('ipx_logger')


class TestConnection(unittest.TestCase):

    def test_connection(self):
        logger.info("\n\nRunning TestConnection - test_connection\n")
        ipx_host = Host()
        self.assertIsInstance(ipx_host, Host)

        host_name = ipx_host.get_name()

        ipx_client = Client(host_name)
        self.assertIsInstance(ipx_client, Client)





