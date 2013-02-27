# A Simple Class to make your program daemonize in Unix-like system


Usage:

    from daemonized import Daemonize

    @Daemonize()
    def my_func():
        # this func will be daemonize
        pass

    my_func()

    # or, this
    d = Daemonize()
    d.stdout = '/tmp/d_out'  # MUST BE ABSOLUTE PATH
    d.stderr = '/tmp/d_err'

    def my_func():
        pass

    d.make_daemon()
    my_func()

