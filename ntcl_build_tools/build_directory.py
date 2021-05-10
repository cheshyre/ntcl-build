#!/usr/bin/env python3

import os
from .debug_writer import debug_print

class BuildDirectory(object):
    default_relative_template_directory = os.path.join('templates', 'build_templates')
    default_source_directory = 'src'
    default_modules_directory = os.path.join(default_source_directory, 'modules')
    default_applications_directory = os.path.join(default_source_directory, 'modules')
    default_test_directory = os.path.join(default_source_directory, 'test')
    default_unittest_directory = os.path.join(default_test_directory, 'unittest')
    default_module_makefile = 'makefile.mk'
    template_path = os.path.join(os.path.dirname(__file__), default_relative_template_directory)

    def __init__(this, name, path, is_test=False, is_executable=False):
        this.name = name
        this.path = path
        this.is_test = is_test
        this.is_executable = is_executable

    def create_directory_if_it_does_not_exist(this):
        if os.path.isdir(this.path):
            debug_print(f'Directory exists: {this.path}')
            return

        if os.path.exists(this.path):
            raise Exception(f'Can not create directory: {this.path}')

        debug_print(f'Creating dir: {this.path}')
        os.makedirs(this.path)

    def create_makefile_if_it_does_not_exist(this):
        makefile_name = os.path.join(this.path, this.default_module_makefile)

        if os.path.isfile(makefile_name):
            debug_print(f'Makefile exists: {makefile_name}')
            return

        if os.path.exists(makefile_name):
            raise Exception(f'Makefile exists, but is not a file: {makefile_name}')

        debug_print(f'Creating makefile: {makefile_name}')
        with open(makefile_name, 'w') as fh : fh.write(this.get_makefile_content())

    def create_makefile(this):
        makefile_name = os.path.join(this.path, this.default_module_makefile)

        debug_print(f'Creating makefile: {makefile_name}')
        with open(makefile_name, 'w') as fh : fh.write(this.get_makefile_content())

    def get_makefile_content(this):
        if this.is_test:
            if this.is_executable: postfix='test_executable'
            else: postfix = 'test_library'
        else:
            if this.is_executable: postfix='executable'
            else: postfix = 'library'

        filename = os.path.join(this.template_path, 'makefile.' + postfix)

        with open(filename, 'r') as fh: makefile = fh.read()
        return makefile

    @classmethod
    def list_all_source_directories(cls, modules, applications=[]):
        directories = cls.list_all_library_directories(modules)
        directories.extend(cls.list_all_test_directories(modules))
        directories.append(cls.list_testapplication_directory())
        directories.extend(cls.list_all_application_directories(applications))

        return directories

    @classmethod
    def list_all_test_directories(cls, modules):
        directories = []
        for m in modules:
            directories.append(cls(m, os.path.join(cls.default_test_directory, m), is_test=True))

        return directories

    @classmethod
    def list_all_library_directories(cls, modules):
        directories = []
        for m in modules:
            directories.append(cls(m, os.path.join(cls.default_modules_directory, m)))

        return directories

    @classmethod
    def list_testapplication_directory(cls):
        return cls('unittest', cls.default_unittest_directory, is_test=True, is_executable=True)

    @classmethod
    def list_all_application_directories(cls, applications):
        directories = []

        for a in applications:
            directories.append(cls(a, os.path.join(cls.default_applications_directory, a), is_executable=True))
        return directories

    @staticmethod
    def create_source_directories_if_necessary(modules):
        for d in BuildDirectory.list_all_source_directories(modules):
            d.create_directory_if_it_does_not_exist()

    @staticmethod
    def create_makefiles_in_source_directories_if_necessary(modules):
        for d in BuildDirectory.list_all_source_directories(modules):
            d.create_makefile_if_it_does_not_exist()
