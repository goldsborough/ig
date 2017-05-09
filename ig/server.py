import os
import webbrowser

from ig import main

try:
    import socketserver
    import http.server as http
except ImportError:
    import SocketServer as socketserver
    import SimpleHTTPServer as http


def serve(open_immediately, port):
    os.chdir(main.WWW_PATH)
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
