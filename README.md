# NTCL build tools
This repository contains scripts and resources to build the NTCL library.

## Prerequisites
- [make](https://www.gnu.org/software/make/)
- [gcc](http://icl.cs.utk.edu/magma/) (>=7.3)
- [Python3](https://www.python.org/)
- [GitPython](https://gitpython.readthedocs.io/en/stable/)

## Optional dependencies
- [BLAS](https://www.openblas.net/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- [cuTENSOR](https://developer.nvidia.com/cutensor)
- [MAGMA](http://icl.cs.utk.edu/magma/)

## Usage
- Get help with `-h`:
    ```
    bin/ntcl-build.py -h
    ```
- Compile default system in current directory:
    ```
    bin/ntcl-build.py -c
    ```
- Specify build directory with `-b`:
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl
    ```
- Specify system with `-s`:
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl -s ws.cuda
    ```
- List available systems (in system.d) using `-l`
    ```
    bin/ntcl-build.py -l
    ```
- Specify system using a system descriptor file with `-f` (for non-default systems):
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl -f FILENAME
    ```
- Update source from upstream repository wth `-u` (Can be combined with compilation):
    ```
    bin/ntcl-build.py -u -b /scratch/ntcl
    ```
- Specify release with `-r` (defaults and falls back to **main**):
   ```
   bin/ntcl-build.py -c -b /scratch/ntcl -r ntcl-0.1.0 -s ws.cuda
   ```
- Compile in a clean source tree with `-cl`:
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl -cl -s ws.cuda
    ```
- Compile tests with `-t`:
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl -cl -t -s ws.cuda
    ```
- Compile debug build with `-d`:
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl -cl -d -s ws.cuda
    ```
- Compile profiling build with `-p`:
    ```
    bin/ntcl-build.py -c -b /scratch/ntcl -cl -p -s ws.cuda
    ```
