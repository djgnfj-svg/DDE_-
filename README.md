# DDE 게시판 애플리케이션
PySide6 기반의 데스크톱 게시판 프로그램

## 사용 기술

| 구분 | 기술 |
|------|------|
| 언어 | Python 3.9+ |
| GUI | PySide6 |
| 데이터베이스 | SQLite |
| 테스트 | pytest |

## 실행 방법

### 1. 가상환경 생성
```bash
python -m venv venv
```

### 2. 의존성 설치
```bash
# Windows
venv\Scripts\pip.exe install -r requirements.txt

# Linux/macOS
venv/bin/pip install -r requirements.txt

# WSL
venv/Scripts/pip.exe install -r requirements.txt
```

### 3. 실행
```bash
# Windows
venv\Scripts\python.exe main.py

# Linux/macOS
venv/bin/python main.py

# WSL (Windows venv 사용 시)
venv/Scripts/python.exe main.py
```

### 4. 테스트 실행
```bash
# Windows
venv\Scripts\python.exe -m pytest tests/ -v

# Linux/macOS
venv/bin/python -m pytest tests/ -v

# WSL (Windows venv 사용 시)
venv/Scripts/python.exe -m pytest tests/ -v
```

## 프로젝트 구조

MVC 구조로 작성했습니다. <br>
- Models | 데이터 구조, DB 접근
- View |  UI 표시, 사용자 입력
- Controller | 유효성 검사, 비즈니스 로직

```
DDE/
├── main.py
├── board.db
├── requirements.txt
│
├── models/
│   ├── post.py              # Post data class
│   └── post_repository.py   # DB CRUD (DBManager)
│
├── controllers/
│   └── post_controller.py
│
├── views/
│   ├── main_window.py 
│   ├── list_page.py
│   ├── create_page.py
│   ├── view_page.py
│   └── edit_page.py
│
└── tests/
    ├── test_post_repository.py
    └── test_post_controller.py
```

 ## 추가 구현

  - 작성/수정 중 이탈 시 확인 대화상자