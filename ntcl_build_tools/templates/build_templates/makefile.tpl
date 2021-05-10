# Auto-generated -- do not modify!

SOURCE_DIR := $$(shell dirname $${MAKEFILE_LIST})
MAKEINC := $${NTCL_ROOT}/ntcl-build/makefile_fragments

include $${MAKEINC}/standard_preample.mk

${module_block}
${library_name}

external_include := ${external_include_directories}
external_libraries := ${libraries}
internal_include_dirs := ${internal_include_directories}
${optional_dependencies}

include $${MAKEINC}/standard_defs.mk
