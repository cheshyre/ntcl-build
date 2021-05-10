! Auto-generated -- DO NOT MODIFY
program unittest
    use :: util_api, only : selector
    use :: mpi_initializer_module, only : mpi_initializer
    use :: mpi_identity_module, only : mpi_identity
    use :: distributed_assert_module, only : distributed_assert

${module_header}
    implicit none

    type(mpi_initializer) :: mpi
    type(mpi_identity) :: mpi_id
    type(distributed_assert) :: assertion
    type(selector) :: aselector

${run_header}
	mpi = mpi_initializer()
    mpi_id = mpi%get_mpi_identity_for_world()
    assertion = distributed_assert(mpi_id)
    aselector = selector()

${run_statements}
    call assertion%write_summary()

    call aselector%cleanup()
    call assertion%cleanup()
    call mpi%cleanup()
end program unittest
