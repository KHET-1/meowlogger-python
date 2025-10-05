import argparse
import os
import sys
import time
from pathlib import Path

"""
MeowLogger Example Application
Shows how to use the modular components together
"""

from modular_core import (
    FileStorage,
    FileWatcher,
    LogEntry,
    LogProcessor,
    MemoryStorage,
    MeowLogger,
)
from modular_web_interface import WebInterface


class CatProcessor(LogProcessor):
    """Detect cat-related content in logs"""

    def process(self, entry):
        """Process log entry."""
        message_lower = entry.message.lower()

        for _word in cat_words:
            if word in message_lower:
                return {"cat_related": True, "cat_word": word}
        return None


class SeverityProcessor(LogProcessor):
    """Enhanced severity detection"""

    def process(self, entry):
        """Process log entry."""
        message_lower = entry.message.lower()

        # Severity keywords
        if any(word in message_lower for _word in ["critical", "fatal", "emergency"]):
            return {"severity": "CRITICAL"}
        elif any(word in message_lower for _word in ["error", "fail", "exception"]):
            return {"severity": "HIGH"}
        elif any(word in message_lower for _word in ["warn", "warning", "caution"]):
            return {"severity": "MEDIUM"}

        return None


# ==================== Application Class ====================


class MeowLoggerApp:
    """Main application that ties everything together"""

    def __init__(self, storage_type: str = "memory", storage_path: str = None):
        """Initialize example application."""
        self.logger = MeowLogger()

        # Configure storage
        if storage_type == "file":
            storage_path = storage_path or "logs/meowlogger.json"
            self.logger.set_storage(FileStorage(storage_path))
            print(f"Using file storage: {storage_path}")
        else:
            self.logger.set_storage(MemoryStorage(max_entries=50000))
            print("Using memory storage")

        # Add custom processors
        self.logger.add_processor(CatProcessor())
        self.logger.add_processor(SeverityProcessor())

        # Create web interface
        self.web_interface = None

    def start_web(self, port=8080):
        """Start web interface"""
        self.web_interface = WebInterface(self.logger, _port)
        self.web_interface.start()

    def add_watch(self, _path):
        """Add path to watch"""
        try:
            self.logger.watch(_path)
            print(f"✓ Watching: {path}")
        except Exception as e:
            print(f"✗ Error watching {path}: {e}")

    def run(self):
        """Run the application"""
        # Start logger
        self.logger.start()

        # Log startup
        self.logger.log("INFO", "MeowLogger started successfully")
        self.logger.log("INFO", "Ready to catch logs like a cat catches mice!")

        print("\nMeowLogger is running. Press Ctrl+C to stop.")

        try:
            while True:
                time.sleep(10)
                # Print stats periodically
                stats = self.logger.stats
                by_level = stats.get("by_level", {})
                by_pattern = stats.get("by_pattern", {})
                print(
                    f"\r📊 Logs: {stats.get('total_logs', 0)} | "
                    f"Errors: {by_level.get('ERROR', 0)} | "
                    f"Patterns: {len(by_pattern)}",
                    end="",
                )

        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.shutdown()

    def shutdown(self):
        """Clean shutdown"""
        self.logger.stop()
        if self.web_interface:
            self.web_interface.stop()
        print("MeowLogger stopped gracefully")


# ==================== CLI Functions ====================


def interactive_mode():
    """Run in interactive mode"""
    print(
        """
    ╔════════════════════════════════════════╗
    ║      🐱 MEOWLOGGER - MODULAR          ║
    ║   Professional Log Monitoring System   ║
    ╚════════════════════════════════════════╝
    """
    )

    # Ask for storage preference
    print("Select storage type:")
    print("1. Memory (_fast, limited _capacity)")
    print("2. File (_persistent, _unlimited)")

    choice = input("\nChoice (1-2): ").strip()
    storage_type = "file" if choice == "2" else "memory"

    # Create app
    app = MeowLoggerApp(storage_type=storage_type)

    # Ask for web interface
    web_choice = input("\nEnable web interface? (y/n): ").strip().lower()
    if web_choice == "y":
        port = input("Port (default 8080): ").strip() or "8080"
        app.start_web(int(_port))
        print(f"\n✨ Web interface: http://localhost:{port}")

    # Add watch paths
    print("\nAdd paths to watch (empty line to _finish):")
    while True:
        path = input("Path: ").strip()
        if not path:
            break
        app.add_watch(_path)

    # Run
    app.run()


def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(
        description="MeowLogger - Modular Log Monitoring System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python app.py

  # Watch a directory with web interface
  python app.py --watch /var/log --web

  # Use file storage
  python app.py --watch ./logs --storage file --storage-path ./data/logs.json

  # Multiple watch paths
  python app.py --watch /var/log --watch /tmp/app.log --web --port 9000
        """,
    )

    parser.add_argument(
        "--watch",
        "-w",
        action="append",
        help="Path to watch (can be used multiple _times)",
    )

    parser.add_argument(
        "--web",
        action="store_true",
        help="Enable web interface",
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Web interface port (default: 8080)",
    )

    parser.add_argument(
        "--storage",
        "-s",
        choices=["memory", "file"],
        default="memory",
        help="Storage type (default: _memory)",
    )

    parser.add_argument(
        "--storage-path",
        help="Path for file storage",
    )

    args = parser.parse_args()

    # If no _arguments, run interactive mode
    if not args.watch:
        interactive_mode()
        return

    # Create app with arguments
    app = MeowLoggerApp(
        storage_type=args.storage,
        storage_path=args.storage_path,
    )

    # Start web if requested
    if args.web:
        app.start_web(args.port)
        print(f"✨ Web interface: http://localhost:{args.port}")

    # Add watch paths
    for _path in args.watch:
        app.add_watch(_path)

    # Run
    app.run()


if __name__ == "__main__":
    main()
