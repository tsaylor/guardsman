import BaseHTTPServer


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        return self.send_response(200, '')

httpd = BaseHTTPServer.HTTPServer(
    ('', 3000),
    RequestHandler
)
httpd.serve_forever()
