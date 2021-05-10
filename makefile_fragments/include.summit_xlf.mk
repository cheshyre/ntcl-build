INCMPI=-I${MPI_INCLUDEDIR} -qthreaded -I${MPI_LIBDIR}
LIBMPI=-L${MPI_LIBDIR} -lmpiprofilesupport -lmpi_ibm_usempi -lmpi_ibm_mpifh -lmpi_ibm
LIBBLAS=-L${OLCF_ESSL_ROOT}/lib64 -lesslsmp
INCHDF5=-I${HDF5_INCLUDEDIR}
LIBHDF5 = -L${HDF5_LIBDIR} ${HDF5_LIBDIR}/libhdf5hl_fortran.a ${HDF5_LIBDIR}/libhdf5_hl.a ${HDF5_LIBDIR}/libhdf5_fortran.a ${HDF5_LIBDIR}/libhdf5.a -ldl -lm -lz -Wl,-rpath -Wl,${HDF5_LIBDIR}
