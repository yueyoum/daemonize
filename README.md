# A Simple Class to make your program daemonize in Unix-like system


Usage:

    from daemonized import Daemonize

    @Daemonize(**kwargs)
    def my_func():
        pass

    my_func()

    #kwargs are:
    #    pidfile=PATH
    #    stdin=PATH
    #    stdout=PATH
    #    stderr=PATH
    #
    #PATH MUST BE ABSOLUTE PATH

