from lxml.objectify import fromstring
import binascii
import zlib


def is_gziped(content):
    return binascii.hexlify(content[:2].encode('utf-8')) == b'1f8b'


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
        return self._objectified

    @objectified.setter
    def objectified(self, value):
        """
        Objectify an XML

        :param value: a file object or string with the XML
        """

        if hasattr(value, 'read'):
            value = value.read()
        if is_gziped(value):
            value = zlib.decompress(value, zlib.MAX_WBITS | 32)
        self._xml = value
        self._objectified = fromstring(self._xml)


class MessageS(BaseMessage):
    """
    Message class for reports.
    """
    pass
