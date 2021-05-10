 #!/usr/bin/env python3

class PackageWriter(object):
    def __init__(this, bdir):
        this.bdir = bdir

    def write(this):
        this.bdir.create_directory_if_it_does_not_exist()
        this.bdir.create_makefile()
