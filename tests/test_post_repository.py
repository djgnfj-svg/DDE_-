import pytest
import os
from models import Post, PostRepository


class TestPostRepository:

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """임시 DB 생성"""
        self.db_path = str(tmp_path / "test.db")
        self.repository = PostRepository(self.db_path)
        yield
        self.repository.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    # === CREATE 테스트 ===

    def test_create_post_success(self):
        """정상적인 게시글 생성"""
        post = Post(title="테스트 제목", content="테스트 내용", author="작성자")
        post_id = self.repository.create(post)

        assert post_id is not None
        assert post_id > 0

    def test_create_post_empty_author_becomes_anonymous(self):
        """작성자가 비어있으면 '익명'으로 저장"""
        post = Post(title="제목", content="내용", author="")
        post_id = self.repository.create(post)

        saved_post = self.repository.get_by_id(post_id)
        assert saved_post.author == "익명"

    def test_create_post_empty_title_raises_error(self):
        """빈 제목으로 생성 시 ValueError 발생"""
        post = Post(title="", content="내용", author="작성자")

        with pytest.raises(ValueError, match="제목은 필수입니다"):
            self.repository.create(post)

    def test_create_post_empty_content_raises_error(self):
        """빈 내용으로 생성 시 ValueError 발생"""
        post = Post(title="제목", content="", author="작성자")

        with pytest.raises(ValueError, match="내용은 필수입니다"):
            self.repository.create(post)

    def test_create_post_whitespace_only_title_raises_error(self):
        """공백만 있는 제목으로 생성 시 ValueError 발생"""
        post = Post(title="   ", content="내용", author="작성자")

        with pytest.raises(ValueError, match="제목은 필수입니다"):
            self.repository.create(post)

    # === READ 테스트 ===

    def test_get_all_empty(self):
        """게시글이 없을 때 빈 리스트 반환"""
        posts = self.repository.get_all()
        assert posts == []

    def test_get_all_returns_posts(self):
        """게시글 목록 조회"""
        self.repository.create(Post(title="제목1", content="내용1", author="작성자1"))
        self.repository.create(Post(title="제목2", content="내용2", author="작성자2"))

        posts = self.repository.get_all()

        assert len(posts) == 2

    def test_get_all_ordered_by_created_at_desc(self):
        """최신 글이 먼저 오도록 정렬 (ID 역순으로 확인)"""
        id1 = self.repository.create(Post(title="첫번째", content="내용", author="작성자"))
        id2 = self.repository.create(Post(title="두번째", content="내용", author="작성자"))

        posts = self.repository.get_all()

        # 나중에 생성된 글(id2)이 먼저 나와야 함
        assert posts[0].id == id2
        assert posts[1].id == id1

    def test_get_by_id_exists(self):
        """존재하는 게시글 조회"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        post = self.repository.get_by_id(post_id)

        assert post is not None
        assert post.title == "제목"
        assert post.content == "내용"
        assert post.author == "작성자"

    def test_get_by_id_not_exists(self):
        """존재하지 않는 게시글 조회 시 None 반환"""
        post = self.repository.get_by_id(9999)
        assert post is None

    # === UPDATE 테스트 ===

    def test_update_post_success(self):
        """게시글 수정 성공"""
        post_id = self.repository.create(
            Post(title="원래 제목", content="원래 내용", author="작성자")
        )

        updated_post = Post(id=post_id, title="수정된 제목", content="수정된 내용")
        result = self.repository.update(updated_post)

        assert result is True

        saved_post = self.repository.get_by_id(post_id)
        assert saved_post.title == "수정된 제목"
        assert saved_post.content == "수정된 내용"

    def test_update_post_not_exists(self):
        """존재하지 않는 게시글 수정 시 False 반환"""
        post = Post(id=9999, title="제목", content="내용")
        result = self.repository.update(post)
        assert result is False

    def test_update_post_empty_title_raises_error(self):
        """빈 제목으로 수정 시 ValueError 발생"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        with pytest.raises(ValueError, match="제목은 필수입니다"):
            self.repository.update(Post(id=post_id, title="", content="내용"))

    # === DELETE 테스트 ===

    def test_delete_post_success(self):
        """게시글 삭제 성공"""
        post_id = self.repository.create(
            Post(title="제목", content="내용", author="작성자")
        )

        result = self.repository.delete(post_id)

        assert result is True
        assert self.repository.get_by_id(post_id) is None

    def test_delete_post_not_exists(self):
        """존재하지 않는 게시글 삭제 시 False 반환"""
        result = self.repository.delete(9999)
        assert result is False
