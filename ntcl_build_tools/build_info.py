from .config import Config
from .debug_writer import debug_print

class BuildInfo (object):
    def __init__(this, name=None):
        if type(name) is list: this.name = name[0]
        else: this.name = name
        this.modules = []
        this.applications = []
        this.uses = []
        this.plugins = []
        this.base_plugins = []
        this.api = []
        this.tests = "none"
        this.flags = {}
        this.dependencies = {}

    def add_module(this, module):
        if type(module) is list: this.modules.extend(module)
        else: this.modules.append(module)

    def add_application(this, application):
        if type(application) is list: this.applications.extend(application)
        else: this.applications.append(application)

    def add_uses(this, uses):
        if type(uses) is list: this.uses.extend(uses)
        else: this.uses.append(uses)

    def add_tests(this, tests):
        if type(tests) is list: this.tests = tests[0]
        else: this.tests.tests = tests

    def add_flags(this, flags):
        for flag, values in flags.items():
            parts = flag.split(':')
            if len(parts) == 2 and parts[1] == 'dependencies':
                if type(values) is list: this.dependencies[parts[0]] = values
                else: this.dependencies[parts[0]] = [values]
            else:
                if type(values) is list: this.flags[flag] = values
                else: this.flags[flag] = [values]



    def add_plugins(this, plugins):
        if type(plugins) is list: this.plugins.extend(plugins)
        else: this.plugins.append(plugins)

    def add_base_plugins(this, base_plugins):
        if type(base_plugins) is list: this.base_plugins.extend(base_plugins)
        else: this.base_plugins.append(base_plugins)

    def add_api(this, api):
        if type(api) is list: this.api.extend(api)
        else: this.api.append(api)

    def has_flags(this): return len(this.flags.keys()) > 0
    def has_plugins(this): return len(this.plugins) > 0
    def has_base_plugins(this): return len(this.base_plugins) > 0
    def has_api(this): return len(this.api) > 0
    def has_applications(this): return len(this.applications) > 0

    def flag_in_plugins(this, flag):
        for module in this.flags[flag]:
            if module in this.plugins: return True
        return False

    def flag_in_base_plugins(this, flag):
        for module in this.flags[flag]:
            if module in this.base_plugins: return True
        return False

    def has_serial_tests(this):
        return this.tests == "serial"

    def has_distributed_tests(this):
        return this.tests == "distributed"

    def has_tests(this):
        return this.has_distributed_tests() or this.has_serial_tests()

    def module_in_flag(this, flag, module):
        if module in this.flags[flag]: return True
        return False

    def module_has_no_flag(this, module):
        for key, item in this.flags.items():
            if module in item: return False
        return True

    @classmethod
    def from_file(cls, filename):
        d = Config.from_file(filename)
        debug_print(d)

        if 'library_name' in d.keys():
            info = cls(d['library_name'])
        else: info = cls()

        if 'modules' in d.keys():
            info.add_module(d['modules'])

        if 'applications' in d.keys():
            info.add_application(d['applications'])

        if 'uses' in d.keys():
            info.add_uses(d['uses'])

        if 'tests' in d.keys():
            info.add_tests(d['tests'])

        if 'plugins' in d.keys():
            info.add_plugins(d['plugins'])

        if 'base_plugins' in d.keys():
            info.add_base_plugins(d['base_plugins'])

        if 'api' in d.keys():
            info.add_api(d['api'])

        for key in ['library_name', 'modules', 'applications', 'uses', 'tests', 'base_plugins', 'plugins', 'api']:
            if key in d.keys(): del d[key]

        info.add_flags(d)

        return info
