import http.server
import socketserver
import os

PORT = 5000
DIRECTORY = "."

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        path = self.path.split('?')[0]
        
        if path.endswith('/'):
            path = path + 'index.html'
        elif not os.path.splitext(path)[1]:
            test_path = '.' + path + '/index.html'
            if os.path.exists(test_path):
                path = path + '/index.html'
        
        self.path = path
        return super().do_GET()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ReusableTCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}")
        httpd.serve_forever()
