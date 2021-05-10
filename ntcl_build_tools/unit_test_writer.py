#!/usr/bin/env python3

import os
from .build_directory import BuildDirectory
from .debug_writer import debug_print
from .template_library import create_template_from_file

class UnitTestBuilder(object):
    default_relative_template_directory = os.path.join('templates', 'test_templates')
    template_directory = template_path = os.path.join(os.path.dirname(__file__), default_relative_template_directory)
    unittest_template = os.path.join(template_directory, 'unittest_template.tpl')
    module_header_template = os.path.join(template_directory, 'package_test_module_header.tpl')
    run_header_template = os.path.join(template_directory, 'run_package_test_header.tpl')
    run_statements_template = os.path.join(template_directory, 'package_test_run_statements.tpl')
    ntcl_data_module_header_template = os.path.join(template_directory, 'unittest_ntcl-data-module_header.tpl')
    ntcl_data_run_template = os.path.join(template_directory, 'unittest_ntcl-data_run.tpl')
    ntcl_data_final_template = os.path.join(template_directory, 'unittest_ntcl-data_final.tpl')

    def __init__(this, info, names):
        this.info = info
        this.names = names

    def get_filename(this):
        if ( this.info.has_flags() ) : return 'unittest.F90'
        else: return 'unittest.f90'

    def get_module_header(this):
        s = ''
        module = None
        if "ntcl-algorithms" in this.info.uses or this.info.name=="ntcl-algorithms":
            module = "algorithms"
        elif "ntcl-data" in this.info.uses or this.info.name=="ntcl-data":
            module = "data"

        if module is not None:
            s += create_template_from_file(
                    this.ntcl_data_module_header_template).substitute(module=module) + "\n"

        if ( this.info.has_flags() ) : s += this.get_module_header_with_flags()
        else: s += this.get_module_header_without_flags(this.info.modules)

        return s

    def get_module_header_without_flags(this, names):
        s = ''
        for name in names:
            s += create_template_from_file(
                    this.module_header_template).substitute(name=name)

        return s

    def get_module_header_with_flags(this):
        s = ''
        for flag in this.info.flags.keys():
            if not this.info.flag_in_base_plugins(flag): continue
            s += f'#ifdef {flag}\n'
            s += this.get_module_header_for_flag(flag, this.info.base_plugins)
            s += '#endif\n\n'

        s += this.get_module_header_without_flags(this.info.modules) + "\n"

        for flag in this.info.flags.keys():
            if not this.info.flag_in_plugins(flag): continue
            s += f'#ifdef {flag}\n'
            s += this.get_module_header_for_flag(flag, this.info.plugins)
            s += '#endif\n\n'

        if this.info.has_api():
            s += this.get_module_header_without_flags(this.info.api) + "\n"

        return s[:-1]

    def get_module_header_for_flag(this, flag, names):
        s = ''
        for name in names:
            if ( this.info.module_in_flag(flag, name) ):
                s += create_template_from_file(
                        this.module_header_template).substitute(name=name)

        return s

    def get_run_header(this):
        if ( this.info.has_flags() ) : return this.get_run_header_with_flags()
        else: return this.get_run_header_without_flags(this.info.modules)

    def get_run_header_without_flags(this, names):
        s = ''
        for name in names:
            s += create_template_from_file(
                    this.run_header_template).substitute(name=name)
        return s

    def get_run_header_with_flags(this):
        s = ''
        for flag in this.info.flags.keys():
            if not this.info.flag_in_base_plugins(flag): continue
            s += f'#ifdef {flag}\n'
            s += this.get_run_header_for_flag(flag, this.info.base_plugins)
            s += '#endif\n\n'

        s += this.get_run_header_without_flags(this.info.modules) + "\n"

        for flag in this.info.flags.keys():
            if not this.info.flag_in_plugins(flag): continue
            s += f'#ifdef {flag}\n'
            s += this.get_run_header_for_flag(flag, this.info.plugins)
            s += '#endif\n\n'

        if this.info.has_api():
            s += this.get_run_header_without_flags(this.info.api) + "\n"

        return s[:-1]

    def get_run_header_for_flag(this, flag, names):
        s = ''
        for name in names:
            if ( this.info.module_in_flag(flag, name) ):
                s += create_template_from_file(
                        this.run_header_template).substitute(name=name)

        return s

    def get_run_statements(this):
        s = ''

        module = None
        if "ntcl-algorithms" in this.info.uses or this.info.name=="ntcl-algorithms":
            module = "algorithms"
        elif "ntcl-data" in this.info.uses or this.info.name=="ntcl-data":
            module = "data"

        if module is not None:
            s += create_template_from_file(
                    this.ntcl_data_run_template).substitute(module=module) + "\n"

        if ( this.info.has_flags() ) : s += this.get_run_statements_with_flags()
        else: s += this.get_run_statements_without_flags(this.info.modules)

        if module is not None:
            s += "\n" + create_template_from_file(
                    this.ntcl_data_final_template).substitute(module=module)

        return s

    def get_run_statements_without_flags(this, names):
        s = ''
        for name in names:
            s += create_template_from_file(
                    this.run_statements_template).substitute(name=name) + "\n"
        return s[:-1]

    def get_run_statements_with_flags(this):
        s = ''
        for flag in this.info.flags.keys():
            if not this.info.flag_in_base_plugins(flag): continue
            s += f'#ifdef {flag}\n'
            s += this.get_run_statements_for_flag(flag, this.info.base_plugins)
            s += '#endif\n\n'

        s += this.get_run_statements_without_flags(this.info.modules) + "\n"

        for flag in this.info.flags.keys():
            if not this.info.flag_in_plugins(flag): continue
            s += f'#ifdef {flag}\n'
            s += this.get_run_statements_for_flag(flag, this.info.plugins)
            s += '#endif\n\n'

        if this.info.has_api():
            s += this.get_run_statements_without_flags(this.info.api) + "\n"

        return s[:-1]

    def get_run_statements_for_flag(this, flag, names):
        s = ''
        for name in names:
            if ( this.info.module_in_flag(flag, name) ):
                s += create_template_from_file(
                        this.run_statements_template).substitute(name=name) + "\n"

        return s[:-1]


    def get_content(this):
        module_header = this.get_module_header()
        run_header = this.get_run_header()
        run_statements = this.get_run_statements()

        return create_template_from_file(this.unittest_template).substitute(
                module_header=module_header, run_header=run_header,
                run_statements=run_statements)

