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

    def decode_server_response(self, server_response):
        """
            Method decodes client's response.
        :param server_response: bytes received from client
        :return:
        """
        response = {"Type": None, "ID": None, "Content": None, "Valid": True, "Error": None}

        server_response = server_response.decode(self.encoding)
        server_response = server_response.split()
        response["Type"] = server_response[0]
        response["ID"] = server_response[1]

        # extract content - needed if content contains new line character
        content = ''
        for index, item in enumerate(server_response):
            if index > 1:
                content += '\n'
                content += str(item)

        response["Content"] = content

        # validate content
        if response["Valid"]:
            if (response["Type"]) == str(COMMAND_HEADER) or str(response["Type"]) == str(DATA_HEADER):
                response["Valid"] = True
            else:
                response["Valid"] = False
                if response["Error"] is None:
                    response["Error"] = "Invalid header ID!"
                else:
                    response["Error"] += '\n'
                    response["Error"] += "Invalid header ID!"

        if response["Valid"]:
            id_is_valid = False
            for command in self.host_commands.all_commands:
                if str(command.id) == str(response["ID"]):
                    id_is_valid = True
                    break

            if id_is_valid:
                response["Valid"] = True
            else:
                response["Valid"] = False
                if response["Error"] is None:
                    response["Error"] = "Invalid data/command ID!"
                else:
                    response["Error"] += '\n'
                    response["Error"] += "Invalid data/command ID!"

        # test_print("\nType: " + str(response["Type"]) + "\nID: " + str(response["ID"]) + "\nContent:" +
        #            str(response["Content"]) + "\nValid: " + str(response["Valid"]) + "\nErrors: " +
        #            str(response["Error"]))

        return response

    def connect_to_host(self):
        """
            Method establishes connection to the host.
        :return: None
        """
        self.socket.connect((self.host, self.port))

        server_response = self.socket.recv(BUFFER_SIZE)

        logger.info("Server's response: " + str(server_response))

        self.send_credentials()

    def send_data(self, data, value):
        """
            Method sends a data to the host.
        :param data: IPX data type
        :param value: data's content
        :return: boolean True if ok, error occurred as string if not ok.
        """
        try:
            package = str(DATA_HEADER) + '\n' + str(data.id) + '\n' + str(value)
            package = self.string_to_bytes(package)
            self.socket.send(package)
            return True
        except Exception as err:
            error = "Error occurred while sending data to client:\ndata: " + str(data) + '\nvalue: ' + str(value)\
                    + '\n' + str(err)
            logger.warning(error)
            return error

    def send_credentials(self):
        """
            Method sends credentials required to connect to the server.
        :return: None
        """
        logger.info("Sending credentials...")
        value = 'u:' + str(self.username) + '\np:' + str(self.password)
        self.send_data(self.data.credentials, value)

    def __get_host_command_by_id__(self, command_id):
        """
            Get host's Command type matching command_id.
        :param command_id: host's command id as integer
        """
        logger.debug("Client.__get_host_command_by_id__ called.")

        host_command = None
        for command in self.host_commands.all_commands:
            if command.id == command_id:
                host_command = command
                break

        logger.debug("Provided command_id {} matched command: {}".format(command_id, command))
        return host_command

    def run_in_slave_mode(self):
        """
            Client continuously listens to host's command.
        :return: None
        """
        logger.info("Slave mode enabled! Waiting for host's commands...")
        slave_mode = True
        while slave_mode:
            server_command = self.socket.recv(BUFFER_SIZE)
            server_command = self.decode_server_response(server_command)

            logger.debug("Received package from host: {}".format(server_command))

            if server_command["Type"] == str(COMMAND_HEADER):
                host_command = self.__get_host_command_by_id__(int(server_command["ID"]))
                if host_command is not None:
                    logger.debug("Execute command {}".format(host_command))
                    self.run_slave_command(host_command)
                else:
                    logger.warning("Invalid command provided!")

    def start_video_streaming(self):
        """
            TO DO
        :return:
        """
        pass

    def stop_video_streaming(self):
        """
            TO DO
        :return:
        """
        pass

    def run_slave_command(self, host_command):
        """
            Run command received from host.
        :param host_command: command type object
        :return: None
        """
        if host_command.id == self.host_commands.ask_client_for_credentials.id:
            self.send_credentials()

        elif host_command.id == self.host_commands.start_video_streaming.id:
            self.start_video_streaming()
            self.send_data(self.data.command_accepted, True)

        elif host_command.id == self.host_commands.stop_video_streaming.id:
            self.stop_video_streaming()
            self.send_data(self.data.command_accepted, True)

        else:
            logger.warning("Unknown command provided! {}".format(host_command))



