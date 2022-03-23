#! /usr/bin/env python3

import os
import git
import subprocess
import glob

default_systemd = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "system.d/"))

build = "ntcl-build"
util = "ntcl-util"
data = "ntcl-data"
tensor = "ntcl-tensor"
algorithms = "ntcl-algorithms"
examples = "ntcl-examples"
part_lookup = {
    "build": build,
    "util": util,
    "data": data,
    "tensor": tensor,
    "algorithms": algorithms,
    "examples": examples,
}
url_base="https://github.com/cheshyre/"

class System(object):
    def __init__(this, name, path, args=None):
        this.name = name
        this.modules = []
        this.environment_variables = {}
        this.required_env_variables = []

        this.parse_system_file(os.path.join(path, this.name))
        if args is not None:
            this.define_variable("DEBUG", args.debug)
            this.define_variable("PROFILE", args.profile)

    def check_for_required(this):

        for key in this.required_env_variables:
            if key not in os.environ.keys():
                raise KeyError(f"Required environment variables are not defined: {this.get_required_env_variables()}")


    def parse_system_file(this, filename):
        with open(filename, 'r') as fh:
            lines = fh.readlines()

        for line in lines:
            line = line.partition('#')[0]
            try:
                key, value = [x.strip() for x in line.split('=')]
                if key == "modules": this.modules.extend(value.split())
                if key == "required_env_variables": this.required_env_variables.extend(value.split())
                else: this.environment_variables[key] = value
            except: continue
    def has_modules(this): return len(this.modules) > 0
    def get_modules(this): return ' '.join(this.modules)
    def get_required_env_variables(this): return ' '.join(this.required_env_variables)

    def define_variable(this, name, define):
        if define: this.environment_variables[name] = "1"

    def __str__(this):
        s = f"System: {this.name}\n"
        if len(this.modules) > 0: s += '  modules: ' + this.get_modules() + '\n'
        if len(this.required_env_variables) > 0: s += '  required_env_variables: ' + this.get_required_env_variables() + '\n'
        for key, value in this.environment_variables.items():
            s += f'  {key}: {value}\n'

        return s[:-1]

    @staticmethod
    def fromFile(filename, args):
        path, name = os.path.split(os.path.abspath(filename))
        return System(name, path, args)

def get_available_systems(path):
    return [os.path.basename(x) for x in glob.glob(f"{path}/*")]

def list_available_systems(path):
    print("Available systems:")
    for t in [System(x, path) for x in get_available_systems(path)]: print(t)

def create_directory_if_needed(directory):
    try:
        os.mkdir(directory)
    except:
        if os.path.isdir(directory):
            print(f"Directory already exists: {directory}")
            return
        raise
    print(f"Created directory: {directory}")

def get_repository_directory(directory, repository):
    return os.path.join(directory, repository)

def get_repository_url(repository):
    return url_base + repository + ".git"

def get_repository(directory, repository):
    return git.Repo(get_repository_directory(directory, repository))

def get_all_repository_directories(directory, part=None):
    if part is None:
        repository_names = [util, data, tensor,  algorithms, examples]
    elif part == "build":
        repository_names = []
    else:
        repository_names = [part_lookup[part]]
    return [get_repository_directory(directory, x) for x in repository_names]

def clone_repository(directory, repository):
    origin = get_repository_url(repository)
    d = get_repository_directory(directory, repository)

    print(f"Origin: {origin}")
    print(f"Repo directory: {d}")
    if os.path.exists(d): raise OSError(f"Directory already exists: {d}")

    return git.Repo.clone_from(origin, d)

def clone_repository_if_needed(directory, repository):
    try:
        repo = clone_repository(directory, repository)
    except IOError:
        repo = git.Repo(get_repository_directory(directory, repository))
        print(f"Repository already cloned: {repository}")

    print(f"Cloned repository {get_repository_url(repository)} into {directory}")
    return repo

def clone_repositories_if_needed(directory, part=None):
    if part is None:
        repository_names = [util, data, tensor,  algorithms, examples, build]
    else:
        try:
            repository_names = [part_lookup[part]]
        except KeyError:
            print(f"Error: \"{part}\" is not a valid NTCL subproject.", file=sys.stderr)
            print("Valid NTCL subprojects:", file=sys.stderr)
            print(", ".join([key for key in part_lookup]), file=sys.stderr)
            sys.exit(1)
    repositories = []
    for r in repository_names:
        repositories.append(clone_repository_if_needed(directory, r))

    return repositories

