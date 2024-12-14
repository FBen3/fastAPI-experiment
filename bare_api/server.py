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

        elif self.path == "/about":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {"message": "To store data on the server, hit the /save POST endpoint"}

            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        if self.path == "/process":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)

                if "value" not in data:
                    raise ValueError("Missing 'value' in request body")

                response = {"received_value": data["value"]}

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(response).encode())
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, str(e))

        else:
            self.send_error(404, "Endpoint not found")



def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print(f"Server running on port: {port}")

    httpd.serve_forever()


if __name__ == "__main__":
    run()
