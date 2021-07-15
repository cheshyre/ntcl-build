include ${MAKEINC}/applications.mk

ifndef system
	system := gcc
endif

ifndef compiler_suite
	compiler_suite := gcc
endif

ifndef OPENMP
	OPENMP := yes
endif

include ${MAKEINC}/compiler_flags.${compiler_suite}.mk
ifdef force_compiler
	COMPILER := ${force_compiler}
endif

ifdef force_ccompiler
	CCOMPILER := ${force_ccompiler}
endif

ifdef enforce_standard
	STANDARD = ${enforce_standard}
endif
FFLAGS = ${STD_FLAGS} ${STANDARD}
CFLAGS = ${STD_CFLAGS}

ifeq ($(OPENMP),yes)
    FFLAGS += ${OPENMP_FLAGS}
	CFLAGS += ${OPENMP_FLAGS}
endif

ifdef extra_flags
	FFLAGS += ${extra_flags}
	CFLAGS += ${extra_flags}
endif

ifdef USE_LD
	FFLAGS += ${ldcmd}${USE_LD}
	CFLAGS += ${ldcmd}${USE_LD}
endif

ifdef DEBUG
    FFLAGS += -DDEBUG ${DEBUG_FLAGS}
	CFLAGS += -DDEBUG ${DEBUG_CFLAGS}
else
	FFLAGS += ${PROD_FLAGS}
	CFLAGS += ${PROD_FLAGS}
endif

ifdef PROFILE
	FFLAGS += -DPROFILE ${PROFILE_FLAGS}
	CFLAGS += -DPROFILE ${PROFILE_FLAGS}
endif

ifdef STATIC
	FFLAGS += $(STATIC_FLAGS)
endif

ifdef OPTINFO
	FFLAGS += $(OPTINFO_FLAGS)
endif

# NVIDIA compiler specific
include ${MAKEINC}/compiler_flags.cuda.mk
NVFLAGS = --gpu-architecture=${NV_COMPUTE_LEVEL} --gpu-code=${NV_CODE_LEVEL}
NVFLAGS += ${NV_COMPFLAGS}
ifdef DEBUG
	NVCOMPILE_FLAGS := ${NV_DEBUGFLAGS} -std=c++11
	NVFLAGS += ${CUDA_DEBUGFLAGS} -DDEBUG
else
	NVCOMPILE_FLAGS := ${NV_PRODFLAGS} -std=c++11
endif
NVFLAGS += --compiler-options="${NVCOMPILE_FLAGS}"

# HIP compiler specific for Nvdia target
include ${MAKEINC}/compiler_flags.hip_nvidia.mk
HIP_NVIDIA_FLAGS = ${NVFLAGS}

include ${MAKEINC}/compiler_flags.hip_amd.mk
HIP_AMD_FLAGS = --amdgpu-target=${HIP_AMDGPU_TARGET}
HIP_AMD_FLAGS += ${HIP_AMD_STDFLAGS}
ifdef DEBUG
	HIP_AMD_FLAGS += ${HIP_AMD_DEBUGFLAGS} -DDEBUG
else
	HIP_AMD_FLAGS += ${HIP_AMD_PRODFLAGS}
endif

XLF = ${COMPILER} ${FFLAGS} ${INCLUDE}
CC = ${CCOMPILER} ${CFLAGS} ${INCLUDE}
NVCC = ${NV_COMPILER} ${NVFLAGS}
HIP_AMD_CC = ${HIP_AMD_COMPILER} ${HIP_AMD_FLAGS}
HIP_NVIDIA_CC = ${HIP_NVIDIA_COMPILER} ${HIP_NVIDIA_FLAGS}

ifeq ($(HIP_PLATFORM),nvidia)
	HIPCC = ${HIP_NVIDIA_CC}
endif
ifeq ($(HIP_PLATFORM),amd)
	HIPCC = ${HIP_AMD_CC}
endif

