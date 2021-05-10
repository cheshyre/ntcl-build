COMPILER = gfortran
CCOMPILER = gcc
modcmd = -J
STANDARD = -std=f2008ts
STD_FLAGS = -fdiagnostics-color=always -Wall -Wextra
GCC10_FFLAGS = -fallow-argument-mismatch
GCCVERSION = $(shell gfortran --version | grep ^"GNU Fortran" | sed 's/^.* //g')
ifeq "$(GCCVERSION)" "10.2.0"
	STD_FLAGS += ${GCC10_FFLAGS}
endif
STD_CFLAGS = -Wall -Wextra
OPENMP_FLAGS =-fopenmp
PROD_FLAGS = -O3
DEBUG_FLAGS = -Og -g -fcheck=all -Wuse-without-only -fbacktrace -ffpe-trap=invalid,zero,overflow
DEBUG_CFLAGS = -Og -g -pedantic-errors -fcheck=all
PROFILE_FLAGS = -pg
STATIC_FLAGS = -static
OPTINFO_FLAGS= -fopt-info-all
