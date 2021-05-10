#!/usr/bin/env python3

from .build_info import BuildInfo
from .test_framework import TestFramework
from .library_framework import LibraryFramework
from .application_framework import ApplicationFramework
from .make_framework import MakeFramework

class BuildFramework(object):
    def __init__(this, info):
        this.libraries = LibraryFramework(info.base_plugins + info.modules + info.plugins + info.api)
        this.tests =  TestFramework(info.base_plugins + info.modules + info.plugins + info.api, info)
        this.make = MakeFramework(info)
        this.applications = ApplicationFramework(info.applications)

    def update_test_framework(this):
        this.tests.write_package_tests()
        this.tests.write_unittest_main()

    def update_makefile(this):
        this.make.write_makefile()

    def write_structure(this):
        this.libraries.write_packages()
        this.applications.write_packages()
        this.update_test_framework()
        this.update_makefile()

    @classmethod
    def from_file(cls, filename):
        return BuildFramework(BuildInfo.from_file(filename))


