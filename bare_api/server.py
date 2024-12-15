from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """
    An HTTP request handler with simple endpoints for testing
    basic API functionality (e.g. GET, POST)
    """

    storage = {"stored_data": []}

    def send_json_response(self, status_code, content):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write((json.dumps(content) + "\n").encode())

    def do_GET(self):

        if self.path == "/":
            response = {"message": "Hello, from barebones API :)"}
            self.send_json_response(status_code=200, content=response)

        elif self.path == "/about":
            if self.storage["stored_data"]:
                response = {
                    "message": "Stored data retrieved successfully",
                    "data": self.storage["stored_data"]
                }
            else:
                response = {
                    "message": "To store data on the server, hit the /save POST endpoint",
                    "data": []
                }
            self.send_json_response(status_code=200, content=response)

        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)

            if self.path == "/process":
                if "value" not in data:
                    raise ValueError("Missing 'value' in request body")

                response = {"received_value": data["value"]}
                self.send_json_response(status_code=200, content=response)

            elif self.path == "/save":
                if "value" not in data:
                    raise ValueError("Missing 'value' in request body")

                current_time = datetime.now()
                formatted_time = current_time.strftime('%H:%M:%S')
                self.storage["stored_data"].append({formatted_time: data["value"]})

                response = {"message": f"{data["value"]} saved successfully!"}
                self.send_json_response(status_code=200, content=response)

            else:
                self.send_error(404, "Endpoint not found")

        except json.JSONDecodeError:
            self.send_json_response(status_code=400, content={"error": "Invalid JSON in request body"})

        except ValueError as e:
            self.send_json_response(status_code=400, content={"error": str(e)})


def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print(f"Server running on port: {port}")

    httpd.serve_forever()


if __name__ == "__main__":
    PORT = 8000
    run(port=PORT)
