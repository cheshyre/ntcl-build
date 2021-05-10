! Auto-generated -- DO NOT MODIFY
module ${name}_package_test_module
    use :: util_api, only : &
            selector, &
            assert
${module_header}
    implicit none
    private

    public :: ${name}_package_test

    type :: ${name}_package_test
        type(selector) :: test_selector
    contains
        procedure :: run => run
        procedure :: cleanup => cleanup
        procedure :: clear => clear
    end type ${name}_package_test

    interface ${name}_package_test
        module procedure constructor
    end interface ${name}_package_test

contains
    function constructor(aselector) result(this)
        type(selector), intent(in) :: aselector
        type(${name}_package_test) :: this

        call this%clear()

        this%test_selector = aselector
    end function constructor

    subroutine run(this, assertion)
        class(${name}_package_test), intent(in) :: this
        type(assert), intent(inout) :: assertion
${run_header}
        call assertion%equal("${name}::Package test complete", .true.)
${test_suite}
    end subroutine run

    subroutine cleanup(this)
        class(${name}_package_test), intent(inout) :: this

        call this%clear()
    end subroutine cleanup

    subroutine clear(this)
        class(${name}_package_test), intent(inout) :: this
    end subroutine clear
end module ${name}_package_test_module
