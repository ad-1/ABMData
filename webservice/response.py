from enum import Enum


class Response(Enum):
    """
    possible responses for 'POST' method
    codes 766 and 755 correspond to -1 and -2 as response was invalid
    """

    VALID_PAYLOAD = '<h1>Status 0</h1><h2>Payload validated successfully</h2>', 0
    INVALID_XML = '<h1>Error 400</h1><h2>Invalid XML</h2>', 400
    INVALID_XSD = '<h1>Error 400</h1><h2>Invalid Payload</h2>', 400
    INVALID_DECLARATION_CMD = '<h1>Error -1</h1><h2>Invalid Declaration Command</h2>', 766
    INVALID_SITEID = '<h1>Error -2</h1><h2>Invalid Site ID</h2>', 755