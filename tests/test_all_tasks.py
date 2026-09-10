"""
Independent Verification Test Suite for Tasks T01 - T10 using Python standard unittest
"""
import unittest
import asyncio
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tasks")))

from t01_fastapi_crud import UserService, UserCreate
from t02_sql_migration import MigrationManager
from t03_redis_rate_limiter import SlidingWindowRateLimiter
from t04_topological_sort import topological_sort
from t05_payment_decoupling import MockStripeAdapter, CheckoutService
from t06_async_migration import process_all_sources
from t07_datetime_parser import parse_iso_datetime
from t08_bank_transfer_concurrency import ThreadSafeAccount, safe_transfer
from t09_websocket_manager import WebSocketPool
from t10_oauth2_pkce import PKCEAuthFlow

class TestAllTasks(unittest.TestCase):
    def test_t01_user_service(self):
        svc = UserService()
        u = svc.create_user(UserCreate(username="alice", email="alice@test.com"))
        self.assertEqual(u.id, 1)
        self.assertEqual(svc.get_user(1).username, "alice")
        self.assertIsNone(svc.get_user(999))

    def test_t02_migration(self):
        mgr = MigrationManager()
        self.assertTrue(mgr.up())
        self.assertIn("audit_logs", mgr.schema_state)
        self.assertTrue(mgr.down())
        self.assertNotIn("audit_logs", mgr.schema_state)

    def test_t03_rate_limiter(self):
        limiter = SlidingWindowRateLimiter(limit=3, window_seconds=10.0)
        self.assertTrue(limiter.allow_request(100.0))
        self.assertTrue(limiter.allow_request(101.0))
        self.assertTrue(limiter.allow_request(102.0))
        self.assertFalse(limiter.allow_request(103.0))
        self.assertTrue(limiter.allow_request(111.0))

    def test_t04_topological_sort(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        order = topological_sort(graph)
        self.assertLess(order.index("A"), order.index("B"))
        self.assertLess(order.index("B"), order.index("D"))
        
        cycle_graph = {"X": ["Y"], "Y": ["X"]}
        with self.assertRaises(ValueError):
            topological_sort(cycle_graph)

    def test_t05_payment_adapter(self):
        gateway = MockStripeAdapter()
        checkout = CheckoutService(gateway)
        res = checkout.process_order(5000, "tok_123456")
        self.assertEqual(res["status"], "succeeded")
        with self.assertRaises(ValueError):
            checkout.process_order(5000, "invalid_token")

    def test_t06_async_pipeline(self):
        results = asyncio.run(process_all_sources([1, 2, 3]))
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], 1)

    def test_t07_datetime_parser(self):
        dt = parse_iso_datetime("2026-03-10T14:30:00Z")
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.minute, 30)
        with self.assertRaises(ValueError):
            parse_iso_datetime("invalid-date-string")

    def test_t08_threadsafe_transfer(self):
        acc1 = ThreadSafeAccount("ACC_1", 1000.0)
        acc2 = ThreadSafeAccount("ACC_2", 500.0)
        
        def worker():
            for _ in range(50):
                safe_transfer(acc1, acc2, 10.0)
        
        threads = [threading.Thread(target=worker) for _ in range(2)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.assertEqual(acc1.balance, 0.0)
        self.assertEqual(acc2.balance, 1500.0)

    def test_t09_websocket_pool(self):
        pool = WebSocketPool()
        pool.connect("client_1")
        pool.connect("client_2")
        self.assertEqual(pool.broadcast_count(), 2)
        pool.disconnect("client_1")
        self.assertEqual(pool.broadcast_count(), 1)

    def test_t10_pkce_auth(self):
        verifier, challenge, state = PKCEAuthFlow.generate_pkce_pair()
        self.assertTrue(PKCEAuthFlow.verify_callback(state, state, verifier, challenge))
        with self.assertRaises(PermissionError):
            PKCEAuthFlow.verify_callback(state, "tampered_state", verifier, challenge)

if __name__ == "__main__":
    unittest.main()
