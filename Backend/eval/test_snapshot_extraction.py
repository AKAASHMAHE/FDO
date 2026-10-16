from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from snapshot_extraction import (
    chunk_policy_text,
    ensure_extraction_schema,
    import_manual_snapshot,
)


class SnapshotExtractionTests(unittest.TestCase):
    def test_chunks_are_bounded_with_overlap(self) -> None:
        source = "Heading One\n" + ("Location information is collected. " * 500)
        chunks = chunk_policy_text(source)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 10_000 for chunk in chunks))
        self.assertTrue(
            any(
                chunks[index - 1][-1_000:] in chunks[index]
                for index in range(1, len(chunks))
            )
        )

    def test_schema_migration_is_idempotent(self) -> None:
        connection = sqlite3.connect(":memory:")
        try:
            connection.row_factory = sqlite3.Row
            connection.execute(
                """
                CREATE TABLE policy_snapshots (
                    snapshot_id INTEGER PRIMARY KEY,
                    policy_id TEXT,
                    final_url TEXT,
                    http_status INTEGER,
                    fetched_at TEXT,
                    cleaned_text_sha256 TEXT,
                    character_count INTEGER,
                    cleaned_text TEXT
                )
                """
            )
            ensure_extraction_schema(connection)
            ensure_extraction_schema(connection)
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(policy_snapshots)")
            }
            self.assertTrue({"scope", "source_note", "capture_status", "capture_method"} <= columns)
            tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            self.assertTrue({"extraction_runs", "extracted_evidence"} <= tables)
        finally:
            connection.close()

    def test_manual_import_requires_metadata_and_does_not_touch_raw_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            database = base / "test.sqlite"
            source = base / "manual_capture.txt"
            source.write_text("Collected location information.", encoding="utf-8")
            connection = sqlite3.connect(database)
            try:
                connection.execute(
                    "CREATE TABLE policy_documents (policy_id TEXT PRIMARY KEY, raw_text TEXT)"
                )
                connection.execute(
                    """
                    INSERT INTO policy_documents VALUES ('POL-1', 'unchanged source text')
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE policy_snapshots (
                        snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        policy_id TEXT NOT NULL,
                        final_url TEXT NOT NULL,
                        http_status INTEGER NOT NULL,
                        fetched_at TEXT NOT NULL,
                        cleaned_text_sha256 TEXT NOT NULL,
                        character_count INTEGER NOT NULL,
                        cleaned_text TEXT NOT NULL
                    )
                    """
                )
                connection.commit()
            finally:
                connection.close()

            snapshot_id = import_manual_snapshot(
                database,
                file_path=source,
                policy_id="POL-1",
                final_url="https://example.com/policy",
                http_status=200,
                fetched_at="2026-10-14T06:00:00Z",
                scope="Full policy",
                source_note="Operator-provided browser capture",
            )
            connection = sqlite3.connect(database)
            try:
                row = connection.execute(
                    """
                    SELECT capture_status, capture_method, scope, source_note,
                           cleaned_text
                    FROM policy_snapshots WHERE snapshot_id = ?
                    """,
                    (snapshot_id,),
                ).fetchone()
                self.assertEqual(row[0], "MANUALLY_CAPTURED")
                self.assertEqual(row[1], "MANUAL")
                self.assertEqual(row[2], "Full policy")
                self.assertEqual(row[3], "Operator-provided browser capture")
                self.assertEqual(row[4], "Collected location information.")
                raw_text = connection.execute(
                    "SELECT raw_text FROM policy_documents WHERE policy_id = 'POL-1'"
                ).fetchone()[0]
                self.assertEqual(raw_text, "unchanged source text")
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
