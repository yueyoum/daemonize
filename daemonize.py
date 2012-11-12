# -*- coding: utf-8 -*-

"""
Usage:

from daemonize import Daemonize

@Daemonize()
def my_func():
    pass
    
my_func()
"""

import os
import sys
import tempfile

class Daemonize(object):
    """Do Unix two fork to make your program daemonize"""
    def __init__(self, pidfile = None):
        self.pidfile = pidfile or os.path.join(tempfile.gettempdir(),
                                               '%s.pid' % __file__.rstrip('.py')
                                               )
        
        self.stdin = self.stdout = self.stderr = getattr(os, 'devnull', '/dev/null')
        
        
    def _daemon_fork(self):
        try:
            pid = os.fork()
            if pid > 0:
                # this parent, then exit
                sys.exit(0)
        except Exception, e:
            sys.stderr.write("fork 1 failed, %s\n" % e.strerror)
            sys.exit(1)
            
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
            sys.stderr.write("from 2 failed, %s\n" % e.strerror)
            sys.exit(2)
            
        # this is the second forded process
        # set fd
        sys.stdout.flush()
        sys.stderr.flush()
        
        stdin = file(self.stdin, 'r')
        stdout = file(self.stdout, 'a')
        stderr = file(self.stderr, 'a', 0)
        
        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())
        
        with open(self.pidfile, 'w') as f:
            f.write('%d\n' % os.getpid())
            
            
    def __call__(self, func):
        def wrap(*args, **kwargs):
            self._daemon_fork()
            res = func(*args, **kwargs)
            return res
        return wrap
            


if __name__ == '__main__':
    class T(object):
        def get_name(self):
            return 'NAME'
        
    t = T()
    
    @Daemonize()
    def run():
        with open('/tmp/t_name', 'w') as f:
            f.write('%s\n' % t.get_name())
            
    run()