class DistributedUnitTestBuilder(UnitTestBuilder):
    default_relative_template_directory = os.path.join('templates', 'test_templates')
    template_directory = template_path = os.path.join(os.path.dirname(__file__), default_relative_template_directory)
    module_header_template = os.path.join(template_directory, 'package_test_module_header.tpl')
    run_header_template = os.path.join(template_directory, 'run_package_test_header.tpl')

    unittest_template = os.path.join(template_directory, 'distributed_unittest_template.tpl')
    run_statements_template = os.path.join(template_directory, 'distributed_package_test_run_statements.tpl')

class UnitTestWriter(object):
    def __init__(this, info, names, bdir):
        this.builder = UnitTestBuilder(info, names)
        this.bdir = bdir

    def write(this):
        this.bdir.create_directory_if_it_does_not_exist()
        this.bdir.create_makefile_if_it_does_not_exist()

        filename = os.path.join(this.bdir.path, this.builder.get_filename())
        debug_print(f'Write unittest to: {filename}')
        with open(filename, 'w') as fh: fh.write(this.builder.get_content())

class DistributedUnitTestWriter(UnitTestWriter):
    def __init__(this, info, names, bdir):
        this.builder = DistributedUnitTestBuilder(info, names)
        this.bdir = bdir

if __name__ == '__main__':
    names = ['test1', 'test2', 'test3']
    bdir = BuildDirectory('test', './test', True, True)

    writer = UnitTestWriter(None, names, bdir)
    writer.write()

