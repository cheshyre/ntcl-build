HIP_COMPILER =  hipcc
HIP_STDFLAGS = -fdiagnostics-color=always
HIP_DEBUGFLAGS = --compiler-options=" ${HIP_STDFLAGS}, -O0, -g, -fbounds-check, -ftrapv, -rdynamic"
HIP_PRODFLAGS = --compiler-options="${HIP_STDFLAGS}, -O3"
HIP_COMPUTE_LEVEL=compute_30
HIP_CODE_LEVEL=
HIP_DEBUGFLAGS = -g -G
HIP_COMPFLAGS = --compiler-bindir=${HIP_GCC_DIR} --x=cu --gpu-architecture=${HIP_COMPUTE_LEVEL} --gpu-code=${HIP_CODE_LEVEL}
