INCMPI=-I${MPI_INCLUDEDIR} -I${MPI_LIBDIR}
LIBMPI=-Wl,-rpath -Wl,${MPI_LIBDIR} -Wl,--enable-new-dtags -L${MPI_LIBDIR} -lmpi_usempif08 -lmpi_usempi_ignore_tkr -lmpi_mpifh -lmpi
LIBBLAS=-lopenblas
INCHDF5=-I${HDF5_INCLUDEDIR}
LIBHDF5 = -L${HDF5_LIBDIR} ${HDF5_LIBDIR}/libhdf5hl_fortran.a ${HDF5_LIBDIR}/libhdf5_hl.a ${HDF5_LIBDIR}/libhdf5_fortran.a ${HDF5_LIBDIR}/libhdf5.a -ldl -lm -lz -Wl,-rpath -Wl,${HDF5_LIBDIR}
