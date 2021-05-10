    a${name}_package_test = ${name}_package_test(aselector)
    call a${name}_package_test%run(assertion)
    call a${name}_package_test%cleanup()
