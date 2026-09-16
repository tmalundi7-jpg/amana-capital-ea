import threading
import http.server
import socketserver
import time
from playwright.sync_api import sync_playwright

# Start a simple HTTP server in a thread
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

class ThreadedHTTPServer(object):
    def __init__(self, host, port, request_handler_class):
        self.server = socketserver.TCPServer((host, port), request_handler_class)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

server = ThreadedHTTPServer("localhost", PORT, Handler)
server.start()

# Give it a sec to start
time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1200, "height": 800})
    page.goto(f"http://localhost:{PORT}/market-intelligence.html")
    
    # Wait for the heatmap to render (the JS draws it)
    page.wait_for_selector(".heatmap-box", timeout=5000)
    time.sleep(1) # wait for animations if any
    
    heatmap = page.locator(".mi-heatmap-section")
    output_path = r"C:\Users\tmalu\Documents\DSE_Heatmap_14_Sept.png"
    heatmap.screenshot(path=output_path)
    print(f"Heatmap saved to {output_path}")
    
    browser.close()

server.stop()
