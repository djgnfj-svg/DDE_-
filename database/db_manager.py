import sqlite3
import os
from typing import List, Optional


class DBManager:
    def __init__(self, db_path: str = "board.db"):
        self.db_path = db_path
        self.connection = None
        self._connect()
        self._create_table()

    def _connect(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_posts_timestamp
            AFTER UPDATE ON posts
            FOR EACH ROW
            BEGIN
                UPDATE posts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        self.connection.commit()

    def _validate_post_data(self, title: str, content: str) -> tuple[str, str]:
        """Raises ValueError if title or content is empty."""
        title = title.strip()
        content = content.strip()
        if not title:
            raise ValueError("제목은 필수입니다.")
        if not content:
            raise ValueError("내용은 필수입니다.")
        return title, content

    def create_post(self, title: str, content: str, author: str) -> int:
        """Raises ValueError if title or content is empty."""
        title, content = self._validate_post_data(title, content)
        author = author.strip() if author.strip() else "익명"

        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            (title, content, author)
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_all_posts(self) -> List[sqlite3.Row]:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, author, created_at, updated_at
            FROM posts
            ORDER BY created_at DESC
        """)
        return cursor.fetchall()

    def get_post_by_id(self, post_id: int) -> Optional[sqlite3.Row]:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, content, author, created_at, updated_at
            FROM posts
            WHERE id = ?
        """, (post_id,))
        return cursor.fetchone()

    def update_post(self, post_id: int, title: str, content: str) -> bool:
        """Raises ValueError if title or content is empty."""
        title, content = self._validate_post_data(title, content)

        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE posts
            SET title = ?, content = ?
            WHERE id = ?
        """, (title, content, post_id))
        self.connection.commit()
        return cursor.rowcount > 0  # 실제로 수정된 행이 있으면 True

    def delete_post(self, post_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.connection.commit()
        return cursor.rowcount > 0  # 실제로 삭제된 행이 있으면 True

    def close(self):
        if self.connection:
            self.connection.close()