def set_branch_and_update(repository, branch):
    origin = repository.remote()
    origin.fetch()

    if branch in repository.branches:
        if repository.branches[branch] is not repository.active_branch:
            print(f"Local checkout: {branch}")
            repository.branches[branch].checkout()
        else: print(f"Branch already checked out: {branch}")
    elif branch in origin.refs:
        print(f"Remote checkout: {branch}")
        repository.git.checkout('-b', branch, origin.refs[branch])
    else:
        print(f"Branch does not exist: {branch}")

    origin.pull()

def update_code(args):
    create_directory_if_needed(args.build_directory)
    repos = clone_repositories_if_needed(args.build_directory, args.part)
    if not args.update: return

    for r in repos: set_branch_and_update(r, args.release)

class Environment(object):
    def __init__(this, system, directory):
        this.system = system
        this.build_env = {**os.environ, 'NTCL_ROOT' : directory}

    def create_environment_script(this, directory):
        s = f"cd {directory}\n"
        if this.system.has_modules():
            s += 'module load ' + this.system.get_modules() + '\n'
        for key, value in this.system.environment_variables.items():
            s += f'export {key}="{value}"\n'

        return s

def create_environment(system, build_directory):
    return Environment(system, build_directory)

def run_make(directory, env, target, dryrun):
    print(f"Running 'make {target}' in {directory}")
    cmd = env.create_environment_script(directory)
    cmd += f"make {target}\n"

    print(f"Command script:\n{cmd}")

    if not dryrun:
        subprocess.run(cmd, shell=True, executable='/bin/bash', env=env.build_env, check=True)

def run_make_in_all_dirs(dirs, env, target, dryrun):
    for d in dirs: run_make(d, env, target, dryrun)

def prepare_and_compile_code(args):

    if args.systemfile is not None:
        system = System.fromFile(args.systemfile, args)
    else:
        system = System(args.system, args.path, args)
    print(f"Compiling for system: {system}")

    system.check_for_required()

    build_directory = os.path.realpath(args.build_directory)
    env = create_environment(system, build_directory)
    dirs = get_all_repository_directories(build_directory, args.part)

    if args.clean: run_make_in_all_dirs(dirs, env, "clean", args.dryrun)
    run_make_in_all_dirs(dirs, env, "libraries", args.dryrun)
    if args.tests: run_make_in_all_dirs(dirs, env, "test", args.dryrun)
    run_make_in_all_dirs(dirs, env, "apps", args.dryrun)

def prepare_and_clean_code(args):

    if args.systemfile is not None:
        system = System.fromFile(args.systemfile, args)
    else:
        system = System(args.system, args.path, args)
    print(f"Compiling for system: {system}")

    system.check_for_required()

    build_directory = os.path.realpath(args.build_directory)
    env = create_environment(system, build_directory)
    dirs = get_all_repository_directories(build_directory, args.part)

    run_make_in_all_dirs(dirs, env, "clean", args.dryrun)

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-s", "--system", default="default",
            type=str.lower, help="System to compile for.")
    group.add_argument("-f", "--systemfile", help="Specify the system file to use.")

    parser.add_argument("--path", default=default_systemd, help="Path to look for system files.")
    parser.add_argument("-b", "--build_directory", default=os.getcwd(), help="Directory to use for builds.")
    parser.add_argument("-r", "--release", default="main", help="Release to use for build.")
    parser.add_argument("-u", "--update", help="Update source.", action="store_true")
    parser.add_argument("-c", "--compile", help="Compile source.", action="store_true")
    parser.add_argument("-cl", "--clean", help="Compile in a clean source tree", action="store_true")
    parser.add_argument("-t", "--tests", help="Compile tests.", action="store_true")
    parser.add_argument("-l", "--list_systems", help="List available systems and exits.", action="store_true")
    parser.add_argument("-d", "--debug", help="Compile with debug flags.", action="store_true")
    parser.add_argument("-p", "--profile", help="Compile with profile flags.", action="store_true")
    parser.add_argument("-n", "--dryrun", help="Dry run, does nothing but print messages.", action="store_true")
    parser.add_argument("-x", "--part", default=None, help="Only run ntcl-build on specific part of NTCL.")
    args = parser.parse_args()

    if args.list_systems:
        list_available_systems(os.path.abspath(args.path))
        sys.exit(0)

    update_code(args)
    if args.compile: prepare_and_compile_code(args)
    elif args.clean: prepare_and_clean_code(args)
