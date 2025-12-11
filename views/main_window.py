from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from models import PostRepository
from controllers import PostController
from views.list_page import ListPage
from views.create_page import CreatePage
from views.view_page import ViewPage
from views.edit_page import EditPage


class MainWindow(QWidget):
    PAGE_LIST = 0
    PAGE_CREATE = 1
    PAGE_VIEW = 2
    PAGE_EDIT = 3

    def __init__(self):
        super().__init__()
        self.repository = PostRepository()
        self.controller = PostController(self.repository)
        self.init_ui()
        self.connect_signals()
        self.connect_controller_signals()

    def init_ui(self):
        self.setWindowTitle("DDE 게시판")
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.stacked_widget = QStackedWidget()

        self.list_page = ListPage(self.controller)
        self.create_page = CreatePage(self.controller)
        self.view_page = ViewPage(self.controller)
        self.edit_page = EditPage(self.controller)

        self.stacked_widget.addWidget(self.list_page)     # 0
        self.stacked_widget.addWidget(self.create_page)   # 1
        self.stacked_widget.addWidget(self.view_page)     # 2
        self.stacked_widget.addWidget(self.edit_page)     # 3

        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.stacked_widget.setCurrentIndex(self.PAGE_LIST)

    def connect_signals(self):
        self.list_page.request_create.connect(self.switch_to_create)
        self.list_page.request_view.connect(self.switch_to_view)

        self.create_page.request_cancel.connect(self.switch_to_list)

        self.view_page.request_edit.connect(self.switch_to_edit)
        self.view_page.request_list.connect(self.switch_to_list)

        self.edit_page.request_cancel.connect(self.on_edit_cancelled)

    def connect_controller_signals(self):
        self.controller.post_created.connect(self.on_post_created)
        self.controller.post_updated.connect(self.on_post_updated)
        self.controller.post_deleted.connect(self.on_post_deleted)
        self.controller.error_occurred.connect(self.show_error)

    def show_error(self, message: str):
        QMessageBox.critical(self, "오류", message)

    def switch_to_list(self):
        self.list_page.refresh_posts()
        self.stacked_widget.setCurrentIndex(self.PAGE_LIST)

    def switch_to_create(self):
        self.create_page.clear_inputs()
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
        current_page = self.stacked_widget.currentIndex()

        # 작성 페이지에서 작성 중인 내용이 있는지 확인
        if current_page == self.PAGE_CREATE and self.create_page.has_unsaved_content():
            reply = QMessageBox.question(
                self,
                "프로그램 종료",
                "작성 중인 내용이 있습니다. 종료하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        # 수정 페이지에서 수정 중인 내용이 있는지 확인
        if current_page == self.PAGE_EDIT and self.edit_page.has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "프로그램 종료",
                "수정 중인 내용이 있습니다. 종료하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        self.repository.close()
        event.accept()
