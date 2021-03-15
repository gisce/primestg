from requests import post
import io
import base64

class ZivService(object):
    def __init__(self, cnc_url, user=None, password=None, sync=True):
        self.cnc_url = cnc_url
        self.sync = sync
        self.auth = None
        if user and password:
            self.auth = (user,password)

    def send_cycle(self, filename, cycle_filedata):
        """Send a cycle file to the concentrator service

        Keyword arguments:
        filename -- the name of our file (doesn't matter)
        cycle_filedata -- the file to send, encoded as a base64 string
        """
        filecontent = base64.b64decode(cycle_filedata)
        url = self.cnc_url + ('/' if (self.cnc_url[-1] != '/') else '') +'cct/cycles/'
        result = None
        if self.auth:
            result = post(url, files={'file': (filename, filecontent)}, auth=self.auth)
        else:
            result = post(url, files={'file': (filename, filecontent)})
        return result
