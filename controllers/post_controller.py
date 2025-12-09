from PySide6.QtCore import QObject, Signal

from models import Post, PostRepository


class PostController(QObject):
    posts_loaded = Signal(list)
    post_loaded = Signal(object)
    post_created = Signal()
    post_updated = Signal()
    post_deleted = Signal()
    error_occurred = Signal(str)

    def __init__(self, repository: PostRepository):
        super().__init__()
        self.repository = repository

    def _validate_post_data(self, title: str, content: str) -> bool:
        """데이터 유효성 검사"""
        if not title or not title.strip():
            self.error_occurred.emit("제목을 입력해주세요.")
            return False
        if not content or not content.strip():
            self.error_occurred.emit("내용을 입력해주세요.")
            return False
        return True

    def load_posts(self):
        try:
            posts = self.repository.get_all()
            self.posts_loaded.emit(posts)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def load_post(self, post_id: int):
        try:
            post = self.repository.get_by_id(post_id)
            if post:
                self.post_loaded.emit(post)
            else:
                self.error_occurred.emit("게시글을 찾을 수 없습니다.")
        except Exception as e:
            self.error_occurred.emit(str(e))

    def create_post(self, title: str, content: str, author: str):
        if not self._validate_post_data(title, content):
            return

        try:
            post = Post(title=title, content=content, author=author)
            self.repository.create(post)
            self.post_created.emit()
        except Exception as e:
            self.error_occurred.emit(f"저장 오류: {str(e)}")

    def update_post(self, post_id: int, title: str, content: str):
        if not self._validate_post_data(title, content):
            return

        try:
            post = Post(id=post_id, title=title, content=content)
            success = self.repository.update(post)
            if success:
                self.post_updated.emit()
            else:
                self.error_occurred.emit("수정 실패")
        except Exception as e:
            self.error_occurred.emit(f"수정 오류: {str(e)}")

    def delete_post(self, post_id: int):
        try:
            success = self.repository.delete(post_id)
            if success:
                self.post_deleted.emit()
            else:
                self.error_occurred.emit("삭제 실패")
        except Exception as e:
            self.error_occurred.emit(f"삭제 오류: {str(e)}")
