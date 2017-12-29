import logging

from .generic_utils import Command
from .host_commands_constants import *

logger = logging.getLogger('ipx_logger')


class HostCommands:
    """
        Class used to handle host's commands.
    """
    def __init__(self):
        """
            Constructor
        """

        logger.debug("Initiating host commands...")

        self.ask_client_for_credentials = Command(
            ASK_CLIENT_FOR_CREDENTIALS_CMD_ID,
            ASK_CLIENT_FOR_CREDENTIALS_CMD_NAME,
            ASK_CLIENT_FOR_CREDENTIALS_CMD_DESCRIPTION,
            ASK_CLIENT_FOR_CREDENTIALS_CMD_IN_CODE,
            ASK_CLIENT_FOR_CREDENTIALS_CMD_VR,
        )

        self.start_video_streaming = Command(
            START_VIDEO_STREAMING_CMD_ID,
            START_VIDEO_STREAMING_CMD_NAME,
            START_VIDEO_STREAMING_CMD_DESCRIPTION,
            START_VIDEO_STREAMING_CMD_IN_CODE,
            START_VIDEO_STREAMING_CMD_VR,
        )

        self.all_commands = sorted(
            [
                self.ask_client_for_credentials,
                self.start_video_streaming,
            ]
        )

        logger.debug("Host commands initiated!")


