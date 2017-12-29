import logging
from crawler_ipx.client import Client

test_host = '192.168.100.15'

logger = logging.getLogger('ipx_logger')

logger.info("Running client from bat script\n\n")

ipx_client = Client(test_host)
ipx_client.connect_to_host()
ipx_client.run_in_slave_mode()

