import re

from lxml.etree import XMLSyntaxError
from lxml.objectify import fromstring
import binascii
import zlib
import six


def is_gziped(content):
    signature = content[:2]
    if isinstance(signature, six.binary_type):
        res = binascii.hexlify(signature) == b'1f8b'
    elif isinstance(signature, six.text_type):
        res = binascii.hexlify(signature.encode('utf-8')) == b'1f8b'
    else:
        raise ValueError('type {} not supported'.format(type(content)))

    return res


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
        try:
            self._xml = value.decode('iso-8859-15')
        except:
            self._xml = value

        # If there is null chars on the XML string, delete it
        try:
            xml = fromstring(self._xml)
        except XMLSyntaxError as e:
            # Delete everything from the first null char until the next double quote char '"'
            xml_string = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F].*?"', '"', self._xml)
            xml = fromstring(xml_string)

        self._objectified = xml


class MessageS(BaseMessage):
    """
    Message class for reports.
    """
    pass
