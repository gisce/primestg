# coding=utf-8
import csv
from os.path import isfile
from os import access, R_OK
import io
import datetime
import re


class CycleFile(object):

    def __init__(self, path='', content=None):
        self.data = []
        if path and isfile(path) and access(path, R_OK):
            with io.open(path, encoding='utf-8') as fp:
                self.parse(fp)
        elif content is not None:
            with io.StringIO(content) as fp:
                self.parse(fp)

    def parse(self, fp):
        csvreader = csv.reader(fp, delimiter=';')
        for row in csvreader:
            # skip info header and tail
            if len(row) < 6:
                # TODO parse file date
                continue
            if row[0] == 'time':
                # header
                continue

            exec_date_str, reg_name, operation, obis, class_id, element_id, result_str = row[:7]
            action_return = None
            if len(row) > 7:
                action_return = row[-1]

            exec_date = datetime.datetime.strptime(exec_date_str, '%Y/%m/%d %H:%M:%S')
            clean_data = re.sub(
                'array|structure', '', re.sub('[{}]', '', re.sub('[a-z_]*\{([0-9/: ]+)\}', ';\\1', result_str))
            )
            data = clean_data.split(';')[1:]
            result = {
                'timestamp': exec_date,
                'reg_name': reg_name,
                'operation': operation,
                'obis': obis,
                'class_id': class_id and int(class_id) or None,
                'element_id': element_id and int(element_id) or None,
                'data': data
            }

            self.data.append(result)