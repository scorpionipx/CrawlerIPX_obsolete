import logging

from .generic_utils import Data
from .generic_data_constants import *

logger = logging.getLogger('ipx_logger')


class DataIPX:
    """
        Class used to handle data send and received by host and client.
    """
    def __init__(self):
        """
            Constructor
        """
        logger.debug("Initiating IPX data...")

        self.command_accepted = Data(
            COMMAND_ACCEPTED_DATA_ID,
            COMMAND_ACCEPTED_DATA_NAME,
            COMMAND_ACCEPTED_DATA_DESCRIPTION,
            COMMAND_ACCEPTED_DATA_IN_CODE,
        )

        self.credentials = Data(
            CREDENTIALS_DATA_ID,
            CREDENTIALS_DATA_NAME,
            CREDENTIALS_DATA_DESCRIPTION,
            CREDENTIALS_DATA_IN_CODE,
        )

        logger.debug("IPX data initiated!")




