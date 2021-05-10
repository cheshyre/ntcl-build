        if ( &
                this%test_selector%is_enabled("${name}") .and. &
                this%test_selector%is_enabled("long") ) then
            a${name}_test = ${name}_test()
            call a${name}_test%run(assertion)
            call a${name}_test%cleanup()
        end if
