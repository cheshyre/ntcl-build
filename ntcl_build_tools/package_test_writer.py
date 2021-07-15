#!/usr/bin/env python3

import os

from .test_info import TestInfo
from .template_library import create_template_from_file
from .debug_writer import debug_print

class PackageTestBuilder(object):
    default_relative_template_directory = os.path.join('templates', 'test_templates')
    template_directory = template_path = os.path.join(os.path.dirname(__file__), default_relative_template_directory)
    package_test_template = os.path.join(template_directory, 'package_test.tpl')
    test_module_header = os.path.join(template_directory, 'test_module_header.tpl')
    run_test_header = os.path.join(template_directory, 'run_test_header.tpl')
    regular_test_template = os.path.join(template_directory, 'regular_test_suite.tpl')
    long_test_template = os.path.join(template_directory, 'long_test_suite.tpl')
    test_template = os.path.join(template_directory, 'test_skeleton.tpl')

    def __init__(this, name):
        this.name = name

    def get_filename(this): return this.name + '_package_test.f90'
    def get_test_filename(this, name): return name + '_test.f90'

    def create_module_header_line(this, test):
        return create_template_from_file(this.test_module_header).substitute(name=test)

    def create_run_header_line(this, test):
        return create_template_from_file(this.run_test_header).substitute(name=test)

    def create_regular_test_line(this, test):
        return create_template_from_file(this.regular_test_template).substitute(name=test)

    def create_long_test_line(this, test):
        return create_template_from_file(this.long_test_template).substitute(name=test)

    def create_module_header(this, info):
        s = '\n'
        for t in info.regular_tests:
            s += this.create_module_header_line(t)
        for t in info.long_tests:
            s += this.create_module_header_line(t)
        if len(s) is not 1: s += '\n'
        return s[:-1]

    def create_run_header(this, info):
        s = '\n'
        for t in info.regular_tests:
            s += this.create_run_header_line(t)
        for t in info.long_tests:
            s += this.create_run_header_line(t)
        if len(s) is not 1: s += '\n'
        return s[:-1]

    def create_test_suite(this, info):

        s = '\n'
        for t in info.regular_tests:
            s += this.create_regular_test_line(t) + '\n'

        if len(info.long_tests) is not 0: s += '        ! The following tests will not be run unless long is specified.' + '\n'
        for t in info.long_tests:
            s += this.create_long_test_line(t) + '\n'

        return s[:-1]
    def get_package_test(this, info):
        module_header = this.create_module_header(info)
        run_header = this.create_run_header(info)
        test_suite = this.create_test_suite(info)

        return create_template_from_file(this.package_test_template).substitute(
                name=this.name, module_header=module_header, run_header=run_header,
                test_suite=test_suite)

    def get_all_tests(this, info):
        tests = {}
        for t in info.regular_tests:
            tests[t] = this.get_test(t)
        for t in info.long_tests:
            tests[t] = this.get_test(t)

        return tests

    def get_test(this, name):
        return create_template_from_file(this.test_template).substitute(name=name)

class DistributedPackageTestBuilder(PackageTestBuilder):
    default_relative_template_directory = os.path.join('templates', 'test_templates')
    template_directory = template_path = os.path.join(os.path.dirname(__file__), default_relative_template_directory)
    run_test_header = os.path.join(template_directory, 'run_test_header.tpl')

    package_test_template = os.path.join(template_directory, 'distributed_package_test.tpl')
    test_module_header = os.path.join(template_directory, 'distributed_test_module_header.tpl')
    regular_test_template = os.path.join(template_directory, 'distributed_regular_test_suite.tpl')
    long_test_template = os.path.join(template_directory, 'distributed_long_test_suite.tpl')
    test_template = os.path.join(template_directory, 'distributed_test_skeleton.tpl')


class PackageTestWriter(object):
    infofile = 'test.info'

    def __init__(this, bdir):
        this.builder = PackageTestBuilder(bdir.name)
        this.path = bdir.path
        this.bdir = bdir

    def write(this):
        this.bdir.create_directory_if_it_does_not_exist()
        this.bdir.create_makefile_if_it_does_not_exist()

        info = TestInfo.from_file(os.path.join(this.path, this.infofile))

        this.write_package_test(info)
        this.write_unit_tests(info)

    def write_package_test(this, info):
        filename = os.path.join(this.path, this.builder.get_filename())
        debug_print(f'Writing package test to: {filename}')
        with open(filename, 'w') as fh: fh.write(this.builder.get_package_test(info))

    def write_unit_tests(this, info):
        tests = this.builder.get_all_tests(info)
        for name, content in tests.items():
            filename = os.path.join(this.path, this.builder.get_test_filename(name))
            debug_print(f'{filename} exists: {os.path.exists(filename)}')
            if not os.path.exists(filename):
                debug_print(f'Writing test to: {filename}')
                with open(filename, 'w') as fh: fh.write(content)

class DistributedPackageTestWriter(PackageTestWriter):
    infofile = 'test.info'

    def __init__(this, bdir):
        this.builder = DistributedPackageTestBuilder(bdir.name)
        this.path = bdir.path
        this.bdir = bdir

if __name__ == '__main__':
    import sys
    try:
        package_name = sys.argv[1]
        infofile = sys.argv[2]
    except:
        print(f"Usage: {os.path.basename(sys.argv[0])} package_name infofile")
        sys.exit(1)

    info = TestInfo.from_file(infofile)
    print(f'Package_name: {package_name}')
    print(f'infofile: {infofile}')
    print(info)

    builder = PackageTestBuilder(package_name)
    print(f'{builder.get_package_test(info)}')
    print(f'Filename: {builder.get_filename()}')
    tests = builder.get_all_tests(info)
    for k, v in tests.items():
        print(f'key: {k}')
        print(v)

