ifndef AR
AR := gcc-ar
endif

ifndef ARLIBFLAGS
ARLIBFLAGS := -rcT
endif

ifndef MV
MV  := mv -f
endif

ifndef RM
RM  := rm -f
endif

ifndef SED
SED := sed
endif

finddep := python3 ${SCRIPTDIR}/find_dependencies_make.py

