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

include ${MAKEINC}/applications.mk
ifdef force_applications
	include ${MAKEINC}/applications.${force_applications}.mk
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

ifdef USE_HIP
ifdef USE_HIP_NVCC
    include ${MAKEINC}/compiler_flags.hip_nvcc.mk
endif
ifdef USE_HIP_HCC
    include ${MAKEINC}/compiler_flags.hip_hcc.mk
endif
    LIBS += ${HIP_LIBS}

	HIPFLAGS += ${HIP_COMPFLAGS}
    ifdef DEBUG
        HIPCOMPILE_FLAGS := ${HIP_DEBUGFLAGS}
        HIPFLAGS += ${HIP_DEBUGFLAGS} -DDEBUG
    else
        HIPCOMPILE_FLAGS := ${HIP_PRODFLAGS}
    endif
	HIPFLAGS += ${HIPCOMPILE_FLAGS}
endif

XLF = ${COMPILER} ${FFLAGS} ${INCLUDE}
CC = ${CCOMPILER} ${CFLAGS} ${INCLUDE}
NVCC = ${NV_COMPILER} ${NVFLAGS}
HIPCC = ${HIP_COMPILER} ${HIPFLAGS}

