import logging

# ===================================================== CONSTANTS =====================================================
# Maximum number of connections to host allowed at once (maximum number of clients)
ALLOWED_NUMBER_OF_CONNECTIONS = 1

# Default connection port
DEFAULT_PORT = 1369

# Data income buffer size
BUFFER_SIZE = 64

# Headers used to send and receive data/commands
COMMAND_HEADER = 0
DATA_HEADER = 1

# Client default credentials
CLIENT_USERNAME = 'RaspberryPIScorpionIPX'
CLIENT_PASSWORD = 'Qwerty123'
# ===================================================== CONSTANTS =====================================================


logger = logging.getLogger('ipx_logger')


class Command:
    """
        Class used to handle commands sent and received by IPX client and host.
    """
    def __init__(self, cmd_id, name, description, in_code, value_required=False):
        """
            Constructor
        :param cmd_id: unique id of the command as positive integer
                       example: 13
        :param name: command's name as string
                     example: Ask client for it's name
        :param in_code: code used to call command as string
                        example: ask_client_name
        :param description: command's description as string
                            example: Get client's name command asks client to send it's name
                                     id: 13
                                     value_required: False
                                     in_code usage: ask_client_name
        :param value_required: specifies if additional info (for instance a value) is required when sending the command.
                               example: set_speed_command(speed_value) would require the speed_value additional info
        """
        if type(cmd_id) is not int or cmd_id < 0:
            error = "Invalid command id: {}!".format(cmd_id) + "\nExpected positive integer type!"
            raise NameError(error)

        if type(name) is not str:
            error = "Invalid command name: {}".format(name) + "\nExpected str type!"
            raise NameError(error)

        if type(in_code) is not str:
            error = "Invalid command in_code: {}".format(in_code) + "\nExpected str type!"
            raise NameError(error)

        if type(description) is not str:
            error = "Invalid command description: {}".format(description) + "\nExpected str type!"
            raise NameError(error)

        if type(value_required) is not bool:
            error = "Invalid command value required attribute: {}".format(value_required) + "\nExpected bool type!"
            raise NameError(error)

        self.id = cmd_id
        self.name = name
        self.in_code = in_code
        self.description = description
        self.value_required = value_required

        logger.debug("Command " + str(self.in_code) + " initiated!")

    def get_id(self):
        """
            Get command's id.
        :return: id - integer
        """
        return self.id

    def get_name(self):
        """
            Get command's name.
        :return: name - string
        """
        return self.name

    def get_in_code(self):
        """
            Get command's in_code - in code usage.
        :return: in_code
        """
        return self.in_code

    def get_description(self):
        """
            Get command's description.
        :return: description - string
        """
        return self.description

    def get_value_required(self):
        """
            Get command's value required attribute.
        :return: value_required - bool
        """
        return self.value_required

    def __str__(self):
        """
            Informal” or nicely printable string representation of the object.
        :return: name
        """
        return str(self.name)

    def __unicode__(self):
        """
            Informal” or nicely printable string representation of the object required for older versions of Python.
        :return: name
        """
        return str(self.name)

    def __lt__(self, other_command):
        """
            Method used to be able to sort Command type objects by their ID.
        :param other_command: Command object to compare id with
        :return: bool True or False
        """
        return self.name < other_command.name


class Data:
    """
        Class used to handle data sent and received by IPX client and host.
    """
    def __init__(self, data_id, name, in_code, description):
        """
            Constructor
        :param data_id: unique id of the data as positive integer
                        example: 13
        :param name: data's name as string
                     example: Headlights status
        :param in_code: code used to call data as string
                        example: headlights_status
        :param description: data's description as string
                            example: Headlights status data indicates status of headlights
                                     id: 13
                                     in_code usage: headlights_status
        """

        if type(data_id) is not int or data_id < 0:
            error = "Invalid data id: {}!".format(data_id) + "\nExpected positive integer type!"
            raise NameError(error)

        if type(name) is not str:
            error = "Invalid data name: {}".format(name) + "\nExpected str type!"
            raise NameError(error)

        if type(in_code) is not str:
            error = "Invalid data in_code: {}".format(in_code) + "\nExpected str type!"
            raise NameError(error)

        if type(description) is not str:
            error = "Invalid data description: {}".format(description) + "\nExpected str type!"
            raise NameError(error)

        self.id = data_id
        self.name = name
        self.in_code = in_code
        self.description = description

        logger.debug("Data " + str(self.in_code) + " initiated!")

    def get_id(self):
        """
            Get data's id.
        :return: id - integer
        """
        return self.id

    def get_name(self):
        """
            Get data's name.
        :return: name - string
        """
        return self.name

    def get_in_code(self):
        """
            Get data's in_code - in code usage.
        :return: in_code
        """
        return self.in_code

    def get_description(self):
        """
            Get data's description.
        :return: description - string
        """
        return self.description

    def __str__(self):
        """
            Informal” or nicely printable string representation of the object.
        :return: name
        """
        return str(self.name)

    def __unicode__(self):
        """
            Informal” or nicely printable string representation of the object required for older versions of Python.
        :return: name
        """
        return str(self.name)




