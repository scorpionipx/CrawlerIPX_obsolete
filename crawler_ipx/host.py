import logging
import socket as py_socket

from .generic_utils import ALLOWED_NUMBER_OF_CONNECTIONS as GU_ANOC
from .generic_utils import DEFAULT_PORT as GU_DP
from .generic_utils import BUFFER_SIZE
from .generic_utils import COMMAND_HEADER, DATA_HEADER
from .generic_utils import CLIENT_USERNAME as GU_USR
from .generic_utils import CLIENT_PASSWORD as GU_PWD

from .host_utils import HostCommands
from .client_utils import ClientCommands
from .generic_data import DataIPX

logger = logging.getLogger('ipx_logger')


class Host:
    """
        Classed used to control host.
    """
    def __init__(self, port=GU_DP, number_of_connections=GU_ANOC):
        """
            Constructor
        :param port: host's communication port as integer
                     example: 1369
        :param number_of_connections: host's maximum number of connection allowed at once
                                      example: 1
        """
        try:
            logger.debug("Initiating host...")

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

            # initiate commands that can be sent by host
            self.commands = HostCommands()

            # initiate commands that can be sent by client
            self.client_commands = ClientCommands()

            # initiate data that can be send or received
            self.data = DataIPX()

            # client instance and attributes
            self.client = None
            self.client_name = None

            # connection encoding
            self.encoding = 'utf-8'

            logger.debug("Host initiated!")

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

        # logger.debug("Called Host.get_info")

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

    def send_command(self, command, value=None):
        """
            Sends a command to the client.
        :param command: command to be sent as Command type from generic_utils.py
        :param value: value to be used by client, optional parameter
        :return: True if ok, error occurred otherwise
        """

        if self.client is None:
            error = "Unable to send data: no client connected!"
            logger.warning(error)
            return error

        try:
            package = str(COMMAND_HEADER) + '\n' + str(command.id) + '\n' + str(value)
            package = self.string_to_bytes(package)
            self.client.send(package)
            return True
        except Exception as err:
            error = "Error occurred while sending command to client:\ncommand: " + str(command) + '\n' + str(err)
            logger.warning(error)
            return error

    def decode_response(self, client_response):
        """
            Method decodes client's response.
        :param client_response: bytes received from client
        :return: decoded response as dictionary
        """
        response = {"Type": None, "ID": None, "Content": None, "Valid": True, "Error": None}

        client_response = client_response.decode(self.encoding)
        client_response = client_response.split()
        response["Type"] = client_response[0]
        response["ID"] = client_response[1]

        # extract content - needed if content contains new line character
        content = ''
        for index, item in enumerate(client_response):
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
            if response["Type"] == str(COMMAND_HEADER):
                for command in self.client_commands.all_commands:
                    if str(command) == str(response["ID"]):
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

    def ask_client_for_credentials(self):
        """
            Method asks the client requesting the connection for credentials.
        :return: None
        """
        command = self.commands.ask_client_for_credentials
        self.send_command(command)

    def verify_credentials(self, credentials):
        """
            Method checks if the credentials received from client are valid.
        :return: True if valid, false otherwise
        """
        credentials = self.decode_response(credentials)
        username = str(credentials["Content"].split()[0])[2:]
        password = str(credentials["Content"].split()[1])[2:]

        if username == GU_USR and password == GU_PWD:
            return True
        else:
            return False

    def connect_with_client(self):
        """
            Connects with a connection requesting client.
        :return: None
        """
        client_is_valid = False

        logger.info("Waiting for connection request...")
        while not client_is_valid:

            # establish a connection
            self.client, client_address = self.socket.accept()
            info = "Got a connection request from " + str(client_address[0])
            logger.info(info)

            info = "Asking client for credentials..."
            logger.info(info)
            self.ask_client_for_credentials()

            client_response = self.client.recv(BUFFER_SIZE)
            info = "Credentials received! verifying..."
            logger.info(info)

            client_is_valid = self.verify_credentials(client_response)
            if client_is_valid:
                self.client_name = GU_USR
                logger.info("Valid credentials. Client " + str(self.client_name) + " connected!")
            else:
                logger.info("Unknown client connection request! Connection refused!")
                self.client.shutdown(py_socket.SHUT_RDWR)
                self.client.close()
                self.client = None

    def __host_command_name_is_valid__(self, user_command):
        """
            Check if a command is valid.
        :param user_command: command's name to be sent
        :return: True if command is valid, False otherwise
        """
        command_is_valid = False
        for command in self.commands.all_commands:
            if str(user_command) == str(command.in_code):
                command_is_valid = True
                break

        return command_is_valid

    def decode_user_input(self, user_input):
        """
            Method decode user's input and takes proper action.
        :param user_input: user's input
        :return: None
        """
        user_input = str(user_input)
        user_input = user_input.split()
        logger.info("Got user input: " + str(user_input))
        action = str(user_input[0])

        if str(action).upper() == 'send_command'.upper() or str(action).upper() == 'sc'.upper():
            logger.debug("send_command command initiated by user!")
            user_command = str(user_input[1])
            logger.debug("command to be send: " + str(user_command))
            logger.debug("Evaluating command...")
            command_is_valid = self.__host_command_name_is_valid__(user_command)
            if command_is_valid:
                logger.debug("Command is valid.")
            else:
                logger.warning("Invalid command to be sent: {}".format(user_command))

        elif str(action).upper() == 'send_data'.upper() or str(action).upper() == 'sd'.upper():
            logger.debug("send_data command initiated by user!")
            user_data = str(user_input[1])
            logger.debug("data to be send: " + str(user_data))

    def run_user_input_mode(self):
        """
            Host runs in user input mode.
        User input is awaited to take action.
        """
        logger.info("User input mode enabled! Waiting for user input...")
        user_input_mode = True
        while user_input_mode:
            user_input = input()
            self.decode_user_input(user_input)






