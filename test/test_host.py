import unittest

from crawler_ipx.host import Host


class TestHostCreation(unittest.TestCase):

    def test_host_initialization(self):
        ipx_host = Host()
        self.assertIsInstance(ipx_host, Host)


class TestHostInformation(unittest.TestCase):

    def test_host_information(self):
        ipx_host = Host()

        host_info = ipx_host.get_info()
        print(host_info)



