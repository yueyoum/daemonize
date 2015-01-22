# -*- coding: utf-8 -*-

"""
Usage:

from daemonized import Daemonize

@Daemonize(**kwargs)
def my_func():
    pass

my_func()

 kwargs are:
    pidfile=PATH
    stdin=PATH
    stdout=PATH
    stderr=PATH

PATH MUST BE ABSOLUTE PATH
"""

import os
import sys


__version__ = VERSION = '0.3.0'
__all__ = ['Daemonize']


class Daemonize(object):
    """Do Unix two fork to make your program daemonize"""
    def __init__(self, pidfile=None, stdin=None, stdout=None, stderr=None):
        if pidfile:
            # test pidfile is writeable
            open(pidfile, 'w').close()

        self.pidfile = pidfile

        dev_null = getattr(os, 'devnull', '/dev/null')
        self.stdin = stdin or dev_null
        self.stdout = stdout or dev_null
        self.stderr = stderr or dev_null

    def make_daemon(self):
        try:
            pid = os.fork()
            if pid > 0:
                # this parent, then exit
                sys.exit(0)
        except Exception, e:
            sys.stderr.write("fork 1 failed, %s\n" % e)
            raise

        # this is the first forked child process
        # separate from parent's environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except Exception, e:
            sys.stderr.write("fork 2 failed, %s\n" % e)
            raise

        # this is the second forded process
        # set fd
        sys.stdout.flush()
        sys.stderr.flush()

        sys.stdout.write("Start...\n")

        stdin = file(self.stdin, 'r')
        stdout = file(self.stdout, 'a')
        stderr = file(self.stderr, 'a', 0)

        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

        if self.pidfile:
            with open(self.pidfile, 'w') as f:
                f.write('%d\n' % os.getpid())


    def __call__(self, func=None):
        if not func:
            self.make_daemon()
            return

        def wrap(*args, **kwargs):
            self.make_daemon()
            return func(*args, **kwargs)
        return wrap


