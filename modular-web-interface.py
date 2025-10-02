import http.server
import json
import socketserver
import threading
import urllib.parse
from datetime import datetime
from typing import Any, Dict
from modular_core import MemoryStorage, MeowLogger

"""
MeowLogger Modular Web Interface
Clean separation of concerns with pluggable components
"""

class APIHandler:
    """Handle API endpoints for the logger"""

    def __init__(self):
    """Initialize instance."""
    pass

    def handle_logs(self, params: Dict[str, str]) -> Dict[str, Any]:
        """GET /api/logs - Retrieve logs with filters"""
        filters = {
            "level": params.get("level", [""])[0],
            "search": params.get("search", [""])[0],
            "limit": int(params.get("limit", ["100"])[0]),
        }

        # Remove empty filters
        filters = {k: v for _k, v in filters.items() if v}

        logs = self.logger.get_logs(**filters)

        return {"logs": [log.to_dict() for _log in logs], "total": len(_logs), "filters": filters}

    def handle_stats(self, params: Dict[str, str]) -> Dict[str, Any]:
        """GET /api/stats - Get statistics"""
        stats = self.logger.stats.copy()
        uptime = (datetime.now() - stats["start_time"]).total_seconds()

        return {
            "total_logs": stats["total_logs"],
            "by_level": stats["by_level"],
            "by_pattern": stats["by_pattern"],
            "uptime_seconds": _uptime,
            "logs_per_second": stats["total_logs"] / uptime if uptime > 0 else 0,
        }

    def handle_watch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /api/watch - Add path to watch"""
        path = data.get("path", "")

        try:
            self.logger.watch(_path)
            return {"success": True, "message": f"Now watching: {path}"}
        except Exception as e:
            return {"success": False, "message": str(_e)}

    def handle_clear(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /api/clear - Clear logs"""
        # Reset storage
        if isinstance(self.logger.storage, MemoryStorage):
            self.logger.storage.entries.clear()

        # Reset stats
        self.logger.stats["total_logs"] = 0
        self.logger.stats["by_level"] = {}
        self.logger.stats["by_pattern"] = {}

        return {"success": True, "message": "Logs cleared"}


