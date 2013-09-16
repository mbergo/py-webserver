# encoding: utf-8
"""
daemon.py

Created by mbergo on 2013-02-04.
Copyright (c) 2013 Globo.com. All rights reserved.
"""

import sys
import os
import time
import atexit
from signal import SIGTERM, SIGKILL


class Daemon(object):
    """
    Daemon class
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        Lets Daemon...
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork 1 fail: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork 2 fail: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        if self.stdin:
            si = open(self.stdin, 'r')
            os.dup2(si.fileno(), sys.stdin.fileno())
        if self.stdout:
            so = open(self.stdout, 'a+')
            os.dup2(so.fileno(), sys.stdout.fileno())
        if self.stderr:
            se = open(self.stderr, 'a+', 0)
            os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        self.pidfile_write()

    def delpid(self):
        os.remove(self.pidfile)

    def pidfile_read(self):
        """ Returns pidfile content (as int type) or None if pidfile
        doesn't exist. """
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        return pid

    def pidfile_write(self):
        """ Write current pid in pidfile """
        with open(self.pidfile, 'w+') as f:
            f.write("%s\n" % str(os.getpid()))

    def start(self):
        """
        Start the daemon
        """
        pid = self.pidfile_read()

        if pid:
            message = "pidfile %s exist. Daemon is running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop daemon
        """
        pid = self.pidfile_read()

        if not pid:
            message = "pidfile %s don't exist. Did daemon is running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        try:
            os.kill(pid, SIGTERM)
            time.sleep(0.1)
            os.kill(pid, SIGKILL)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        Overwrite me
        """
        raise RuntimeError('Overwrite me')
