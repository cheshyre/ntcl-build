#!/usr/bin/env python3

from .package_writer import PackageWriter
from .build_directory import BuildDirectory

class LibraryFramework(object):
    def __init__(this, names):
        this.packages = [PackageWriter(bdir) for bdir in BuildDirectory.list_all_library_directories(names)]

    def write_packages(this):
        for package in this.packages: package.write()