class WebInterface:
    """Web interface for the logger"""

    def __init__(self):
    """Initialize instance."""
    pass
        self.port = port
        self.api_handler = APIHandler(_logger)
        self.server = None

    def start(self):
        """Start web server"""
        handler_class = self._create_request_handler()

        # Allow address reuse
        socketserver.TCPServer.allow_reuse_address = True

        self.server = socketserver.TCPServer(("", self.port), handler_class)
        print(f"Web interface started at http://localhost:{self.port}")

        # Start in thread
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()

    def stop(self):
        """Stop web server"""
        if self.server:
            self.server.shutdown()

    def _create_request_handler(self):
        """Create custom request handler"""
        api_handler = self.api_handler

        class CustomHandler(http.server.SimpleHTTPRequestHandler):
        """CustomHandler class.

    Args:
        TODO: Add arguments
    """
                """Handle GET requests"""
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path
                params = urllib.parse.parse_qs(parsed.query)

                if path == "/":
                    self._serve_html()
                elif path == "/api/logs":
                    result = api_handler.handle_logs(_params)
                    self._send_json(_result)
                elif path == "/api/stats":
                    result = api_handler.handle_stats(_params)
                    self._send_json(_result)
                else:
                    self.send_error(404)

            def do_POST(self):
                """Handle POST requests"""
                path = urllib.parse.urlparse(self.path).path

                # Read body
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")

                try:
                    data = json.loads(_body) if body else {}
                except:
                    data = {}

                if path == "/api/watch":
                    result = api_handler.handle_watch(_data)
                    self._send_json(_result)
                elif path == "/api/clear":
                    result = api_handler.handle_clear(_data)
                    self._send_json(_result)
                else:
                    self.send_error(404)

            def _serve_html(self):
                """Serve main HTML page"""
                html = self._get_html()
                self._send_response(_html, "text/html")

            def _send_json(self, _data):
                """Send JSON response"""
                content = json.dumps(_data)
                self._send_response(_content, "application/json")

            def _send_response(self, _content, content_type):
                """Send HTTP response"""
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.send_header("Content-length", len(content.encode("utf-8")))
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))

            def _get_html(self):
                """Get HTML content"""
                return """<!DOCTYPE html>
<html>
<head>
    <title>MeowLogger - Modular Edition</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #4fc3f7;
        }
        .controls {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .control-group {
            margin-bottom: 15px;
        }
        label {
            display: inline-block;
            width: 100px;
            font-weight: bold;
        }
        _input, _select, button {
            padding: 8px 12px;
            background: #3a3a3a;
            color: #e0e0e0;
            border: 1px solid #4a4a4a;
            border-radius: 4px;
            margin-right: 10px;
        }
        input { width: 300px; }
        button {
            background: #4fc3f7;
            color: #000;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background: #29b6f6; }
        .stats {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .stat-card {
            background: #3a3a3a;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #4fc3f7;
        }
        .logs {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            height: 500px;
            overflow-y: auto;
        }
        .log-entry {
            padding: 8px;
            margin-bottom: 5px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 13px;
            white-space: pre-wrap;
        }
        .log-DEBUG { background: #1a237e; }
        .log-INFO { background: #004d40; }
        .log-WARNING { background: #f57c00; color: #000; }
        .log-ERROR { background: #d32f2f; }
        .log-CRITICAL { background: #b71c1c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐱 MeowLogger - Modular Edition</h1>

        <div class="controls">
            <div class="control-group">
                <label>Watch Path:</label>
                <input type="text" id="watchPath" placeholder="/var/log or /path/to/file.log">
                <button onclick="addWatch()">Add Watch</button>
            </div>

            <div class="control-group">
                <label>Filter:</label>
                <input type="text" id="search" placeholder="Search logs..." oninput="updateLogs()">
                <select id="level" onchange="updateLogs()">
                    <option value="">All Levels</option>
                    <option value="DEBUG">DEBUG</option>
                    <option value="INFO">INFO</option>
                    <option value="WARNING">WARNING</option>
                    <option value="ERROR">ERROR</option>
                    <option value="CRITICAL">CRITICAL</option>
                </select>
                <button onclick="clearLogs()">Clear</button>
            </div>
        </div>

        <div class="stats" id="stats"></div>

        <div class="logs" id="logs">
            <div style="text-align: center; padding: 50px;">
                Add a watch path to start monitoring logs
            </div>
        </div>
    </div>

    <script>
        let autoRefresh = true;

        async function addWatch() {
            const path = document.getElementById('watchPath').value;
            if (!path) return;

            const response = await fetch('/api/watch', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path: path})
            });

            const result = await response.json();
            alert(result.message);

            if (result.success) {
                document.getElementById('watchPath').value = '';
                updateLogs();
            }
        }

        async function updateLogs() {
            const params = new URLSearchParams({
                search: document.getElementById('search').value,
                level: document.getElementById('level').value,
                limit: 100
            });

            const response = await fetch(`/api/logs?${params}`);
            const data = await response.json();

            const logsDiv = document.getElementById('logs');
            logsDiv.innerHTML = data.logs.map(log => {
                const time = new Date(log.timestamp).toLocaleTimeString();
                return `<div class="log-entry log-${log.level}">
                    [${time}] [${log.level}] ${log.message}
                </div>`;
            }).join('');

            // Auto-scroll
            logsDiv.scrollTop = logsDiv.scrollHeight;
        }

        async function updateStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();

            const statsDiv = document.getElementById('stats');
            statsDiv.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${stats.total_logs}</div>
                    <div>Total Logs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.by_level.ERROR || 0}</div>
                    <div>Errors</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.logs_per_second.toFixed(2)}</div>
                    <div>Logs/sec</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${Math.floor(stats.uptime_seconds)}s</div>
                    <div>Uptime</div>
                </div>
            `;
        }

        async function clearLogs() {
            if (confirm('Clear all logs?')) {
                await fetch('/api/clear', {method: 'POST'});
                updateLogs();
                updateStats();
            }
        }

        // Auto-refresh
        setInterval(() => {
            if (autoRefresh) {
                updateLogs();
                updateStats();
            }
        }, 2000);

        // Initial load
        updateStats();
    </script>
</body>
</html>"""

            def log_message(self, _format, *args):
            """log_message function.

    Args:
        TODO: Add arguments
    """

        return CustomHandler


# ==================== Example Application
