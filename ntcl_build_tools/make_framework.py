#!/usr/bin/env python3

from .makefile_writer import MakefileWriter

class MakeFramework(object):
    def __init__(this, info):
        this.writer = MakefileWriter(info)

    def write_makefile(this): this.writer.write()
