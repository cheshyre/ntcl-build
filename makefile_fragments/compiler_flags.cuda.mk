NV_COMPILER =  nvcc
NV_STDFLAGS = -fdiagnostics-color=always, -Wall, -Wextra, -ansi
NV_DEBUGFLAGS = ${NV_STDFLAGS}, -O0, -g, -fbounds-check, -ftrapv, -rdynamic
NV_PRODFLAGS = ${NV_STDFLAGS}, -O3
NV_COMPFLAGS = --compiler-bindir=${CUDA_GCC_DIR}
CUDA_DEBUGFLAGS = -g -G
