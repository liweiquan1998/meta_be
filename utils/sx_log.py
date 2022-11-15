# coding=utf-8
# Powered by SoaringNova Technology Company
import datetime
import sys


def format_print():
    class GeneralWriter:
        def __init__(self, *writers):
            self.writers = writers

        def write(self, buf):
            now = datetime.datetime.now()
            ts = '{},{}'.format(now.strftime('%Y-%m-%d %H:%M:%S'), '%03d' % (now.microsecond // 1000))
            for w in self.writers:
                for line in buf.rstrip().splitlines():
                    msg = line.rstrip()
                    if len(msg):
                        w.write('\033[1;32;1m{}| {}\033[0m\n'.format(ts, msg))

        def flush(self):
            pass

    sys.stdout = GeneralWriter(sys.stdout)
    sys.stderr = GeneralWriter(sys.stdout)
