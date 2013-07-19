execgate
========

A safer python 3 exec.

Usage:

    from execgate import gated_exec, gated_eval, GateSecurityError

    foo = gated_eval('1 + 1')
    try:
        gated_exec("""[
            c for c in 
                ().__class__.__bases__[0].__subclasses__() 
                    if c.__name__ == "Quitter"
                    ][0](0)()""")
    except GateSecurityError:
        print("You are a baaaad monkey.")

