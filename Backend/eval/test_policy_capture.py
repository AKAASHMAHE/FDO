from __future__ import annotations

import sqlite3
import unittest

from capture_benchmark_policies import (
    PageSnapshot,
    classify_snapshot,
    ensure_snapshot_table,
    is_usable_http_url,
    save_snapshot,
)


class PolicyCaptureTests(unittest.TestCase):
    def test_only_usable_http_urls_are_accepted(self) -> None:
        self.assertTrue(is_usable_http_url("https://example.com/privacy"))
        self.assertTrue(is_usable_http_url("http://example.com/privacy"))
        self.assertFalse(is_usable_http_url(None))
        self.assertFalse(is_usable_http_url("Google privacy policy"))
        self.assertFalse(is_usable_http_url("https://"))
        self.assertFalse(is_usable_http_url("https://example.com/has space"))

    def test_short_and_gated_pages_need_manual_capture(self) -> None:
        short = PageSnapshot("https://example.com", 200, "now", "Privacy policy")
        self.assertEqual(classify_snapshot(short)[0], "NEEDS_MANUAL_CAPTURE")

        gated = PageSnapshot(
            "https://example.com",
            200,
            "now",
            "Please enable JavaScript to continue.",
        )
        self.assertEqual(classify_snapshot(gated)[0], "NEEDS_MANUAL_CAPTURE")

        policy_text = "Privacy policy. " + ("Detailed policy text. " * 150)
        policy_text += "These technical cookies must be enabled to use our services."
        policy = PageSnapshot("https://example.com", 200, "now", policy_text)
        self.assertEqual(classify_snapshot(policy)[0], "CAPTURED")

    def test_http_errors_are_failed(self) -> None:
        snapshot = PageSnapshot("https://example.com", 503, "now", "Unavailable")
        self.assertEqual(classify_snapshot(snapshot), ("FAILED", "HTTP 503"))

    def test_snapshot_table_persists_required_fields(self) -> None:
        connection = sqlite3.connect(":memory:")
        try:
            connection.execute(
                "CREATE TABLE policy_documents (policy_id TEXT PRIMARY KEY)"
            )
            connection.execute(
                "INSERT INTO policy_documents (policy_id) VALUES ('POL-1')"
            )
            ensure_snapshot_table(connection)
            snapshot = PageSnapshot(
                "https://example.com/privacy",
                200,
                "2026-10-14T00:00:00+00:00",
                "clean policy text",
            )
            save_snapshot(connection, "POL-1", snapshot)
            saved = connection.execute(
                """
                SELECT policy_id, final_url, http_status, fetched_at,
                       cleaned_text_sha256, character_count, cleaned_text
                FROM policy_snapshots
                """
            ).fetchone()
            self.assertEqual(saved[0], "POL-1")
            self.assertEqual(saved[1], snapshot.final_url)
            self.assertEqual(saved[2], 200)
            self.assertEqual(saved[3], snapshot.fetched_at)
            self.assertEqual(saved[4], snapshot.text_sha256)
            self.assertEqual(saved[5], len(snapshot.cleaned_text))
            self.assertEqual(saved[6], snapshot.cleaned_text)
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
