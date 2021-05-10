INCMPI=-I${MPI_INCLUDEDIR} -I${MPI_LIBDIR}
LIBMPI=-Wl,-flat_namespace -Wl,-commons,use_dylibs -L${LIBEVENT_DIR}/lib -L${MPI_DIR}/lib -lmpi_usempif08 -lmpi_usempi_ignore_tkr -lmpi_mpifh -lmpi
LIBBLAS=-lblas
INCHDF5=-I${HDF5_INCLUDEDIR}
LIBHDF5 = -L${HDF5_LIBDIR} ${HDF5_LIBDIR}/libhdf5hl_fortran.a ${HDF5_LIBDIR}/libhdf5_hl.a ${HDF5_LIBDIR}/libhdf5_fortran.a ${HDF5_LIBDIR}/libhdf5.a -L${SZIP_DIR}/lib -lsz -ldl -lm -lz -Wl,-rpath -Wl,${HDF5_LIBDIR}
