import os
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from google import genai

client = genai.Client()

class ZubEduHandler(SimpleHTTPRequestHandler):

    def send_json(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/ask":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))

            question = data.get("question", "")
            student_class = data.get("studentClass", "10")

            prompt = f"""
You are ZubEdu AI, a helpful CBSE study assistant.
Student class: {student_class}
Answer the student's question clearly and simply.

Question:
{question}
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            self.send_json({"answer": response.text})
            return

        self.send_json({"error": "Invalid request"})

PORT = int(os.environ.get("PORT", 8000))
server = ThreadingHTTPServer(("0.0.0.0", PORT), ZubEduHandler)

print("================================")
print("ZubEdu AI Server Started")
print("Open: http://127.0.0.1:8000")
print("================================")

server.serve_forever()
