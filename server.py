import http.server
import socketserver
import os

# Set the port number
PORT = 8000

# Change to the directory containing the website files
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the server
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at http://localhost:{PORT}")
print("Press Ctrl+C to stop the server")

# Start the server
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server...")
    httpd.server_close() 