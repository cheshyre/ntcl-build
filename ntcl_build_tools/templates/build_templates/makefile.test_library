local_src := $(wildcard $(subdirectory)/*.f90) $(wildcard $(subdirectory)/*.F90)
$(eval $(call make-testlibrary, $(shell basename $(subdirectory))_test.a, $(local_src)))
$(eval $(subst #,$(newline),$(shell $(finddep) $(subdirectory) | tr '\n' '#')))
