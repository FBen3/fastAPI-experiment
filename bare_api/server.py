from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {"message": "Hello, from barebones API :)"}

            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        pass


def run():
    pass


if __name__ == "__main__":
    run()
