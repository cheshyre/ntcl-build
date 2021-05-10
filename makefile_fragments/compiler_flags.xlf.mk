COMPILER = xlf2008_r
CCOMPILER = xlc
modcmd = -qmoddir=
#STANDARD = -qlanglvl=tspure
STD_FLAGS = -qessl
STD_CFLAGS = -Wall -Wextra
OPENMP_FLAGS =-qsmp=omp
PROD_FLAGS = -O3
DEBUG_FLAGS = -O0 -g -qcheck=all -qflttrap=enable:invalid:nanq:overflow:underflow:zerodivide
DEBUG_CFLAGS = -O0 -g -qcheck=all
PROFILE_FLAGS = -pg -O3
