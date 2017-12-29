import logging
import socket as py_socket

from .generic_utils import ALLOWED_NUMBER_OF_CONNECTIONS as GU_ANOC
from .generic_utils import DEFAULT_PORT as GU_DP

logger = logging.getLogger('ipx_logger')


class Host:
    """
        Classed used to control host.
    """
    def __init__(self, port=GU_DP, number_of_connections=GU_ANOC):
        """
            Constructor
        """
        try:

            # create the socket object
            self.socket = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)

            # set host's name
            self.name = py_socket.gethostname()

            # set host's ip address and port
            self.ip = self.__get_host_ip_address__()
            self.port = port

            # bind the socket to public interface
            self.socket.bind((self.name, self.port))

            # allow a specific number of connections
            self.socket.listen(number_of_connections)

            # client instance and attributes
            self.client = None
            self.client_name = None

            # connection encoding
            self.encoding = 'utf-8'

        except Exception as err:
            error = 'Failed to initialize Host! ' + str(err)
            logger.error(error)

    def __get_host_ip_address__(self):
        """
            Get current created host's ip address.
        At initialization, IP address is unknown. It may be different when connected to another router/network.
        Host's IP address is needed by client to know at which address to connect.
        :return: ip - string
        """
        ip = py_socket.gethostbyname(py_socket.gethostname())
        return ip

    def get_ip(self):
        """
            Get host's ip address.
        :return: ip - string
        """
        return self.ip

    def get_port(self):
        """
            Get host's port.
        :return: port - integer
        """
        return self.port

    def get_name(self):
        """
            Get host's name.
        :return: name - string
        """
        return self.name

    def get_encoding(self):
        """
            Get host's encoding.
        :return: encoding - string
        """
        return self.encoding

    def get_info(self):
        """
            Get host's info: ip address, port, name, encoding, etc...
        :return: host_info - string
        """

        logger.debug("Called Host.get_info")

        name = self.get_name()
        ip = self.get_ip()
        port = self.get_port()
        encoding = self.get_encoding()

        host_info = "Host info\n"
        host_info += "Name: " + str(name) + "\n"
        host_info += "IP: " + str(ip) + "\n"
        host_info += "Port: " + str(port) + "\n"
        host_info += "Encoding: " + str(encoding) + "\n"

        logger.debug(host_info)

        return host_info

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




