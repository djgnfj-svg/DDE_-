from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QMessageBox, QLabel
)
from PySide6.QtCore import Signal
from controllers import PostController
from models import Post


class EditPage(QWidget):
    request_cancel = Signal()

    def __init__(self, controller: PostController):
        super().__init__()
        self.controller = controller
        self.current_post_id = None
        self.original_title = ""
        self.original_content = ""
        self.init_ui()
        self.controller.post_loaded.connect(self.on_post_loaded)

    def init_ui(self):
        layout = QVBoxLayout()

        page_title = QLabel("게시글 수정")
        page_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(page_title)

        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("게시글 제목을 입력하세요")
        form_layout.addRow("제목:", self.title_input)

        self.label_author = QLabel()
        form_layout.addRow("작성자:", self.label_author)

        layout.addLayout(form_layout)

        content_label = QLabel("내용:")
        layout.addWidget(content_label)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("게시글 내용을 입력하세요")
        layout.addWidget(self.content_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_save = QPushButton("저장")
        self.btn_save.clicked.connect(self.on_save_clicked)
        button_layout.addWidget(self.btn_save)

        self.btn_cancel = QPushButton("취소")
        self.btn_cancel.clicked.connect(self.on_cancel_clicked)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_post(self, post_id: int):
        self.current_post_id = post_id
        self.controller.load_post(post_id)

    def on_post_loaded(self, post: Post):
        self.title_input.setText(post.title)
        self.content_input.setPlainText(post.content)
        self.label_author.setText(post.author)
        self.original_title = post.title
        self.original_content = post.content

    def on_save_clicked(self):
        if not self.current_post_id:
            return

        title = self.title_input.text()
        content = self.content_input.toPlainText()
        self.controller.update_post(self.current_post_id, title, content)

    def on_cancel_clicked(self):
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "수정 취소",
                "수정 중인 내용이 있습니다. 취소하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.request_cancel.emit()

    def has_unsaved_changes(self):
        """현재 입력값과 원본 비교"""
        current_title = self.title_input.text()
        current_content = self.content_input.toPlainText()
        return current_title != self.original_title or current_content != self.original_content
