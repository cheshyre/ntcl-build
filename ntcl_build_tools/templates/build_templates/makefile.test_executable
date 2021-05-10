local_src := $(wildcard $(subdirectory)/*.f90) $(wildcard $(subdirectory)/*.F90)
$(eval $(subst #,$(newline),$(shell $(finddep) $(subdirectory) | tr '\n' '#')))
$(eval $(call make-test, $(subdirectory)/$(shell basename $(subdirectory)).x, $(local_src)))
