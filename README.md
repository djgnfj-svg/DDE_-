# DDE 게시판 애플리케이션

## 실행 방법

### Windows (PowerShell/CMD)
```bash
venv\Scripts\python.exe main.py
```

### Linux/macOS/WSL
```bash
venv/Scripts/python.exe main.py
```

## MVC 테스트
그대로 복붙해서 사용하자
### Model 계층 테스트
```bash
venv/Scripts/python.exe -c "
from models import Post, PostRepository

repo = PostRepository('test_mvc.db')

# Create
post_id = repo.create(Post(title='테스트', content='내용', author='작성자'))
print(f'생성된 ID: {post_id}')

# Read
posts = repo.get_all()
print(f'전체 목록: {len(posts)}개')

post = repo.get_by_id(post_id)
print(f'조회: {post}')

# Update
repo.update(Post(id=post_id, title='수정됨', content='수정내용'))
print(f'수정 후: {repo.get_by_id(post_id)}')

# Delete
repo.delete(post_id)
print(f'삭제 후: {repo.get_by_id(post_id)}')

repo.close()
import os; os.remove('test_mvc.db')
"
```

### Controller 계층 테스트
```bash
venv/Scripts/python.exe -c "
from PySide6.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)

from models import PostRepository
from controllers import PostController

repo = PostRepository('test_ctrl.db')
controller = PostController(repo)

# Signal 연결
controller.post_created.connect(lambda: print('post_created'))
controller.posts_loaded.connect(lambda posts: print(f'posts_loaded: {len(posts)}개'))
controller.post_loaded.connect(lambda post: print(f'post_loaded: {post.title}'))
controller.post_updated.connect(lambda: print('post_updated'))
controller.post_deleted.connect(lambda: print('post_deleted'))
controller.error_occurred.connect(lambda msg: print(f'error: {msg}'))

# 테스트
controller.create_post('테스트', '내용', '작성자')
controller.load_posts()
controller.load_post(1)
controller.update_post(1, '수정됨', '수정내용')
controller.delete_post(1)

repo.close()
import os; os.remove('test_ctrl.db')
"
```
