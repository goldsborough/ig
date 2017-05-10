'''The server that serves the web visualization.'''

import json
import logging
import os
import shutil
import socket
import webbrowser

from ig import paths

try:
    import socketserver
    import http.server as http
except ImportError:
    import SocketServer as socketserver
    import SimpleHTTPServer as http


log = logging.getLogger(__name__)


class Server(object):
    def __init__(self, directory):
        '''
        Constructor.

        Args:
            directory: The directory to serve from.
        '''
        self.delete_directory = directory is None
        self.directory = paths.create_directory(directory)

    def run(self, open_immediately, port):
        '''
        Serves the `www` directory.

        Args:
            open_immediately: Whether to open the web browser immediately
            port: The port at which to serve the graph
        '''
        os.chdir(self.directory)
        handler = http.SimpleHTTPRequestHandler
        handler.extensions_map.update({
            '.webapp': 'application/x-web-app-manifest+json',
        })

        server = socketserver.TCPServer(('', port), handler)
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        address = 'http://localhost:{0}/graph.html'.format(port)
        log.info('Serving at %s', address)

        if open_immediately:
            log.debug('Opening webbrowser')
            webbrowser.open(address)

        server.serve_forever()

    def write(self, payload):
        '''
        Writes the given JSON representation to the served location.

        Args:
            payload: The playlod to JSONify and store.
        '''
        path = os.path.join(self.directory, 'graph.json')
        with open(path, 'w') as graph_file:
            graph_file.write(json.dumps(payload, indent=4))

        log.debug('Wrote graph file to {0}'.format(path))

    def cleanup(self):
        if self.delete_directory:
            assert self.directory is not None
            shutil.rmtree(self.directory, ignore_errors=True)
            log.debug('Deleted directory %s', self.directory)

    def __enter__(self):
        return self

    def __exit__(self, error_type, error_value, traceback):
        self.cleanup()
        if error_type == KeyboardInterrupt:
            return True  # Supresses the exception
        # Any other exception is propagated up
