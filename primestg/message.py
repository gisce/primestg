from lxml.objectify import fromstring


class BaseMessage(object):
    """
    Base XML message.
    """
    def __init__(self, xml):
        """
        Create an object of BaseMessage.

        :param xml: a file object or a string with the XML
        :return: an instance of BaseMessage
        """
        self.objectified = xml

    @property
    def objectified(self):
        """
        The XML objectified

        :return: the XML objectified
        """
        return self._objectifyed

    @objectified.setter
    def objectified(self, value):
        """
        Objectify an XML

        :param value: a file object or string with the XML
        """

        if isinstance(value, file):
            value = value.read()
        self._xml = value
        self._objectifyed = fromstring(self._xml)


class MessageS(BaseMessage):
    """
    Message class for reports.
    """
    pass
