module ${name}_test_module
    use :: util_api, only : assert
    use :: ${name}_module, only : ${name}

    implicit none
    private

    public :: ${name}_test

    type :: ${name}_test
    contains
        procedure :: run => run
        procedure :: cleanup => cleanup
        procedure :: clear => clear
    end type ${name}_test

    interface ${name}_test
        module procedure constructor
    end interface ${name}_test
contains
    function constructor() result(this)
        type(${name}_test) :: this

        call this%clear()
    end function constructor

    subroutine run(this, assertion)
        class(${name}_test), intent(in) :: this
        type(assert), intent(inout) :: assertion

        type(${name}) :: a${name}

        call assertion%equal("${name}::Test complete", .false.)

        a${name} = ${name}()
    end subroutine run

    subroutine cleanup(this)
        class(${name}_test), intent(inout) :: this

        call this%clear()
    end subroutine cleanup

    subroutine clear(this)
        class(${name}_test), intent(inout) :: this
    end subroutine clear
end module ${name}_test_module
