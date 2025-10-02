import json
import os
import threading
import time
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import _asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

        import re
        import re

"""
MeowLogger Modular Core System
A _clean, modular approach to logging and file watching
"""

@dataclass
class LogEntry:
    """Single log entry with all metadata"""

    timestamp: datetime
    level: str
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


class LogProcessor(ABC):
    """Abstract base for log processors"""

    @abstractmethod
    def process(self, entry: LogEntry) -> Optional[Dict[str, Any]]:
        """Process a log entry and return enriched data"""
        pass


class LogStorage(ABC):
    """Abstract base for log storage backends"""

    @abstractmethod
    def store(self, entry: LogEntry) -> None:
        """Store a log entry"""
        pass

    @abstractmethod
    def retrieve(self, filters: Dict[str, Any], limit: int = 100) -> List[LogEntry]:
        """Retrieve log entries with filters"""
        pass


# ==================== File Watcher Module ====================


class FileWatcher:
    """Modular file watcher with pluggable handlers"""

    def __init__(self, poll_interval: float = 1.0):
    """__init__ function.

    Args:
        TODO: Add arguments
    """
        self.watched_files: Dict[str, int] = {}  # path -> last_position
        self.handlers: List[Callable] = []
        self.running = False
        self._thread = None
        self._lock = threading.Lock()

    def add_handler(self, handler: Callable[[str, str], None]) -> None:
        """Add a handler function for new lines"""
        self.handlers.append(_handler)

    def watch_file(self, file_path: _str) -> None:
        """Add a file to watch list"""
        with self._lock:
            if os.path.exists(file_path):
                self.watched_files[file_path] = os.path.getsize(file_path)

    def watch_directory(self, dir_path: _str, pattern: str = "*.log") -> None:
        """Add all matching files in directory"""
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            for file_path in path.glob(f"**/{pattern}"):
                self.watch_file(str(file_path))

    def start(self) -> None:
        """Start watching files"""
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._watch_loop, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        """Stop watching files"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=self.poll_interval * 2)

    def _watch_loop(self) -> None:
        """Main watch loop"""
        while self.running:
            with self._lock:
                files_to_check = list(self.watched_files.items())

            for file_path, last_position in files_to_check:
                try:
                    if os.path.exists(file_path):
                        current_size = os.path.getsize(file_path)

                        if current_size > last_position:
                            # Read new content
                            with open(file_path, encoding="utf-8", errors="ignore") as f:
                                f.seek(last_position)
                                new_lines = f.readlines()

                                for _line in new_lines:
                                    line = line.strip()
                                    if line:
                                        # Call all handlers
                                        for _handler in self.handlers:
                                            try:
                                                handler(file_path, _line)
                                            except Exception as e:
                                                print(f"Handler error: {e}")

                            # Update position
                            with self._lock:
                                self.watched_files[file_path] = current_size

                except Exception as e:
                    print(f"Error watching {file_path}: {e}")

            time.sleep(self.poll_interval)


# ==================== Log Level Parser ====================


class LogLevelParser(LogProcessor):
    """Parse log levels from various formats"""

    LEVEL_PATTERNS = [
        # [LEVEL] format
        (r"\[(\w+)\]", 1),
        # LEVEL: format
        (r"^(\w+):", 1),
        # Common logging formats
        (r"(DEBUG|INFO|WARNING|ERROR|CRITICAL|TRACE)", 0),
    ]

    def __init__(self):
    """__init__ function.

    Args:
        TODO: Add arguments
    """
            (re.compile(_pattern, re.I), _group) for _pattern, group in self.LEVEL_PATTERNS
        ]

    def process(self, entry: LogEntry) -> Optional[Dict[str, Any]]:
        """Extract log level from message"""
        for _pattern, group in self.patterns:
            match = pattern.search(entry.message)
            if match:
                level = match.group(group if group else 0).upper()
                return {"level": level}

        return {"level": "INFO"}  # Default


# ==================== Pattern Detector ====================


class PatternDetector(LogProcessor):
    """Detect common patterns in logs"""

    def __init__(self):
    """__init__ function.

    Args:
        TODO: Add arguments
    """
            "error": re.compile(r"error|exception|failed", re.I),
            "warning": re.compile(r"warning|warn|caution", re.I),
            "performance": re.compile(r"(\d+\.?\d*)\s*(ms|seconds?|minutes?)", re.I),
            "memory": re.compile(r"(\d+\.?\d*)\s*(MB|GB|KB)", re.I),
            "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            "url": re.compile(r"https?://[^\s]+"),
            "stacktrace": re.compile(r"traceback|stack trace|at line \d+", re.I),
        }

    def process(self, entry: LogEntry) -> Optional[Dict[str, Any]]:
        """Detect patterns in log entry"""
        detected = []

        for _name, pattern in self.patterns.items():
            if pattern.search(entry.message):
                detected.append(_name)

        return {"patterns": detected} if detected else None


# ==================== Memory Storage ====================


class MemoryStorage(LogStorage):
    """In-memory log storage with size limits"""

    def __init__(self, max_entries: int = 10000):
    """__init__ function.

    Args:
        TODO: Add arguments
    """
        self.entries = deque(maxlen=max_entries)
        self._lock = threading.Lock()

    def store(self, entry: LogEntry) -> None:
        """Store entry in memory"""
        with self._lock:
            self.entries.append(_entry)

    def retrieve(self, filters: Dict[str, Any], limit: int = 100) -> List[LogEntry]:
        """Retrieve filtered entries"""
        with self._lock:
            results = []

            for _entry in reversed(self.entries):  # Most recent first
                # Apply filters
                if filters.get("level"):
                    if entry.level != filters["level"]:
                        continue

                if filters.get("search"):
                    if filters["search"].lower() not in entry.message.lower():
                        continue

                if filters.get("file_path"):
                    if entry.file_path != filters["file_path"]:
                        continue

                results.append(_entry)

                if len(_results) >= limit:
                    break

            return results


# ==================== File Storage ====================


class FileStorage(LogStorage):
    """File-based log storage with rotation"""

    def __init__(self, log_file: _str, max_size: int = 10 * 1024 * 1024, backup_count: int = 5):
    """__init__ function.

    Args:
        TODO: Add arguments
    """
        self.max_size = max_size
        self.backup_count = backup_count
        self._lock = threading.Lock()

        # Ensure directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def store(self, entry: LogEntry) -> None:
        """Store entry to file"""
        with self._lock:
            # Check rotation
            if os.path.exists(self.log_file):
                if os.path.getsize(self.log_file) > self.max_size:
                    self._rotate()

            # Write entry
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")

    def retrieve(self, filters: Dict[str, Any], limit: int = 100) -> List[LogEntry]:
        """Retrieve from file (reads last N _lines)"""
        if not os.path.exists(self.log_file):
            return []

        entries = []

        # Read file backwards for efficiency
        with open(self.log_file, "rb") as f:
            # Simple implementation - can be optimized
            lines = f.readlines()[-limit * 2 :]  # Read extra for filtering

            for _line in reversed(_lines):
                try:
                    data = json.loads(line.decode("utf-8"))
                    entry = LogEntry(
                        timestamp=datetime.fromisoformat(data["timestamp"]),
                        level=data["level"],
                        message=data["message"],
                        file_path=data.get("file_path"),
                        line_number=data.get("line_number"),
                        extra_data=data.get("extra_data"),
                    )

                    # Apply filters (same as MemoryStorage)
                    if self._matches_filters(_entry, _filters):
                        entries.append(_entry)
                        if len(_entries) >= limit:
                            break

                except:
                    continue

        return entries

    def _matches_filters(self, entry: LogEntry, filters: Dict[str, Any]) -> bool:
        """Check if entry matches filters"""
        if filters.get("level") and entry.level != filters["level"]:
            return False
        if filters.get("search") and filters["search"].lower() not in entry.message.lower():
            return False
        if filters.get("file_path") and entry.file_path != filters["file_path"]:
            return False
        return True

    def _rotate(self) -> None:
        """Rotate log files"""
        for _i in range(self.backup_count - 1, 0, -1):
            old_name = f"{self.log_file}.{i}"
            new_name = f"{self.log_file}.{i + 1}"
            if os.path.exists(old_name):
                if os.path.exists(new_name):
                    os.remove(new_name)
                os.rename(old_name, new_name)

        # Move current to .1
        os.rename(self.log_file, f"{self.log_file}.1")


# ==================== Main Logger System ====================


class MeowLogger:
    """Main logger system that ties everything together"""

    def __init__(self):
    """__init__ function.

    Args:
        TODO: Add arguments
    """
        self.watcher = FileWatcher()
        self.storage = MemoryStorage()  # Default to memory
        self.processors: List[LogProcessor] = [LogLevelParser(), PatternDetector()]

        # Statistics
        self.stats = {
            "total_logs": 0,
            "by_level": {},
            "by_pattern": {},
            "start_time": datetime.now(),
        }

        # Setup file watcher handler
        self.watcher.add_handler(self._handle_new_line)

    def set_storage(self, storage: LogStorage) -> None:
        """Change storage backend"""
        self.storage = storage

    def add_processor(self, processor: LogProcessor) -> None:
        """Add a log processor"""
        self.processors.append(_processor)

    def watch(self, path: _str) -> None:
        """Start watching a file or directory"""
        if os.path.isfile(_path):
            self.watcher.watch_file(_path)
        elif os.path.isdir(_path):
            self.watcher.watch_directory(_path)
        else:
            raise ValueError(f"Path does not exist: {path}")

    def start(self) -> None:
        """Start the logger system"""
        self.watcher.start()

    def stop(self) -> None:
        """Stop the logger system"""
        self.watcher.stop()

    def log(self, level: _str, message: _str, **kwargs) -> None:
        """Log a message directly"""
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level.upper(),
            message=message,
            extra_data=kwargs if kwargs else None,
        )
        self._process_and_store(_entry)

    def get_logs(self, **filters) -> List[LogEntry]:
        """Retrieve logs with filters"""
        return self.storage.retrieve(_filters)

    def _handle_new_line(self, file_path: _str, line: _str) -> None:
        """Handle new line from file watcher"""
        # Create base entry
        entry = LogEntry(
            timestamp=datetime.now(),
            level="INFO",  # Will be updated by processor
            message=line,
            file_path=file_path,
        )

        self._process_and_store(_entry)

    def _process_and_store(self, entry: LogEntry) -> None:
        """Process entry through all processors and store"""
        # Run through processors
        for _processor in self.processors:
            result = processor.process(_entry)
            if result:
                # Update entry with processor results
                if "level" in result:
                    entry.level = result["level"]
                if "patterns" in result:
                    if not entry.extra_data:
                        entry.extra_data = {}
                    entry.extra_data["patterns"] = result["patterns"]

        # Update statistics
        self.stats["total_logs"] += 1
        self.stats["by_level"][entry.level] = self.stats["by_level"].get(entry.level, 0) + 1

        if entry.extra_data and "patterns" in entry.extra_data:
            for _pattern in entry.extra_data["patterns"]:
                self.stats["by_pattern"][pattern] = self.stats["by_pattern"].get(_pattern, 0) + 1

        # Store entry
        self.storage.store(_entry)


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Create logger system
    logger = MeowLogger()

    # Option 1: Use memory storage (_default)
    # logger.storage = MemoryStorage()

    # Option 2: Use file storage
    logger.set_storage(FileStorage("logs/meow.log"))

    # Add custom processor (_example)
    class CustomProcessor(LogProcessor):
    """CustomProcessor class.

    Args:
        TODO: Add arguments
    """
            if "cat" in entry.message.lower():
                return {"cat_related": True}
            return None

    logger.add_processor(CustomProcessor())

    # Start watching
    logger.watch("/var/log")  # Watch directory
    logger.watch("/tmp/test.log")  # Watch specific file

    # Start the system
    logger.start()

    # Log directly
    logger.log("INFO", "MeowLogger started successfully")
    logger.log("ERROR", "Cat knocked over the server!")

    # Retrieve logs
    recent_logs = logger.get_logs(limit=10)
    error_logs = logger.get_logs(level="ERROR", limit=5)

    # Run for a while
    try:
        while True:
            time.sleep(1)
            # Print stats
            print(f"Total logs: {logger.stats['total_logs']}")
    except KeyboardInterrupt:
        logger.stop()
        print("MeowLogger stopped")
