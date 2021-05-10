#!/usr/bin/env python3

from .config import Config
from .debug_writer import debug_print

class TestInfo (object):
    def __init__(this):
        this.regular_tests = []
        this.long_tests = []

    def add_regular_test(this, regular_test):
        if type(regular_test) is list: this.regular_tests.extend(regular_test)
        else: this.regular_tests.append(regular_test)

    def add_long_test(this, long_test):
        if type(long_test) is list: this.long_tests.extend(long_test)
        else: this.long_tests.append(long_test)

    @classmethod
    def from_file(cls, filename):
        info = cls()

        d = Config.from_file(filename)
        debug_print(f'From configfile: {d}')

        if 'regular_tests' in d.keys():
            info.add_regular_test(d['regular_tests'])

        if 'long_tests' in d.keys():
            info.add_long_test(d['long_tests'])

        return info

if __name__ == '__main__':
    import sys
    try:
        infofile = sys.argv[1]
    except:
        print(f"Usage: {os.path.basename(sys.argv[0])} infofile")
        sys.exit(1)

    print(f'infofile: {infofile}')
    info = TestInfo.from_file(infofile)
    print(f'Regular tests: {info.regular_tests}')
    print(f'Long tests: {info.long_tests}')

