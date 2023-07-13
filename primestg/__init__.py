import os

try:
    __version__ = __import__('pkg_resources') \
        .get_distribution(__name__).version
except Exception as e:
    __version__ = 'unknown'

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    wsdl_path = False

    try:
        filename = isinstance(path, (list, tuple)) and path[0] or path
        wsdl_path =  os.path.join(_ROOT, 'data', filename)
        with open(wsdl_path, 'r') as wsdl_file:
            pass  # just test that can be opened
    except Exception as e:
        try:
            import primestgplus
            wsdl_path = primestgplus.get_data(path)
            with open(wsdl_path, 'r') as wsdl_file:
                pass  # just test that can be opened
        except Exception as _:
            wsdl_path = False

    return wsdl_path
