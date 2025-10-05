import gc
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
from datetime import datetime

from modular_core import (
    FileStorage,
    FileWatcher,
    LogEntry,
    LogLevelParser,
    LogProcessor,
    LogStorage,
    MemoryStorage,
    MeowLogger,
    PatternDetector,
)
from modular_web_interface import APIHandler

"""
MeowLogger Complete Test Suite
Comprehensive testing with quality gates

Naming Conventions:
- Mock objects: prefix with 'mock_' (e.g., mock_handler, mock_storage)
- Fake objects: prefix with 'fake_' (e.g., fake_log_entry, fake_file_path)
- Patch decorators: use @patch() with the full path to the object being patched
"""

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup"""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.log")

    def tearDown(self):
        """Clean up test fixtures."""
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            # Non-critical cleanup failure during tests; ignore
            pass

    def create_test_log_file(self, content=""):
        """Create a test log file"""
        with open(self.test_file, "w") as f:
            f.write(content)
        return self.test_file


# ==================== Unit Tests: Core Components ====================


class TestLogEntry(BaseTestCase):
    """Test LogEntry dataclass"""

    def test_mock_usage_example(self):
        """Example of using mock objects for testing callbacks"""
        # Create a mock callback function
        mock_callback = unittest.mock.Mock()

        # Create a log entry with the mock callback
        log_entry = LogEntry(
            timestamp=datetime.now(),
            level="INFO",
            message="Test message",
            on_process=mock_callback,
        )

        # Trigger the callback (if your LogEntry supports _this)
        if hasattr(log_entry, "on_process") and callable(log_entry.on_process):
            log_entry.on_process(log_entry)

            # Verify the mock was called with the log entry
            mock_callback.assert_called_once()

            # Get the first call's first argument
            callback_arg = mock_callback.call_args[0][0]
            self.assertIsInstance(callback_arg, LogEntry)
            self.assertEqual(callback_arg.level, "INFO")

    def test_fake_usage_example(self):
        """Example of using fake objects for testing"""
        # Create a fake timestamp
        fake_timestamp = datetime(2023, 1, 1, 12, 0, 0)

        # Create a fake log entry
        fake_log_entry = LogEntry(
            timestamp=fake_timestamp,
            level="ERROR",
            message="Test error message",
            extra_data={"source": "test", "code": 500},
        )

        # Test the fake entry's properties
        self.assertEqual(fake_log_entry.timestamp, fake_timestamp)
        self.assertEqual(fake_log_entry.level, "ERROR")
        self.assertEqual(fake_log_entry.message, "Test error message")
        self.assertEqual(fake_log_entry.extra_data["code"], 500)

    def test_creation(self):
        """Test LogEntry creation"""
        entry = LogEntry(timestamp=datetime.now(), level="INFO", message="Test message")
        self.assertEqual(entry.level, "INFO")
        self.assertEqual(entry.message, "Test message")
        self.assertIsNone(entry.file_path)

    def test_to_dict(self):
        """Test dictionary conversion"""
        now = datetime.now()
        entry = LogEntry(
            timestamp=now,
            level="ERROR",
            message="Error occurred",
            extra_data={"code": 500},
        )

        result = entry.to_dict()
        self.assertEqual(result["level"], "ERROR")
        self.assertEqual(result["message"], "Error occurred")
        self.assertEqual(result["extra_data"]["code"], 500)
        self.assertEqual(result["timestamp"], now.isoformat())


class TestFileWatcher(BaseTestCase):
    """Test FileWatcher component"""

    def test_initialization(self):
        """Test watcher initialization"""
        watcher = FileWatcher(poll_interval=0.1)
        self.assertEqual(watcher.poll_interval, 0.1)
        self.assertEqual(len(watcher.handlers), 0)
        self.assertFalse(watcher.running)

    def test_add_handler(self):
        """Test adding handlers"""
        watcher = FileWatcher()
        mock_handler1 = unittest.mock.Mock()
        mock_handler2 = unittest.mock.Mock()

        watcher.add_handler(mock_handler1)
        watcher.add_handler(mock_handler2)

        self.assertEqual(len(watcher.handlers), 2)
        self.assertIn(mock_handler1, watcher.handlers)
        self.assertIn(mock_handler2, watcher.handlers)

    def test_watch_file(self):
        """Test watching a single file"""
        self.create_test_log_file("Initial content")

        watcher = FileWatcher()
        watcher.watch_file(self.test_file)

        self.assertIn(self.test_file, watcher.watched_files)
        self.assertEqual(watcher.watched_files[self.test_file], 15)  # "Initial content"

    def test_watch_directory(self):
        """Test watching a directory"""
        # Create multiple log files
        log1 = os.path.join(self.test_dir, "app1.log")
        log2 = os.path.join(self.test_dir, "app2.log")
        txt1 = os.path.join(self.test_dir, "notes.txt")

        for _f in [log1, _log2, txt1]:
            open(_f, "w").close()

        watcher = FileWatcher()
        watcher.watch_directory(self.test_dir, "*.log")

        # Should only watch .log files
        self.assertIn(_log1, watcher.watched_files)
        self.assertIn(_log2, watcher.watched_files)
        self.assertNotIn(_txt1, watcher.watched_files)

    def test_file_change_detection(self):
        """Test detecting file changes"""
        self.create_test_log_file("Line 1\n")

        handler_calls = []

        def handler(file_path, line_text):
            """Handler function for file changes."""
            handler_calls.append((file_path, line_text))

        watcher = FileWatcher(poll_interval=0.1)
        watcher.add_handler(handler)
        watcher.watch_file(self.test_file)
        watcher.start()

        # Give it time to start
        time.sleep(0.2)

        # Append to file
        with open(self.test_file, "a") as f:
            f.write("Line 2\n")

        # Wait for detection
        time.sleep(0.3)

        watcher.stop()

        # Check handler was called
        self.assertEqual(len(handler_calls), 1)
        self.assertEqual(handler_calls[0], (self.test_file, "Line 2"))


class TestLogLevelParser(BaseTestCase):
    """Test log level parsing"""

    def test_bracket_format(self):
        """Test [LEVEL] format"""
        parser = LogLevelParser()
        entry = LogEntry(datetime.now(), "INFO", "[ERROR] Something failed")

        result = parser.process(_entry)
        self.assertIsNotNone(_result)
        level = result["level"] if result is not None else None
        self.assertEqual(_level, "ERROR")

    def test_colon_format(self):
        """Test LEVEL: format"""
        parser = LogLevelParser()
        entry = LogEntry(datetime.now(), "INFO", "WARNING: Low memory")

        result = parser.process(_entry)
        self.assertIsNotNone(_result)
        level = result["level"] if result is not None else None
        self.assertEqual(_level, "WARNING")

    def test_word_format(self):
        """Test plain word format"""
        parser = LogLevelParser()
        entry = LogEntry(datetime.now(), "INFO", "Application started DEBUG mode")

        result = parser.process(_entry)
        self.assertIsNotNone(_result)
        level = result["level"] if result is not None else None
        self.assertEqual(_level, "DEBUG")

    def test_default_level(self):
        """Test default level when no match"""
        parser = LogLevelParser()
        entry = LogEntry(datetime.now(), "INFO", "Just a regular message")

        result = parser.process(_entry)
        self.assertIsNotNone(_result)
        level = result["level"] if result is not None else None
        self.assertEqual(_level, "INFO")


class TestPatternDetector(BaseTestCase):
    """Test pattern detection"""

    def test_error_detection(self):
        """Test error pattern detection"""
        detector = PatternDetector()
        entry = LogEntry(datetime.now(), "ERROR", "Critical error occurred in module")

        result = detector.process(_entry)
        self.assertIsNotNone(_result)
        patterns = result.get("patterns", []) if result is not None else []
        self.assertIn("error", _patterns)

    def test_performance_detection(self):
        """Test performance pattern detection"""
        detector = PatternDetector()
        entry = LogEntry(datetime.now(), "INFO", "Request completed in 125.5ms")

        result = detector.process(_entry)
        self.assertIsNotNone(_result)
        patterns = result.get("patterns", []) if result is not None else []
        self.assertIn("performance", _patterns)

    def test_ip_detection(self):
        """Test IP address detection"""
        detector = PatternDetector()
        entry = LogEntry(datetime.now(), "INFO", "Connection from 192.168.1.100")

        result = detector.process(_entry)
        self.assertIsNotNone(_result)
        patterns = result.get("patterns", []) if result is not None else []
        self.assertIn("ip_address", _patterns)

    def test_multiple_patterns(self):
        """Test multiple pattern detection"""
        detector = PatternDetector()
        entry = LogEntry(
            datetime.now(),
            "ERROR",
            "Error: Request to https://api.example.com failed from 10.0.0.1",
        )

        result = detector.process(_entry)
        self.assertIsNotNone(_result)
        patterns = result.get("patterns", []) if result is not None else []
        self.assertIn("error", _patterns)
        self.assertIn("url", _patterns)
        self.assertIn("ip_address", _patterns)


class TestMemoryStorage(BaseTestCase):
    """Test memory storage backend"""

    def test_store_and_retrieve(self):
        """Test basic storage and retrieval"""
        storage = MemoryStorage(max_entries=10)

        # Store entries
        for _i in range(5):
            entry = LogEntry(
                timestamp=datetime.now(), level="INFO", message=f"Message {i}"
            )
            storage.store(_entry)

        # Retrieve all
        entries = storage.retrieve({}, limit=10)
        self.assertEqual(len(_entries), 5)
        self.assertEqual(entries[0].message, "Message 4")  # Most recent first

    def test_level_filtering(self):
        """Test filtering by level"""
        storage = MemoryStorage()

        # Store mixed levels
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "INFO"]
        for _i, level in enumerate(_levels):
            entry = LogEntry(datetime.now(), _level, f"Message {i}")
            storage.store(_entry)

        # Filter by level
        info_entries = storage.retrieve({"level": "INFO"})
        self.assertEqual(len(info_entries), 2)

        error_entries = storage.retrieve({"level": "ERROR"})
        self.assertEqual(len(error_entries), 1)

    def test_search_filtering(self):
        """Test text search filtering"""
        storage = MemoryStorage()

        messages = [
            "User logged in",
            "Database connection failed",
            "User logged out",
            "Cache cleared",
        ]

        for _msg in messages:
            entry = LogEntry(datetime.now(), "INFO", _msg)
            storage.store(_entry)

        # Search for "user"
        user_entries = storage.retrieve({"search": "user"})
        self.assertEqual(len(user_entries), 2)

    def test_size_limit(self):
        """Test max entries limit"""
        storage = MemoryStorage(max_entries=3)

        # Store more than limit
        for _i in range(5):
            entry = LogEntry(datetime.now(), "INFO", f"Message {i}")
            storage.store(_entry)

        # Should only have last 3
        entries = storage.retrieve({})
        self.assertEqual(len(_entries), 3)
        self.assertEqual(entries[0].message, "Message 4")


class TestFileStorage(BaseTestCase):
    """Test file storage backend"""

    def test_store_and_retrieve(self):
        """Test file storage operations"""
        storage_file = os.path.join(self.test_dir, "logs.json")
        storage = FileStorage(storage_file, max_size=1024 * 1024)

        # Store entries
        for _i in range(3):
            entry = LogEntry(datetime.now(), "INFO", f"Message {i}")
            storage.store(_entry)

        # Check file exists
        self.assertTrue(os.path.exists(storage_file))

        # Retrieve entries
        entries = storage.retrieve({})
        self.assertEqual(len(_entries), 3)

    def test_file_rotation(self):
        """Test log file rotation"""
        storage_file = os.path.join(self.test_dir, "logs.json")
        storage = FileStorage(storage_file, max_size=100, backup_count=2)

        # Store enough to trigger rotation
        for _i in range(20):
            entry = LogEntry(datetime.now(), "INFO", f"Long message {i} " * 10)
            storage.store(_entry)

        # Check rotation occurred
        self.assertTrue(os.path.exists(storage_file))
        self.assertTrue(os.path.exists(f"{storage_file}.1"))


class TestMeowLogger(BaseTestCase):
    """Test main logger system"""

    def test_initialization(self):
        """Test logger initialization"""
        logger = MeowLogger()
        self.assertIsInstance(logger.storage, MemoryStorage)
        self.assertEqual(len(logger.processors), 2)  # Default processors
        self.assertIsInstance(logger.watcher, FileWatcher)

    def test_direct_logging(self):
        """Test direct log method"""
        logger = MeowLogger()

        logger.log("INFO", "Test message", user="alice")
        logger.log("ERROR", "Error occurred", code=500)

        entries = logger.get_logs()
        self.assertEqual(len(_entries), 2)
        self.assertEqual(entries[0].level, "ERROR")
        extra = entries[0].extra_data or {}
        self.assertEqual(extra["code"], 500)

    def test_file_watching_integration(self):
        """Test file watching with processing"""
        self.create_test_log_file()

        logger = MeowLogger()
        logger.watch(self.test_file)
        logger.start()

        # Append to file
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("[ERROR] Database connection failed\n")
            f.write("[INFO] Retry attempt 1\n")

        # Wait for processing
        time.sleep(0.2)

        logger.stop()

        # Check entries were processed
        entries = logger.get_logs()
        self.assertEqual(len(_entries), 2)

        # Check level was parsed correctly
        error_entry = next(e for _e in entries if "Database" in e.message)
        self.assertEqual(error_entry.level, "ERROR")

    def test_statistics_tracking(self):
        """Test statistics are tracked correctly"""
        logger = MeowLogger()

        # Log various entries
        logger.log("INFO", "Info message 1")
        logger.log("INFO", "Info message 2")
        logger.log("ERROR", "Error message")
        logger.log("WARNING", "Warning message")

        # Check stats
        self.assertEqual(logger.stats["total_logs"], 4)
        self.assertEqual(logger.stats["by_level"]["INFO"], 2)
        self.assertEqual(logger.stats["by_level"]["ERROR"], 1)
        self.assertEqual(logger.stats["by_level"]["WARNING"], 1)


# ==================== Integration Tests ====================


class TestWebInterface(BaseTestCase):
    """Test web interface integration"""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.logger = MeowLogger()
        self.api = APIHandler(self.logger)

    def test_logs_api(self):
        """Test logs API endpoint"""
        # Add some logs
        self.logger.log("INFO", "Test 1")
        self.logger.log("ERROR", "Test 2")
        self.logger.log("INFO", "Test 3")

        # Test retrieval
        result = self.api.handle_logs({})
        self.assertEqual(len(result["logs"]), 3)

        # Test filtering
        result = self.api.handle_logs({"level": "ERROR"})
        self.assertEqual(len(result["logs"]), 1)

    def test_stats_api(self):
        """Test stats API endpoint"""
        # Add logs
        for _i in range(5):
            self.logger.log("INFO", f"Message {i}")

        result = self.api.handle_stats({})
        self.assertIsNotNone(_result)
        self.assertEqual(result["total_logs"], 5)
        self.assertIn("uptime_seconds", _result)
        self.assertIn("logs_per_second", _result)

    def test_watch_api(self):
        """Test watch API endpoint"""
        # Valid path
        result = self.api.handle_watch({"path": self.test_dir})
        self.assertTrue(result["success"])

        # Invalid path
        result = self.api.handle_watch({"path": "/invalid/path"})
        self.assertFalse(result["success"])

    def test_clear_api(self):
        """Test clear API endpoint"""
        # Add logs
        self.logger.log("INFO", "Test")
        self.assertEqual(self.logger.stats["total_logs"], 1)

        # Clear
        result = self.api.handle_clear({})
        self.assertTrue(result["success"])

        # Check cleared
        self.assertEqual(self.logger.stats["total_logs"], 0)
        entries = self.logger.get_logs()
        self.assertEqual(len(_entries), 0)


# ==================== Performance Tests ====================


class TestPerformance(BaseTestCase):
    """Performance and stress tests"""

    def test_logging_throughput(self):
        """Test logging performance"""
        logger = MeowLogger()

        start_time = time.time()
        num_logs = 1000

        for _i in range(num_logs):
            logger.log("INFO", f"Performance test message {i}")

        elapsed = time.time() - start_time
        throughput = num_logs / elapsed

        # Should handle at least 500 logs/second
        self.assertGreater(
            _throughput, 500, f"Low throughput: {throughput:.0f} logs/sec"
        )

    def test_memory_usage(self):
        """Test memory efficiency"""
        logger = MeowLogger()
        logger.set_storage(MemoryStorage(max_entries=1000))

        # Baseline
        gc.collect()
        initial_objects = len(gc.get_objects())

        # Add many logs
        for _i in range(2000):
            logger.log("INFO", f"Memory test {i}")

        # Force GC
        gc.collect()
        final_objects = len(gc.get_objects())

        # Check we're not leaking too much
        growth = final_objects - initial_objects
        self.assertLess(_growth, 2000, f"Memory growth too high: {growth}")

    def test_concurrent_access(self):
        """Test thread safety"""
        logger = MeowLogger()
        errors = []

        def log_worker(worker_id):
            """Log worker function for testing concurrent access."""
            try:
                for i in range(100):
                    logger.log("INFO", f"Worker {worker_id} message {i}")
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads = []
        for _i in range(5):
            t = threading.Thread(target=log_worker, args=(_i,))
            threads.append(_t)
            t.start()

        # Wait for completion
        for _t in threads:
            t.join()

        # Check no errors
        self.assertEqual(len(_errors), 0)
        self.assertEqual(logger.stats["total_logs"], 500)


# ==================== Quality Gate Checks ====================


class TestQualityGates(unittest.TestCase):
    """Quality gate validation tests"""

    def test_code_structure(self):
        """Verify code structure and imports"""
        # Check modular_core exists and has required classes
        self.assertTrue(hasattr(LogProcessor, "__abstractmethods__"))
        self.assertTrue(hasattr(LogStorage, "__abstractmethods__"))

    def test_error_handling(self):
        """Test error handling in critical paths"""
        # Test invalid file path
        logger = MeowLogger()
        try:
            logger.watch("/definitely/not/a/real/path")
            self.fail("Should raise exception for invalid path")
        except ValueError:
            pass

        # Test invalid storage
        storage = FileStorage("/invalid/path/file.log")
        entry = LogEntry(datetime.now(), "INFO", "Test")

        # Should not crash on write failure
        storage.store(_entry)  # Should handle gracefully

    def test_documentation(self):
        """Verify documentation exists"""
        self.assertIsNotNone(MeowLogger.__doc__)
        self.assertIsNotNone(FileWatcher.__doc__)
        self.assertIsNotNone(MeowLogger.log.__doc__)

    def test_type_safety(self):
        """Test type handling"""
        logger = MeowLogger()

        # Should handle various input types gracefully
        logger.log("INFO", "String message")
        logger.log("INFO", 123)  # Number
        logger.log("INFO", {"dict": "message"})  # Dict
        logger.log("INFO", None)  # None

        # Should not crash
        entries = logger.get_logs()
        self.assertEqual(len(_entries), 4)


# ==================== Test Runner ====================


def run_all_tests():
    """Run all tests with summary"""
    print("=" * 70)
    print("MeowLogger Quality Gate Tests")
    print("=" * 70)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestLogEntry,
        TestFileWatcher,
        TestLogLevelParser,
        TestPatternDetector,
        TestMemoryStorage,
        TestFileStorage,
        TestMeowLogger,
        TestWebInterface,
        TestPerformance,
        TestQualityGates,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(_tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(_suite)

    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ All quality gates passed!")
        print("The modular system is ready for testing.")
    else:
        print("\n❌ Quality gate failures detected.")
        print("Please fix the issues before proceeding.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
