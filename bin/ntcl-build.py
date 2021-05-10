#! /usr/bin/env python3

import os
import git
import subprocess
import glob

systemd = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "system.d"))

build = "ntcl-build"
util = "ntcl-util"
data = "ntcl-data"
tensor = "ntcl-tensor"
algorithms = "ntcl-algorithms"
examples = "ntcl-examples"
url_base="git@gitlab.com:ntcl/"

class System(object):
    def __init__(this, name, args=None):
        this.name = name
        this.modules = []
        this.environment_variables = {}

        this.parse_system_file(os.path.join(systemd, this.name))
        if args is not None:
            this.define_variable("DEBUG", args.debug)
            this.define_variable("PROFILE", args.profile)

    def parse_system_file(this, filename):
        with open(filename, 'r') as fh:
            lines = fh.readlines()

        for line in lines:
            line = line.partition('#')[0]
            try:
                key, value = [x.strip() for x in line.split('=')]
                if key == "modules": this.modules.extend(value.split())
                else: this.environment_variables[key] = value
            except: continue
    def has_modules(this): return len(this.modules) > 0
    def get_modules(this): return ' '.join(this.modules)

    def define_variable(this, name, define):
        if define: this.environment_variables[name] = "1"

    def __str__(this):
        s = f"System: {this.name}\n"
        if len(this.modules) > 0: s += '  modules: ' + this.get_modules() + '\n'
        for key, value in this.environment_variables.items():
            s += f'  {key}: {value}\n'

        return s[:-1]

def get_available_systems():
    return [os.path.basename(x) for x in glob.glob(f"{systemd}/*")]

def list_available_systems():
    print("Available systems:")
    for t in [System(x) for x in get_available_systems()]: print(t)

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

def get_all_repository_directories(directory):
    repository_names = [util, data, tensor,  algorithms, examples]
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

def clone_repositories_if_needed(directory):
    repository_names = [util, data, tensor,  algorithms, examples, build]
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
    repos = clone_repositories_if_needed(args.build_directory)
    if not args.update: return

    for r in repos: set_branch_and_update(r, args.release)

class Environment(object):
    def __init__(this, system, directory):
        this.system = system
        this.build_env = {**os.environ, 'NTCL_ROOT' : directory}

    def create_environment_script(this, directory):
        s = f"cd {directory}\n"
        if this.system.has_modules:
            # TODO: Switch to implementation specific stuff.
            s += 'source /etc/profile.d/modules.sh bash\n'
            s += 'module load ' + this.system.get_modules() + '\n'
        for key, value in this.system.environment_variables.items():
            s += f'export {key}={value}\n'

        return s

def create_environment(system, build_directory):
    return Environment(system, build_directory)

def run_make(directory, env, target):
    print(f"Running 'make {target}' in {directory}")
    cmd = env.create_environment_script(directory)
    cmd += f"make {target}\n"

    print(f"Command script:\n{cmd}")
    subprocess.run(cmd, shell=True, executable='/bin/bash', env=env.build_env)

def run_make_in_all_dirs(dirs, env, target):
    for d in dirs: run_make(d, env, target)

def prepare_and_compile_code(args):

    system = System(args.system, args)
    print(f"Compiling for system: {system}")

    build_directory = os.path.realpath(args.build_directory)
    env = create_environment(system, build_directory)
    dirs = get_all_repository_directories(build_directory)

    if args.clean: run_make_in_all_dirs(dirs, env, "clean")
    run_make_in_all_dirs(dirs, env, "libraries")
    if args.clean: run_make_in_all_dirs(dirs, env, "test")
    run_make_in_all_dirs(dirs, env, "apps")

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--system", choices=get_available_systems(), default="default",
            type=str.lower, help="System to compile for.")
    parser.add_argument("-b", "--build_directory", default=os.getcwd(), help="Directory to use for builds.")
    parser.add_argument("-r", "--release", default="main", help="Release to use for build.")
    parser.add_argument("-u", "--update", help="Update source.", action="store_true")
    parser.add_argument("-c", "--compile", help="Compile source.", action="store_true")
    parser.add_argument("-cl", "--clean", help="Compile in a clean source tree", action="store_true")
    parser.add_argument("-t", "--tests", help="Compile tests.", action="store_true")
    parser.add_argument("-l", "--list_systems", help="List available systems and exits.", action="store_true")
    parser.add_argument("-d", "--debug", help="Compile with debug flags.", action="store_true")
    parser.add_argument("-p", "--profile", help="Compile with profile flags.", action="store_true")
    args = parser.parse_args()

    if args.list_systems:
        list_available_systems()
        sys.exit(0)

    update_code(args)
    if args.compile: prepare_and_compile_code(args)
