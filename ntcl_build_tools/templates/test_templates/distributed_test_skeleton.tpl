module ${name}_test_module
    use :: mpi_identity_module, only : mpi_identity
    use :: distributed_assert_module, only : distributed_assert
    use :: ${name}_module, only : ${name}

    implicit none
    private

    public :: ${name}_test

    type :: ${name}_test
        type(mpi_identity) :: mpi_id
    contains
        procedure :: run => run
        procedure :: cleanup => cleanup
        procedure :: clear => clear
    end type ${name}_test

    interface ${name}_test
        module procedure constructor
    end interface ${name}_test
contains
    function constructor(mpi_id) result(this)
        type(mpi_identity), intent(in) :: mpi_id
        type(${name}_test) :: this

        call this%clear()
        this%mpi_id = mpi_id
    end function constructor

    subroutine run(this, assertion)
        class(${name}_test), intent(in) :: this
        type(distributed_assert), intent(inout) :: assertion

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
