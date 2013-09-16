# encoding: utf-8
import os
import argparse
import logging.config
from .server import Server
from .daemon import Daemon
from . import LOG, ACTION_START, ACTION_STOP, DEFAULT_ACTION, DEFAULT_BIND, \
    DEFAULT_PORT, DEFAULT_PIDFILE


class WebDaemon(Daemon):

    def __init__(self, pidfile, ip, port, datastore):
        super(WebDaemon, self).__init__(pidfile, stdout=None, stderr=None)
        # pidfile, stdin='/dev/null', stdout='/dev/null',stderr='/dev/null'):
        self.datastore = datastore
        self.ip = ip
        self.port = port

    def run(self):
        self.http_server = Server(self.ip, self.port, self.datastore)
        while True:
            try:
                self.http_server.handle_request()
            except KeyboardInterrupt:
                LOG.warning('Ctrl+C pressed... aborting!')
                break
            except:
                LOG.error('Error processing request', exc_info=True)


def run_cmd(argv=None):
    parser = argparse.ArgumentParser(description='Run webserver to serve'
                                     'instance meta-data')
    parser.add_argument('action',
                        choices=[ACTION_START, ACTION_STOP],
                        default=ACTION_START,
                        nargs='?',
                        help='Action. Default %s' % DEFAULT_ACTION)
    parser.add_argument('--daemon',
                        action='store_true',
                        help='daemonize server')
    parser.add_argument('--dummy',
                        action='store_true',
                        help='Dummy mode. Use only for tests')
    parser.add_argument('--pidfile',
                        default=DEFAULT_PIDFILE,
                        help='pid file. Default %s' % DEFAULT_PIDFILE)
    parser.add_argument('--bind',
                        default=DEFAULT_BIND,
                        help='bind address. Default %s' % DEFAULT_BIND)
    parser.add_argument('--port',
                        default=DEFAULT_PORT,
                        type=int,
                        help='port number. Default %s' % DEFAULT_PORT)
    args = parser.parse_args(argv)

    if args.dummy:
        from .datastore.dummy import create_dummy_datastore_with_data
        datastore = create_dummy_datastore_with_data()
    else:
        from .datastore.xenstore import XenStoreDataStore
        datastore = XenStoreDataStore()
    web_daemon = WebDaemon(args.pidfile, args.bind, args.port, datastore)

    # configure logging
    log_file = os.path.abspath('%s/../logging.conf' % __file__)
    logging.config.fileConfig(log_file)

    if args.action == 'start':
        if args.daemon:
            web_daemon.start()
        else:
            web_daemon.run()

    elif args.action == 'stop':
        web_daemon.stop()

if __name__ == '__main__':
    run_cmd()
