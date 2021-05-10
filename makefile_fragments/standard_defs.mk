objects=$(call source-to-object,$(sources))
test_objects=$(call source-to-object,$(test_sources))

FFLAGS     += $(addprefix -I ,$(include_directory))
FFLAGS     += $(addprefix -I ,$(internal_include_dirs))
FFLAGS     += $(addprefix -I ,$(internal_test_include))
FFLAGS     += $(external_include)

CFLAGS     += $(addprefix -I ,$(include_directory))
CFLAGS     += $(addprefix -I ,$(internal_include_dirs))
CFLAGS     += $(addprefix -I ,$(internal_test_include))
CFLAGS     += $(external_include)

NVFLAGS     += $(addprefix -I ,$(include_directory))
NVFLAGS     += $(addprefix -I ,$(internal_include_dirs))

HIPFLAGS     += $(addprefix -I ,$(include_directory))
HIPFLAGS     += $(addprefix -I ,$(internal_include_dirs))

vpath %.f90 $(SOURCE_DIR)
vpath %.F90 $(SOURCE_DIR)
vpath %.cu $(SOURCE_DIR)
vpath %.c $(SOURCE_DIR)
vpath %.hip $(SOURCE_DIR)

include ${MAKEINC}/standard_targets.mk

create-output-directories :=											\
		$(shell for d in src include bin lib;							\
				do														\
					test -d $$d || mkdir $$d;							\
				done;													\
				for d in modules test;									\
				do														\
					test -d src/$$d || mkdir src/$$d;					\
				done;													\
				for f in $(modules);									\
				do														\
					test -d src/modules/$$f || mkdir src/modules/$$f;   \
				done;													\
				for f in $(test_modules);								\
				do														\
					test -d src/test/$$f || mkdir src/test/$$f;			\
				done)
