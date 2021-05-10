# $(call make-library, library-name, source-file-list, dependencies)
define make-library
libraries += $1
libraries_for_linking := $1 ${libraries_for_linking}
sources += $2
headers += $(call extract-header-files,$2)
$1: $(call source-to-object,$2)
	$(AR) $(ARFLAGS) $(library_directory)/$$@ $$^
	$(foreach f,$(call extract-header-files,$2), cp $f $(include_directory)/.)
endef
define make-testlibrary
test_libraries += $1
testlibraries_for_linking := $1 ${testlibraries_for_linking}
test_sources   += $2
$1: $(call source-to-object,$2)
	$(AR) $(ARFLAGS) $(library_directory)/$$@ $$^
endef
# $(call source-to-object, source-file-list)
source-to-object =  $(subst .f90,.o,$(filter %.f90,$(patsubst ${SOURCE_DIR}/%,%, $1))) \
					$(subst .F90,.o,$(filter %.F90,$(patsubst ${SOURCE_DIR}/%,%, $1))) \
					$(subst .c,.o,$(filter %.c,$(patsubst ${SOURCE_DIR}/%,%, $1))) \
					$(subst .cu,.o,$(filter %.cu,$(patsubst ${SOURCE_DIR}/%,%, $1))) \
					$(subst .hip,.o,$(filter %.hip,$(patsubst ${SOURCE_DIR}/%,%, $1)))


extract-header-files =  $(filter %.h, $1)

# $(subdirectory)
subdirectory = 	$(patsubst %/makefile.mk,%, $(word  \
				$(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))


define newline


endef

define make-test
test_programs += $1
test_sources += $2
$1: $(call source-to-object,$2)
	${XLF} -o bin/$(shell basename $1) $$^ \
		$(patsubst %,$(library_directory)/%, ${testlibraries_for_linking}) \
		$(patsubst %,$(library_directory)/%, ${libraries_for_linking}) \
		$(internal_test_libraries) ${internal_libraries} ${external_libraries}
endef

define make-program
programs += $1
sources += $2
$1: $(call source-to-object,$2)
	${XLF} -o bin/$(shell basename $1) $$^ \
		$(patsubst %,$(library_directory)/%, ${libraries_for_linking}) \
		${internal_libraries} ${external_libraries}
endef
