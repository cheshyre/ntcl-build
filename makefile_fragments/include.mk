MPI_LIBDIR = ${MPI_DIR}/lib
MPI_INCLUDEDIR =${MPI_DIR}/include
HDF5_LIBDIR = ${HDF5_DIR}/lib
HDF5_INCLUDEDIR =${HDF5_DIR}/include

ifdef force_include
	include ${MAKEINC}/include.${force_include}.mk
else
ifneq (${system},default)
	include ${MAKEINC}/include.${system}.mk
endif
endif

ifdef use_cuda
    include ${MAKEINC}/include.cuda.mk
endif

ifdef use_hip
	ifeq ($(HIP_PLATFORM),nvidia)
		include ${MAKEINC}/include.hip_nvidia.mk
	endif
	ifeq ($(HIP_PLATFORM),amd)
		include ${MAKEINC}/include.hip_amd.mk
	endif
endif

ifdef USE_CUTT
    include ${MAKEINC}/include.cutt.mk
endif
ifdef USE_CUTENSOR
    include ${MAKEINC}/include.cutensor.mk
endif
ifdef USE_MAGMA
    include ${MAKEINC}/include.magma.mk
endif

