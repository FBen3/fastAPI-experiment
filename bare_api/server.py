from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):

    storage = {"stored_data": []}


    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {"message": "Hello, from barebones API :)"}

            self.wfile.write((json.dumps(response) + "\n").encode())

        elif self.path == "/about":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            if self.storage["stored_data"]:
                response = {
                    "message": "Stored data retreived successfully",
                    "data": self.storage["stored_data"]
                }
            else:
                response = {
                    "message": "To store data on the server, hit the /save POST endpoint",
                    "data": []
                }

            self.wfile.write((json.dumps(response) + "\n").encode())

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

                self.wfile.write((json.dumps(response) + "\n").encode())
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, str(e))

        elif self.path == "/save":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)

                if "value" not in data:
                    raise ValueError("Missing 'value' in request body")

                current_time = datetime.now()
                formatted_time = current_time.strftime('%H:%M:%S')
                self.storage["stored_data"].append({formatted_time: data["value"]})

                response = {"message": f"{data["value"]} saved successfully!"}

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write((json.dumps(response) + "\n").encode())
            except (ValueError) as e:
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
