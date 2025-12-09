import sqlite3
import os
from datetime import datetime
from typing import Optional

from .post import Post


class PostRepository:
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
                created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                updated_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
            )
        """)

        # updated_at 자동 갱신 트리거
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_posts_timestamp
            AFTER UPDATE ON posts
            FOR EACH ROW
            BEGIN
                UPDATE posts SET updated_at = datetime('now', 'localtime') WHERE id = NEW.id;
            END
        """)
        self.connection.commit()

    def _row_to_post(self, row: sqlite3.Row) -> Post:
        return Post(
            id=row["id"],
            title=row["title"],
            content=row["content"] if "content" in row.keys() else "",
            author=row["author"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
        )

    def _validate_post_data(self, title: str, content: str) -> tuple[str, str]:
        title = title.strip()
        content = content.strip()
        if not title:
            raise ValueError("제목은 필수입니다.")
        if not content:
            raise ValueError("내용은 필수입니다.")
        return title, content

    def create(self, post: Post) -> int:
        title, content = self._validate_post_data(post.title, post.content)
        author = post.author.strip() if post.author.strip() else "익명"

        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            (title, content, author)
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_all(self) -> list[Post]:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, author, created_at, updated_at
            FROM posts
            ORDER BY created_at DESC
        """)
        return [self._row_to_post(row) for row in cursor.fetchall()]

    def get_by_id(self, post_id: int) -> Optional[Post]:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, content, author, created_at, updated_at
            FROM posts
            WHERE id = ?
        """, (post_id,))
        row = cursor.fetchone()
        return self._row_to_post(row) if row else None

    def update(self, post: Post) -> bool:
        title, content = self._validate_post_data(post.title, post.content)

        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE posts
            SET title = ?, content = ?
            WHERE id = ?
        """, (title, content, post.id))
        self.connection.commit()
        return cursor.rowcount > 0 # 실제로 수정된 행이 있으면 True

    def delete(self, post_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.connection.commit()
        return cursor.rowcount > 0 # 실제로 삭제된 행이 있으면 True

    def close(self):
        if self.connection:
            self.connection.close()
