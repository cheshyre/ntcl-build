! Auto-generated -- DO NOT MODIFY
program unittest
    use :: util_api, only : &
            assert, &
            selector, &
			string

${module_header}
    implicit none

    type(assert) :: assertion
    type(selector) :: aselector

${run_header}
    assertion = assert()
    aselector = selector([string("long")])

${run_statements}
    call assertion%write_summary()

    call aselector%cleanup()
    call assertion%cleanup()
end program unittest
