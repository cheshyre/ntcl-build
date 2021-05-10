SCRIPTDIR=${NTCL_ROOT}/ntcl-build/bin

include ${MAKEINC}/compiler.mk
include ${MAKEINC}/make_functions.mk
include ${MAKEINC}/include.mk

modules 		:=
headers			:=
programs     	:=
sources      	:=
libraries    	:=
libraries_for_linking    	:=
include_dirs 	:=

test_modules 	:=
test_programs 	:=
test_sources    :=
test_libraries 	:=
testlibraries_for_linking 	:=

include_directory := include
library_directory := lib
