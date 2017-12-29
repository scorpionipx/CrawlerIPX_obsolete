import logging
import socket as py_socket

from .generic_utils import DEFAULT_PORT as GU_DP
from .generic_utils import BUFFER_SIZE
from .generic_utils import COMMAND_HEADER, DATA_HEADER
from .generic_utils import CLIENT_USERNAME as GU_USR
from .generic_utils import CLIENT_PASSWORD as GU_PWD

from .host_utils import HostCommands
from .client_utils import ClientCommands
from .generic_data import DataIPX

logger = logging.getLogger('ipx_logger')


class Client:
    """
        Class used to control client.
    """
    def __init__(self, host, port=GU_DP, username=GU_USR, password=GU_PWD):
        """
            Constructor
        :param host: remote host's name or ip to connect to as string
                     example: '192.168.100.15'
        :param port: host's communication port as integer
                     example: 1369
        :param username: client's username required for authentication as string
                         example: 'RaspberryPIScorpionIPX'
        :param password: client's password required for authentication as string
                         example: 'Qwerty123'
        """
        try:
            logger.debug("Initiating client...")

            # create the socket object
            self.socket = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)

            # setting host and port
            self.host = host
            self.port = port

            # setting credentials
            self.username = username
            self.password = password

            # initiate commands that can be sent by client
            self.commands = ClientCommands()

            # initiate commands that can be sent by host
            self.host_commands = HostCommands()

            # initiate data that can be send or received
            self.data = DataIPX()

            self.encoding = 'utf-8'

            logger.debug("Client initiated!")

        except Exception as err:
            error = "Failed to initiate client! " + str(err)
            logger.warning(error)

    def string_to_bytes(self, _string, encoding=None):
        """
            Method converts string type to bytes, using specified encoding.
        Conversion is required for socket's data transfer protocol: string type is not supported.
        :param _string: string to be converted
        :param encoding: character encoding key
        :return: bytes(_string, encoding)
        """
        if encoding is None:
            encoding = self.encoding
        return bytes(_string, encoding)

    def connect_to_host(self):
        """
            Method establishes connection to the host.
        :return: None
        """
        self.socket.connect((self.host, self.port))

        server_response = self.socket.recv(BUFFER_SIZE)

        logger.info("Server's response: " + str(server_response))

        self.send_credentials()

    def send_data(self, data_id, data):
        """
            Method sends a data to the host.
        :param data_id: specifies the data type that is sent to server.
        :param data: actual data
        :return: boolean True if ok, error occurred as string if not ok.
        """
        try:
            data = str(DATA_HEADER) + '\n' + str(data_id) + '\n' + str(data)
            data = self.string_to_bytes(data)
            self.socket.send(data)
            return True
        except Exception as err:
            error = "Error occurred while sending data to client:\ndata_id: " + str(data_id) + '\ndata: ' + str(data)\
                    + '\n' + str(err)
            logger.warning(error)
            return error

    def send_credentials(self):
        """
            Method sends credentials required to connect to the server.
        :return: None
        """
        logger.info("Sending credentials...")
        data = 'u:' + str(self.username) + '\np:' + str(self.password)
        self.send_data(1, data)




