#!/usr/bin/env python3

import os, sys
from ntcl_build_tools import BuildFramework

if __name__ == "__main__":
    try:
        infofile = sys.argv[1]
    except:
        print(f"Usage: {os.path.basename(sys.argv[0])} infofile")
        sys.exit(1)

    build = BuildFramework.from_file(infofile)
    build.write_structure()
