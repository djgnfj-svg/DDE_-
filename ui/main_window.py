from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Qt
from database import DBManager
from ui.list_page import ListPage


class MainWindow(QWidget):
    PAGE_HOME = 0
    PAGE_LIST = 1

    def __init__(self):
        super().__init__()
        self.db_manager = DBManager()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setWindowTitle("DDE 게시판 애플리케이션")
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.home_page = self.create_home_page()
        self.list_page = ListPage(self.db_manager)

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.list_page)

        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        self.stacked_widget.setCurrentIndex(self.PAGE_HOME)

    def create_home_page(self):
        home_widget = QWidget()
        home_layout = QVBoxLayout()

        welcome_label = QLabel("DDE 게시판 애플리케이션")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        btn_view_board = QPushButton("게시판 보기")
        btn_view_board.setFixedSize(150, 40)
        btn_view_board.clicked.connect(self.switch_to_list)

        home_layout.addStretch()
        home_layout.addWidget(welcome_label)
        home_layout.addSpacing(20)
        home_layout.addWidget(btn_view_board, alignment=Qt.AlignmentFlag.AlignCenter)
        home_layout.addStretch()

        home_widget.setLayout(home_layout)
        return home_widget

    def connect_signals(self):
        self.list_page.request_home.connect(self.switch_to_home)
        self.list_page.request_create.connect(self.on_create_requested)
        self.list_page.request_view.connect(self.on_view_requested)

    def switch_to_home(self):
        self.stacked_widget.setCurrentIndex(self.PAGE_HOME)

    def switch_to_list(self):
        self.list_page.refresh_posts()
        self.stacked_widget.setCurrentIndex(self.PAGE_LIST)

    def on_create_requested(self):
        print("Create page requested (not implemented yet)")

    def on_view_requested(self, post_id: int):
        print(f"View page requested for post_id={post_id} (not implemented yet)")

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()
