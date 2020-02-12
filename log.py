# _*_ coding:utf-8 _*_

from datetime import datetime
import os

class Log:

    def __init__(self, logfile='log', add_timestamp=True):
        self.new(logfile, add_timestamp)

    def new(self, logfile, add_timestamp=True):
        now = datetime.now()
        if add_timestamp:
            timestamp = now.strftime('%Y%m%d')
            self._logfile = f'{logfile}-{timestamp}.log'
        else:
            self._logfile = f'{logfile}.log'

    def write(self, *entry):
        with open(self._logfile, 'a') as f:
            now = datetime.now()
            timestamp = now.strftime('%Y/%m/%d %H:%M:%S')
            log_entry = '{}: {}\n'.format(timestamp, self._format(*entry))
            return f.write(log_entry)

    def _format(self, *entry):
        text = ''
        for item in entry:
            text += item.__str__()
            if entry.index(item) < len(text) + 1:
                text += ' '
        return text

    def clear(self):
        f = open(self._logfile, 'w')
        f.close()

    def delete(self):
        try:
            os.remove(self._logfile)
            return True
        except FileNotFoundError:
            return False

