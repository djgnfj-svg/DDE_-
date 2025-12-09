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
