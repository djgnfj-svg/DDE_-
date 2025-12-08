import sqlite3
import os
from typing import List, Optional


class DBManager:
    """SQLite 데이터베이스 관리 클래스"""

    def __init__(self, db_path: str = "board.db"):
        """데이터베이스 매니저 초기화"""
        self.db_path = db_path
        self.connection = None
        self._connect()
        self._create_table()

    def _connect(self):
        """데이터베이스 연결"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def _create_table(self):
        """posts 테이블 생성"""
        cursor = self.connection.cursor()

        # 테이블 생성 쿼리
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

        # updated_at 자동 갱신 트리거 생성
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
        """게시글 데이터 유효성 검사

        Raises:
            ValueError: title 또는 content가 비어있을 경우
        """
        title = title.strip()
        content = content.strip()

        if not title:
            raise ValueError("제목은 필수입니다.")
        if not content:
            raise ValueError("내용은 필수입니다.")

        return title, content

    def create_post(self, title: str, content: str, author: str) -> int:
        """새 게시글 생성

        Raises:
            ValueError: title 또는 content가 비어있을 경우
        """
        # 유효성 검사
        title, content = self._validate_post_data(title, content)

        author = author.strip() if author.strip() else "익명"

        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            (title, content, author)
        )
        self.connection.commit()

        return cursor.lastrowid  # 생성된 게시글 ID 반환

    def get_all_posts(self) -> List[sqlite3.Row]:
        """모든 게시글 조회 (최신순)"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, author, created_at, updated_at
            FROM posts
            ORDER BY created_at DESC
        """)

        return cursor.fetchall()

    def get_post_by_id(self, post_id: int) -> Optional[sqlite3.Row]:
        """특정 게시글 조회"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, content, author, created_at, updated_at
            FROM posts
            WHERE id = ?
        """, (post_id,))

        return cursor.fetchone()

    def update_post(self, post_id: int, title: str, content: str) -> bool:
        """게시글 수정

        Raises:
            ValueError: title 또는 content가 비어있을 경우
        """
        # 유효성 검사
        title, content = self._validate_post_data(title, content)

        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE posts
            SET title = ?, content = ?
            WHERE id = ?
        """, (title, content, post_id))

        self.connection.commit()

        # rowcount: 영향받은 행의 개수
        return cursor.rowcount > 0

    def delete_post(self, post_id: int) -> bool:
        """게시글 삭제"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.connection.commit()

        # rowcount: 영향받은 행의 개수
        return cursor.rowcount > 0

    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
