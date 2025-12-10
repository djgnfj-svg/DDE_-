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

```
DDE/
├── main.py
├── board.db                 # SQLite DB
├── requirements.txt
│
├── models/                  # Model 계층
│   ├── post.py              # Post 데이터 클래스
│   └── post_repository.py   # DB CRUD 처리
│
├── controllers/             # Controller 계층
│   └── post_controller.py   # 비즈니스 로직, 유효성 검사
│
├── views/                   # View 계층
│   ├── main_window.py       # 메인 윈도우, 페이지 전환
│   ├── list_page.py         # 게시글 목록
│   ├── create_page.py       # 게시글 작성
│   ├── view_page.py         # 게시글 조회
│   └── edit_page.py         # 게시글 수정
│
└── tests/                   # 테스트 코드
    ├── test_post_repository.py  # Repository 테스트
    └── test_post_controller.py  # Controller 테스트
```

## MVC 아키텍처

```
View (views/)
  │
  │ Signal/메서드 호출
  ▼
Controller (controllers/)
  │
  │ 메서드 호출
  ▼
Model (models/)
  │
  ▼
SQLite Database
```

- **View**: UI 표시, 사용자 입력 전달
- **Controller**: 유효성 검사, 비즈니스 로직
- **Model**: 데이터 구조, DB 접근

