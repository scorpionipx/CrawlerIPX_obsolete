import logging
from crawler_ipx.host import Host

logger = logging.getLogger('ipx_logger')

logger.info("Running host from bat script\n\n")

ipx_host = Host()
logger.info(ipx_host.get_info())
ipx_host.run_user_input_mode()
