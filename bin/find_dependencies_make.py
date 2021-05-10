"""Find all modules
    - Loop through all fortran files
        - Store all module, file combos in a dict.
        - Store all dependencies in a dict.
        - Match files with dependencies and print"""

from glob import glob
import re, sys, os
def get_filenames(wildcard):
    return glob(wildcard)

def find_module_name(text):
    m = re.search('end module.(?P<name>.*)', text, re.IGNORECASE)
    if not m:
        m = re.search('^program.(?P<name>.*)\n', text, re.IGNORECASE)
    return m.group('name').strip()

def find_module_dependencies(text):
    return re.findall('\s*use\s+::\s+(?P<module_name>.*?)\W', text, re.IGNORECASE)


def parse_file(f):
    with open(f, "r") as fh:
        text = fh.read()
    module_name = find_module_name(text)
    dependencies = find_module_dependencies(text)
    return module_name, dependencies

def parse_files(directory):
    files = {}
    dependencies = {}
    for f in get_filenames(os.path.join(directory, "*.f90")) + get_filenames(os.path.join(directory, "*.F90")) :
        try:
            module_name, module_dependencies = parse_file(f)
            object_file = f.split(".")[0] + ".o"
            files[module_name] = object_file
            dependencies[module_name] = module_dependencies
        except: pass
    return files, dependencies

if __name__ == "__main__":
    try:
        directory = sys.argv[1]
    except:
        print usage
        sys.exit(1)

    files, dependencies = parse_files(directory)

    for key, values in dependencies.items():
        s = "%s :" % files[key]
        for val in values:
            if val in files.keys():
                s += " %s" % files[val]
        print s
