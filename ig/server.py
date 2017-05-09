import os
import webbrowser

from ig import paths

try:
    import socketserver
    import http.server as http
except ImportError:
    import SocketServer as socketserver
    import SimpleHTTPServer as http


def serve(open_immediately, port):
    '''
    Serves the `www` directory.

    Args:
        open_immediately: Whether to open the webbrowser with the graph file
        port: The port at which to serve the graph
    '''
    os.chdir(paths.WWW)
    handler = http.SimpleHTTPRequestHandler
    handler.extensions_map.update({
        '.webapp': 'application/x-web-app-manifest+json',
    })

    server = socketserver.TCPServer(('', port), handler)

    address = 'http://localhost:{0}/graph.html'.format(port)
    print('Serving at {0}'.format(address))

    if open_immediately:
        webbrowser.open(address)

    server.serve_forever()
