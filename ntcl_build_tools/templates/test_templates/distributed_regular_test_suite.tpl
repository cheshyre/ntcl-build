        if ( &
                this%test_selector%is_enabled("${name}") ) then
            a${name}_test = ${name}_test(this%mpi_id)
            call a${name}_test%run(assertion)
            call a${name}_test%cleanup()
        end if
