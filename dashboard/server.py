"""Mailaka Dashboard Server

A lightweight web dashboard for managing Mailaka inboxes and viewing messages.
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Dashboard files directory
DASHBOARD_DIR = Path(__file__).parent / "dashboard"
STORAGE_FILE = Path.home() / ".local" / "share" / "mailaka" / "storage.json"


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard."""
    
    def log_message(self, format, *args):
        """Suppress request logging."""
        pass
    
    def do_GET(self):
        """Handle GET requests."""
        path = self.path
        
        if path == '/':
            self.serve_file('index.html', 'text/html')
        elif path == '/styles.css':
            self.serve_file('styles.css', 'text/css')
        elif path == '/dashboard.js':
            self.serve_file('dashboard.js', 'application/javascript')
        elif path == '/api/stats':
            self.serve_stats()
        elif path == '/api/inboxes':
            self.serve_inboxes()
        else:
            self.send_response(404)
            self.end_headers()
    
    def serve_file(self, filename, content_type):
        """Serve a static file."""
        filepath = DASHBOARD_DIR / filename
        if filepath.exists():
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
    
    def serve_stats(self):
        """Serve dashboard statistics from Mailaka storage."""
        try:
            if STORAGE_FILE.exists():
                with open(STORAGE_FILE, 'r') as f:
                    data = json.load(f)
                    inboxes = data.get('inboxes', [])
            else:
                inboxes = []
            
            # Calculate statistics
            total_inboxes = len(inboxes)
            total_messages = sum(len(ib.get('messages', [])) for ib in inboxes)
            active_inboxes = sum(1 for ib in inboxes if not ib.get('expired', False))
            
            stats = {
                'active_inboxes': active_inboxes,
                'total_inboxes': total_inboxes,
                'total_messages': total_messages,
                'providers': ['mail.tm', 'mail.gw', 'guerrillamail', 'tempmail.io']
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
    
    def serve_inboxes(self):
        """Serve inbox data."""
        try:
            if STORAGE_FILE.exists():
                with open(STORAGE_FILE, 'r') as f:
                    data = json.load(f)
                    inboxes = data.get('inboxes', [])
            else:
                inboxes = []
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(inboxes).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()


def start_dashboard(host='localhost', port=8080):
    """Start the dashboard server."""
    server = HTTPServer((host, port), DashboardHandler)
    print(f"""
  ╔═══════════════════════════════════════════════════════════════╗
  ║                                                               ║
  ║  Mailaka Dashboard                                            ║
  ║                                                               ║
  ║  URL: http://{host}:{port}                                    ║
  ║                                                               ║
  ╚═══════════════════════════════════════════════════════════════╝
    """)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Arret du serveur...")
        server.shutdown()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    
    start_dashboard(port=port)