import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from tmdb_sentinel.domain.snapshot import Snapshot


class SQLiteSnapshotRepository:
    """SQLite Implementation of SnapshotRepository"""

    def __init__(self, database_path: str | Path) -> None:
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row

        self._create_table()

    def _create_table(self) -> None:
        create_sql: str = """
                        CREATE TABLE IF NOT EXISTS snapshots (
                            id INTEGER PRIMARY KEY,
                            person_id INTEGER NOT NULL,
                            biography TEXT NOT NULL,
                            observed_at TEXT NOT NULL
                        )
                        """
        self._connection.execute(create_sql)

        idx_sql = """
                    CREATE INDEX IF NOT EXISTS idx_snapshots_person_observed_at 
                    ON snapshots (person_id, observed_at DESC, id DESC)
                    """
        self._connection.execute(idx_sql)

        self._connection.commit()

    def save(self, snapshot: Snapshot) -> None:
        if (
            snapshot.observed_at.tzinfo is None
            or snapshot.observed_at.utcoffset is None
        ):
            raise ValueError("Snapshot timestamp must be timezone-aware")

        observed_at = snapshot.observed_at.astimezone(UTC).isoformat()

        insert_sql: str = """
                        INSERT INTO snapshots (person_id, biography, observed_at) 
                        VALUES (?, ?, ?)
                        """
        with self._connection:
            self._connection.execute(
                insert_sql,
                (
                    snapshot.person_id,
                    snapshot.biography,
                    observed_at,
                ),
            )

    def get_latest(self, person_id: int) -> Snapshot | None:
        fetch_sql = """
                    SELECT person_id, biography, observed_at 
                    FROM snapshots 
                    WHERE person_id = ?
                    ORDER BY observed_at DESC, id DESC
                    LIMIT 1
                    """

        with self._connection:
            row = self._connection.execute(
                fetch_sql,
                (person_id,),
            ).fetchone()

            if row is None:
                return None

            return Snapshot(
                person_id=row["person_id"],
                biography=row["biography"],
                observed_at=datetime.fromisoformat(row["observed_at"]),
            )

    def close(self) -> None:
        self._connection.close()
