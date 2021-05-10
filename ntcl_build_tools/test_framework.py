#!/usr/bin/env python3

from .unit_test_writer import UnitTestWriter, DistributedUnitTestWriter
from .package_test_writer import PackageTestWriter, DistributedPackageTestWriter
from .build_directory import BuildDirectory

class TestFramework(object):
    def __init__(this, modules, info):
        if info.has_serial_tests():
            this.tests = [PackageTestWriter(bdir) for bdir in BuildDirectory.list_all_test_directories(modules)]
            this.unittest = UnitTestWriter(info, modules, BuildDirectory.list_testapplication_directory())
        elif info.has_distributed_tests():
            this.tests = [DistributedPackageTestWriter(bdir) for bdir in BuildDirectory.list_all_test_directories(modules)]
            this.unittest = DistributedUnitTestWriter(info, modules, BuildDirectory.list_testapplication_directory())
        else:
            this.tests = []
            this.unittest = None

    def write_package_tests(this):
        for test in this.tests: test.write()

    def write_unittest_main(this):
        if this.unittest is not None: this.unittest.write()
