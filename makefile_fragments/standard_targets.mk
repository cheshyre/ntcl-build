all:

include $(patsubst %,$(SOURCE_DIR)/src/modules/%/makefile.mk,$(modules))
include $(patsubst %,$(SOURCE_DIR)/src/test/%/makefile.mk,$(test_modules))

.PHONY: all
all: libraries

.PHONY: libraries
libraries: $(libraries)
ifdef library_name
	${RM} ${library_directory}/${library_name}
	$(AR) ${ARLIBFLAGS} $(library_directory)/$(library_name) $(patsubst %,lib/%, $(libraries))
ifdef library_name_full
	echo "create ${library_name_full}" > $(library_directory)/$(library_name_full).mri
	for f in $(patsubst %,lib/%, $(libraries)); do \
		echo "addlib $$f" >> $(library_directory)/$(library_name_full).mri; \
	done
	echo "save" >> $(library_directory)/$(library_name_full).mri
	echo "end" >> $(library_directory)/$(library_name_full).mri
	$(AR) -M <$(library_directory)/$(library_name_full).mri
	${MV} $(library_name_full)  $(library_directory)/$(library_name_full)
endif
endif
	for f in $(headers); do cp $$f $(include_directory); done

.PHONY: test
test: libraries ${test_libraries} ${test_programs}

.PHONY: apps
apps: libraries ${programs}

.PHONY: clean
clean:
	$(RM) $(objects) ${test_objects} $(programs) $(patsubst %,lib/%, $(libraries)) \
	$(patsubst %,lib/%, $(test_libraries)) \
	${test_programs} bin/*.x include/*.mod
	for d in ${include_dirs}; do \
		${RM} $$d/*.mod; \
	done
ifdef library_name
	${RM} ${library_directory}/${library_name}
endif

%.o: %.f90
	${XLF} $(modcmd)${include_directory} -c $< -o $@
%.o: %.F90
	${XLF} $(modcmd)${include_directory} -c $< -o $@
%.o: %.cu
	${NVCC} -c $< -o $@
%.o: %.c
	${CC} ${CFLAGS} -c $< -o $@
%.o: %.hip
	${HIPCC} -c $< -o $@
