#!/usr/bin/env python3

#"""Find all modules
#    - Loop through all fortran files
#        - Store all module, file combos in a dict.
#        - Store all dependencies in a dict.
#        - Match files with dependencies and print"""

from glob import glob
import re, sys, os

def get_filenames(wildcard):
    return glob(wildcard)

def find_module_names(text):
    modules = re.findall('end module\s+(?P<name>.*)\W', text, re.IGNORECASE)
    m = re.search('end program\s+(?P<name>.*)\W', text, re.IGNORECASE)
    if m is not None: modules.append(m.group('name').strip())
    return [x for x in modules if len(x) > 0]

def find_module_dependencies(text):
    deps = re.findall('\s*use\s+::\s+(?P<module_name>.*?)\W', text, re.IGNORECASE)
    deps.extend(re.findall('\s*use\s+(?P<module_name>.*?)\W', text, re.IGNORECASE))
    return deps


def find_a_module(text, name):
    pattern = r'(program|module)\s+' + name
    limits = [x.start() for x in re.finditer(pattern, text, re.IGNORECASE)]
    if len(limits) != 2: raise ValueError("Not a valid module")
    return text[limits[0]:limits[1]]

def parse_file(f):
    with open(f, "r") as fh:
        text = fh.read()
    #if f != "src/modules/tbi/tbi-constants.f90": return "", ""
    dependencies = []
    module_names = find_module_names(text)
    for name in module_names:
        dependencies.append(find_module_dependencies(find_a_module(text, name)))
    return module_names, dependencies

def parse_files(directory):
    files = {}
    dependencies = {}
    for f in get_filenames(os.path.join(directory, "*.f90")) + get_filenames(os.path.join(directory, "*.F90")) :
        object_file = f.split(".")[0] + ".o"
        module_names, module_dependencies = parse_file(f)
        for name, dep in zip(module_names, module_dependencies):
            files[name] = object_file
            dependencies[name] = dep
    return files, dependencies

if __name__ == "__main__":
    try:
        directory = sys.argv[1]
    except:
        print(usage)
        sys.exit(1)

    files, dependencies = parse_files(directory)
    object_dependencies = {}

    for key, values in dependencies.items():
        o = files[key]
        if o not in object_dependencies.keys(): object_dependencies[o] = []
        for v in values:
            if v in files.keys():
                d = files[v]
                if d not in object_dependencies[o] and d != o:
                    object_dependencies[o].append(d)

    for f, d in object_dependencies.items():
        if len(d) == 0: continue
        s = "%s :" % f
        s += ' '.join(d)
        print(s)
