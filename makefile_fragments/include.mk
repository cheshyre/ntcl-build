MPI_LIBDIR = ${MPI_DIR}/lib
MPI_INCLUDEDIR =${MPI_DIR}/include
HDF5_LIBDIR = ${HDF5_DIR}/lib
HDF5_INCLUDEDIR =${HDF5_DIR}/include

ifdef force_include
	include ${MAKEINC}/include.${force_include}.mk
else
	include ${MAKEINC}/include.${system}.mk
endif

ifdef use_cuda
    include ${MAKEINC}/include.cuda.mk
endif
ifdef USE_HIP_NVCC
    include ${MAKEINC}/include.hip_nvcc.mk
endif
ifdef USE_HIP_HCC
    include ${MAKEINC}/include.hip_hcc.mk
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

