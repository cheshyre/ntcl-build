#!/usr/bin/env python3

import os
import shutil

from .debug_writer import debug_print
from .template_library import create_template_from_file
from .build_directory import BuildDirectory

class MakefileBuilder(object):
    default_relative_template_directory = os.path.join('templates', 'build_templates')
    template_directory = template_path = os.path.join(os.path.dirname(__file__), default_relative_template_directory)
    makefile_template = os.path.join(template_directory, 'makefile.tpl')
    makefile_module_template = os.path.join(template_directory, 'makefile.modules')
    makefile_testmodule_template = os.path.join(template_directory, 'makefile.testmodules')

    known_external_includes = {
            'mpi'                           : '${INCMPI}',
            'hdf5'                          : '${INCHDF5}',
            'blas'                          : '${INCBLAS}',
            'cutensor'                      : '-I${CUTENSOR_ROOT}/include',
            'magma'                         : '-I${MAGMA_ROOT}/include',
            'rocblas'                       : '-I${ROCM_PATH}/rocblas/include'
            }

    known_internal_includes = {
            'ntcl-util'                     : '${NTCL_ROOT}/ntcl-util/include',
            'ntcl-data'                     : '${NTCL_ROOT}/ntcl-data/include',
            'ntcl-tensor'                   : '${NTCL_ROOT}/ntcl-tensor/include',
            'ntcl-algorithms'               : '${NTCL_ROOT}/ntcl-algorithms/include'
            }

    known_includes = {**known_internal_includes, **known_external_includes}

    known_libs = {
            'ntcl-util'                     : '${NTCL_ROOT}/ntcl-util/lib/libntcl-util.a',
            'ntcl-data'                     : '${NTCL_ROOT}/ntcl-data/lib/libntcl-data.a',
            'ntcl-tensor'                   : '${NTCL_ROOT}/ntcl-tensor/lib/libntcl-tensor.a',
            'ntcl-algorithms'               : '${NTCL_ROOT}/ntcl-algorithms/lib/libntcl-algorithms.a',
            'mpi'                           : '${LIBMPI}',
            'hdf5'                          : '${LIBHDF5}',
            'blas'                          : '${LIBBLAS}',
            'cublas'                        : '-L${CUDA_ROOT}/lib64 -lcublas',
            'magma'                         : '-L${MAGMA_ROOT}/lib -lmagma',
            'cutensor'                      : '-L${CUTENSOR_ROOT}/lib -lcutensor',
            'cuda'                          : '-L${CUDA_ROOT}/lib64 -lcudart -lcuda -lstdc++',
            'hip_amd'                       : '-L${HIP_PATH}/lib -lamdhip64 -lstdc++',
            'rocblas'                       : '-L${ROCM_PATH}/rocblas/lib -lrocblas -ldl'
            }


    def __init__(this, info):
        this.info = info

    def get_filename(this): return "Makefile"

    def get_all_modules(this): return ' '.join(this.info.modules)

    def get_modules(this, flag, all_modules):
        modules = []
        for m in all_modules:
            if ( this.info.module_in_flag(flag, m) ): modules.append(m)
        return ' '.join(modules)

    def get_applications(this):
        return ' '.join(this.info.applications)

    def get_test_modules(this):
        if this.info.has_tests():
            return BuildDirectory.list_testapplication_directory().name
        else: return ''

    def get_api_modules(this):
        return ' '.join(this.info.api)

    def get_internal_include_directories(this):
        s = ''
        for inc in this.info.uses:
            if inc in this.known_internal_includes:
                s += this.known_internal_includes[inc] + ' '
        return s[:-1]

    def get_external_include_directories(this):
        s = ''
        for inc in this.info.uses:
            if inc in this.known_external_includes:
                s += this.known_external_includes[inc] + ' '
        return s[:-1]

    def get_optional(this, flag, deps):
        s = ['']
        s.append(f'ifdef {flag}')
        dirs = []
        for inc in deps:
            if inc in this.known_includes:
                dirs.append(this.known_includes[inc])
        libs = []
        for lib in deps:
            if lib in this.known_libs: libs.append(this.known_libs[lib])

        if len(dirs) > 0: s.append(f'external_include += {" ".join(dirs)}')
        s.append(f'external_libraries += {" ".join(libs)}')
        s.append('endif')
        return s

    def get_optional_for_hip(this, flag, deps):
        idx = deps.index('hip')

        deps[idx] = 'hip_amd'
        s = ['']
        dirs = []
        for inc in deps:
            if inc in this.known_includes:
                dirs.append(this.known_includes[inc])
        libs = []
        for lib in deps:
            if lib in this.known_libs: libs.append(this.known_libs[lib])

        s.append(f'ifdef {flag}')
        s.append('ifeq (${HIP_PLATFORM},amd)')
        if len(dirs) > 0: s.append(f'external_include += {" ".join(dirs)}')
        s.append(f'external_libraries += {" ".join(libs)}')
        s.append('endif')
        s.append('')

        deps[idx] = 'cuda'
        dirs = []
        for inc in deps:
            if inc in this.known_includes:
                dirs.append(this.known_includes[inc])
        libs = []
        for lib in deps:
            if lib in this.known_libs: libs.append(this.known_libs[lib])

        s.append('ifeq (${HIP_PLATFORM},nvidia)')
        if len(dirs) > 0: s.append(f'external_include += {" ".join(dirs)}')
        s.append(f'external_libraries += {" ".join(libs)}')
        s.append('endif')
        s.append('endif')

        deps[idx] = 'hip'
        return s

    def get_optional_dependencies(this):
        if not this.info.dependencies: return ''
        lines = []
        for flag,deps in this.info.dependencies.items():
            print(f"hip in deps: {'hip' in deps}")
            if "hip" in deps: s = this.get_optional_for_hip(flag, deps)
            else: s = this.get_optional(flag, deps)
            lines.extend(s)
        return '\n'.join(lines)

    def get_libraries(this):
        s = ''
        for lib in this.info.uses:
            if lib in this.known_libs:
                s += this.known_libs[lib] + ' '
        return s[:-1]

    def get_library_name(this):
        if this.info.name is not None: return f'library_name := lib{this.info.name}.a'
        else: return f'library_name := '

    def get_module_block(this):
        test_modules = this.get_test_modules()

        module_block = ''
        for flag in this.info.flags.keys():
            if not this.info.flag_in_base_plugins(flag): continue
            s = f'ifdef {flag}\n'
            modules = this.get_modules(flag, this.info.base_plugins)
            s += create_template_from_file(this.makefile_module_template).substitute(
                    modules=modules)
            if this.info.has_tests():
                s += create_template_from_file(this.makefile_testmodule_template).substitute(
                        test_modules=modules)

            s+= f'FFLAGS += -D{flag}\n'
            s += 'endif\n'
            module_block += s + '\n'

        modules = this.get_all_modules()
        module_block += create_template_from_file(this.makefile_module_template).substitute(modules=modules)
        if this.info.has_tests():
            module_block += create_template_from_file(this.makefile_testmodule_template).substitute(test_modules=modules) + "\n"

        for flag in this.info.flags.keys():
            if not this.info.flag_in_plugins(flag): continue
            s = f'ifdef {flag}\n'
            modules = this.get_modules(flag, this.info.plugins)
            s += create_template_from_file(this.makefile_module_template).substitute(
                    modules=modules)
            if this.info.has_tests():
                s += create_template_from_file(this.makefile_testmodule_template).substitute(
                        test_modules=modules)

            s+= f'FFLAGS += -D{flag}\n'
            s += 'endif\n'
            module_block += s + '\n'

        if this.info.has_api():
            modules = this.get_api_modules()
            module_block += create_template_from_file(this.makefile_module_template).substitute(modules=modules)
            if this.info.has_tests():
                module_block += create_template_from_file(this.makefile_testmodule_template).substitute(test_modules=modules) + "\n"

        if this.info.has_applications():
            modules = this.get_applications()
            module_block += create_template_from_file(this.makefile_module_template).substitute(modules=modules) + '\n'

        module_block += create_template_from_file(this.makefile_testmodule_template).substitute(
                    test_modules=test_modules)
        return module_block

    def get_content(this):
        module_block = this.get_module_block()
        library_name = this.get_library_name()
        internal_include_directories = this.get_internal_include_directories()
        external_include_directories = this.get_external_include_directories()

        # TODO: Make sure to get the libraries in the correct order. Introduce dependencies.
        libraries = this.get_libraries()

        optional_dependencies = this.get_optional_dependencies()

        return create_template_from_file(this.makefile_template).substitute(
                module_block=module_block, library_name=library_name,
                internal_include_directories=internal_include_directories,
                external_include_directories=external_include_directories,
                libraries=libraries, optional_dependencies=optional_dependencies )

class MakefileWriter(object):
    def __init__(this, info):
        this.builder = MakefileBuilder(info)

    def write(this):
        filename = this.builder.get_filename()
        debug_print(f'Makefile filename: {filename}')
        debug_print(f'{filename} exists: {os.path.exists(filename)}')
        if os.path.exists(filename):
            debug_print(f'Writing old Makefile: {filename}.old')
            shutil.copy(filename, filename + '.old')

        debug_print(f'Writing Makefile: {filename}')
        with open(filename, 'w') as fh: fh.write(this.builder.get_content())
