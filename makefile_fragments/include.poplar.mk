INCMPI=-I${MPI_INCLUDEDIR} -I${MPI_LIBDIR}
LIBMPI=-Wl,-rpath -Wl,${MPI_LIBDIR} -Wl,--enable-new-dtags -L${MPI_LIBDIR} -lmpi -lfmpich -lmpifort
LIBBLAS=-lblas
INCHDF5=-I${HDF5_INCLUDEDIR}
LIBHDF5 = -L${HDF5_LIBDIR} ${HDF5_LIBDIR}/libhdf5hl_fortran.a ${HDF5_LIBDIR}/libhdf5_hl.a ${HDF5_LIBDIR}/libhdf5_fortran.a ${HDF5_LIBDIR}/libhdf5.a -ldl -lm -lz -Wl,-rpath -Wl,${HDF5_LIBDIR}
NV_COMPUTE_LEVEL=compute_70
NV_CODE_LEVEL=${NV_COMPUTE_LEVEL}
HIP_AMDGPU_TARGET=gfx906,gfx908
