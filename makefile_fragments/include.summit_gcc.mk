INCMPI=-I${MPI_INCLUDEDIR} -I${MPI_LIBDIR}
LIBMPI=-pthread -L${MPI_LIBDIR} -lmpiprofilesupport -lmpi_ibm_usempi -lmpi_ibm_mpifh -lmpi_ibm
LIBBLAS=-L${OLCF_ESSL_ROOT}/lib64 -lesslsmp
#LIBBLAS=-L${OLCF_ESSL_ROOT}/lib64 -lesslsmpcuda
#LIBBLAS=-L${CUDA_ROOT}/lib64 -lnvblas
INCHDF5=-I${HDF5_INCLUDEDIR}
LIBHDF5 = -L${HDF5_LIBDIR} ${HDF5_LIBDIR}/libhdf5hl_fortran.a ${HDF5_LIBDIR}/libhdf5_hl.a ${HDF5_LIBDIR}/libhdf5_fortran.a ${HDF5_LIBDIR}/libhdf5.a -ldl -lm -lz -Wl,-rpath -Wl,${HDF5_LIBDIR}
NV_COMPUTE_LEVEL=compute_70
NV_CODE_LEVEL=sm_70
