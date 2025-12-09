from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel
from PySide6.QtCore import Qt
from database import DBManager


class MainWindow(QWidget):
    """메인 윈도우 클래스"""

    def __init__(self):
        """메인 윈도우 초기화"""
        super().__init__()

        # DB & UI 초기화
        self.db_manager = DBManager()
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        # 윈도우 설정
        self.setWindowTitle("DDE 게시판 애플리케이션")
        self.resize(800, 600)

        # 레이아웃 생성
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()

        # 임시 페이지 (테스트용)
        temp_widget = QWidget()
        temp_layout = QVBoxLayout()

        welcome_label = QLabel("DDE 게시판")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        temp_layout.addStretch()
        temp_layout.addWidget(welcome_label)
        temp_layout.addStretch()

        temp_widget.setLayout(temp_layout)
        self.stacked_widget.addWidget(temp_widget)

        # 레이아웃에 추가
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def closeEvent(self, event):
        """윈도우 종료 시 DB 연결 종료"""
        self.db_manager.close()
        event.accept()
