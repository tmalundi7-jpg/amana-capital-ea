import threading
import http.server
import socketserver
import time
from playwright.sync_api import sync_playwright

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

class ThreadedHTTPServer(object):
    def __init__(self, host, port, request_handler_class):
        self.server = socketserver.TCPServer((host, port), request_handler_class)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
    def start(self): self.server_thread.start()
    def stop(self):
        self.server.shutdown()
        self.server.server_close()

server = ThreadedHTTPServer("localhost", PORT, Handler)
server.start()
time.sleep(1)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # device_scale_factor=3 generates a retina-quality (3x resolution) image
        context = browser.new_context(
            viewport={"width": 1200, "height": 900},
            device_scale_factor=3
        )
        page = context.new_page()
        page.goto(f"http://localhost:{PORT}/market-intelligence.html")
        
        # Wait for any child div inside the container to ensure JS rendered it
        page.wait_for_selector("#dseHeatmapContainer > div", timeout=5000)
        time.sleep(2) # let animations finish
        
        heatmap = page.locator(".mi-heatmap-section")
        
        output_path = r"C:\Users\tmalu\Documents\DSE_Heatmap_14_Sept_HighRes.png"
        heatmap.screenshot(path=output_path, type="png")
        print(f"High resolution heatmap saved to {output_path}")
        browser.close()
finally:
    server.stop()
