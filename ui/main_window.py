from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Qt
from database import DBManager
from ui.list_page import ListPage
from ui.create_page import CreatePage
from ui.view_page import ViewPage
from ui.edit_page import EditPage


class MainWindow(QWidget):
    PAGE_HOME = 0
    PAGE_LIST = 1
    PAGE_CREATE = 2
    PAGE_VIEW = 3
    PAGE_EDIT = 4

    def __init__(self):
        super().__init__()
        self.db_manager = DBManager()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setWindowTitle("DDE 게시판 애플리케이션")
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.stacked_widget = QStackedWidget()

        self.home_page = self._create_home_page()
        self.list_page = ListPage(self.db_manager)
        self.create_page = CreatePage(self.db_manager)
        self.view_page = ViewPage(self.db_manager)
        self.edit_page = EditPage(self.db_manager)

        self.stacked_widget.addWidget(self.home_page)     # 0
        self.stacked_widget.addWidget(self.list_page)     # 1
        self.stacked_widget.addWidget(self.create_page)   # 2
        self.stacked_widget.addWidget(self.view_page)     # 3
        self.stacked_widget.addWidget(self.edit_page)     # 4

        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.stacked_widget.setCurrentIndex(self.PAGE_HOME)

    def _create_home_page(self):
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
        self.list_page.request_create.connect(self.switch_to_create)
        self.list_page.request_view.connect(self.switch_to_view)

        self.create_page.post_created.connect(self.on_post_created)
        self.create_page.request_cancel.connect(self.switch_to_list)

        self.view_page.request_edit.connect(self.switch_to_edit)
        self.view_page.post_deleted.connect(self.on_post_deleted)
        self.view_page.request_list.connect(self.switch_to_list)

        self.edit_page.post_updated.connect(self.on_post_updated)
        self.edit_page.request_cancel.connect(self.on_edit_cancelled)

    def switch_to_home(self):
        self.stacked_widget.setCurrentIndex(self.PAGE_HOME)

    def switch_to_list(self):
        self.list_page.refresh_posts()
        self.stacked_widget.setCurrentIndex(self.PAGE_LIST)

    def switch_to_create(self):
        self.stacked_widget.setCurrentIndex(self.PAGE_CREATE)

    def switch_to_view(self, post_id: int):
        self.view_page.load_post(post_id)
        self.stacked_widget.setCurrentIndex(self.PAGE_VIEW)

    def switch_to_edit(self, post_id: int):
        self.edit_page.load_post(post_id)
        self.stacked_widget.setCurrentIndex(self.PAGE_EDIT)

    def on_post_created(self):
        self.switch_to_list()

    def on_post_updated(self):
        if self.edit_page.current_post_id:
            self.switch_to_view(self.edit_page.current_post_id)
        else:
            self.switch_to_list()

    def on_post_deleted(self):
        self.switch_to_list()

    def on_edit_cancelled(self):
        if self.edit_page.current_post_id:
            self.switch_to_view(self.edit_page.current_post_id)
        else:
            self.switch_to_list()

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()
