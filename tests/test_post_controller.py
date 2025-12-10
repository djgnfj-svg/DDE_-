import pytest
import os
from PySide6.QtWidgets import QApplication
from models import Post, PostRepository
from controllers import PostController


# PySide6 테스트를 위한 QApplication 인스턴스
@pytest.fixture(scope="session")
def app():
    """테스트용 QApplication 생성"""
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    yield application


class SignalSpy:
    """Signal 발생을 추적하는 헬퍼 클래스"""

    def __init__(self):
        self.called = False
        self.call_count = 0
        self.last_args = None

    def slot(self, *args):
        self.called = True
        self.call_count += 1
        self.last_args = args if args else None

    def reset(self):
        self.called = False
        self.call_count = 0
        self.last_args = None


class TestPostController:

    @pytest.fixture(autouse=True)
    def setup(self, app, tmp_path):
        """임시 DB와 Controller 생성"""
        self.db_path = str(tmp_path / "test.db")
        self.repository = PostRepository(self.db_path)
        self.controller = PostController(self.repository)

        # Signal Spy 설정
        self.posts_loaded_spy = SignalSpy()
        self.post_loaded_spy = SignalSpy()
        self.post_created_spy = SignalSpy()
        self.post_updated_spy = SignalSpy()
        self.post_deleted_spy = SignalSpy()
        self.error_spy = SignalSpy()

        self.controller.posts_loaded.connect(self.posts_loaded_spy.slot)
        self.controller.post_loaded.connect(self.post_loaded_spy.slot)
        self.controller.post_created.connect(self.post_created_spy.slot)
        self.controller.post_updated.connect(self.post_updated_spy.slot)
        self.controller.post_deleted.connect(self.post_deleted_spy.slot)
        self.controller.error_occurred.connect(self.error_spy.slot)

        yield
        self.repository.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    # === CREATE 테스트 ===

    def test_create_post_success_emits_signal(self):
        """게시글 생성 성공 시 post_created Signal 발생"""
        self.controller.create_post("제목", "내용", "작성자")

        assert self.post_created_spy.called is True
        assert self.error_spy.called is False

    def test_create_post_empty_title_emits_error(self):
        """빈 제목으로 생성 시 error_occurred Signal 발생"""
        self.controller.create_post("", "내용", "작성자")

        assert self.post_created_spy.called is False
        assert self.error_spy.called is True

    def test_create_post_empty_content_emits_error(self):
        """빈 내용으로 생성 시 error_occurred Signal 발생"""
        self.controller.create_post("제목", "", "작성자")

        assert self.post_created_spy.called is False
        assert self.error_spy.called is True

    def test_create_post_whitespace_title_emits_error(self):
        """공백만 있는 제목으로 생성 시 error_occurred Signal 발생"""
        self.controller.create_post("   ", "내용", "작성자")

        assert self.post_created_spy.called is False
        assert self.error_spy.called is True

    # === READ 테스트(Load) ===

    def test_load_posts_emits_signal_with_data(self):
        """게시글 목록 로드 시 posts_loaded Signal에 데이터 포함"""
        self.repository.create(Post(title="제목1", content="내용1", author="작성자"))
        self.repository.create(Post(title="제목2", content="내용2", author="작성자"))

        self.controller.load_posts()

        assert self.posts_loaded_spy.called is True
        posts = self.posts_loaded_spy.last_args[0]
        assert len(posts) == 2

    def test_load_posts_empty_list(self):
        """게시글이 없을 때 빈 리스트로 Signal 발생"""
        self.controller.load_posts()

        assert self.posts_loaded_spy.called is True
        posts = self.posts_loaded_spy.last_args[0]
        assert posts == []

    def test_load_post_success(self):
        """단일 게시글 로드 성공"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        self.controller.load_post(post_id)

        assert self.post_loaded_spy.called is True
        post = self.post_loaded_spy.last_args[0]
        assert post.title == "제목"

    def test_load_post_not_found_emits_error(self):
        """존재하지 않는 게시글 로드 시 error_occurred Signal 발생"""
        self.controller.load_post(9999)

        assert self.post_loaded_spy.called is False
        assert self.error_spy.called is True

    # === UPDATE 테스트 ===

    def test_update_post_success_emits_signal(self):
        """게시글 수정 성공 시 post_updated Signal 발생"""
        post_id = self.repository.create(
            Post(title="원래 제목", content="원래 내용", author="작성자")
        )

        self.controller.update_post(post_id, "수정된 제목", "수정된 내용")

        assert self.post_updated_spy.called is True
        assert self.error_spy.called is False

    def test_update_post_empty_title_emits_error(self):
        """빈 제목으로 수정 시 error_occurred Signal 발생"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        self.controller.update_post(post_id, "", "수정된 내용")

        assert self.post_updated_spy.called is False
        assert self.error_spy.called is True

    def test_update_post_empty_content_emits_error(self):
        """빈 내용으로 수정 시 error_occurred Signal 발생"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        self.controller.update_post(post_id, "수정된 제목", "")

        assert self.post_updated_spy.called is False
        assert self.error_spy.called is True

    def test_update_post_not_exists_emits_error(self):
        """존재하지 않는 게시글 수정 시 error_occurred Signal 발생"""
        self.controller.update_post(9999, "제목", "내용")

        assert self.post_updated_spy.called is False
        assert self.error_spy.called is True

    # === DELETE 테스트 ===

    def test_delete_post_success_emits_signal(self):
        """게시글 삭제 성공 시 post_deleted Signal 발생"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        self.controller.delete_post(post_id)

        assert self.post_deleted_spy.called is True
        assert self.error_spy.called is False

    def test_delete_post_not_exists_emits_error(self):
        """존재하지 않는 게시글 삭제 시 error_occurred Signal 발생"""
        self.controller.delete_post(9999)

        assert self.post_deleted_spy.called is False
        assert self.error_spy.called is True
