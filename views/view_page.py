from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Signal
from controllers import PostController
from models import Post


class ViewPage(QWidget):
    request_edit = Signal(int)
    request_list = Signal()

    def __init__(self, controller: PostController):
        super().__init__()
        self.controller = controller
        self.current_post_id = None
        self.init_ui()
        self.controller.post_loaded.connect(self.on_post_loaded)

    def init_ui(self):
        layout = QVBoxLayout()

        page_title = QLabel("게시글 조회")
        page_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(page_title)

        form_layout = QFormLayout()

        self.label_title = QLabel()
        self.label_title.setWordWrap(True)
        self.label_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        form_layout.addRow("제목:", self.label_title)

        self.label_author = QLabel()
        form_layout.addRow("작성자:", self.label_author)

        self.label_created = QLabel()
        form_layout.addRow("작성일:", self.label_created)

        self.label_updated = QLabel()
        form_layout.addRow("수정일:", self.label_updated)

        layout.addLayout(form_layout)

        content_label = QLabel("내용:")
        layout.addWidget(content_label)

        self.text_content = QTextEdit()
        self.text_content.setReadOnly(True)
        layout.addWidget(self.text_content)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_edit = QPushButton("수정")
        self.btn_edit.clicked.connect(self.on_edit_clicked)
        button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("삭제")
        self.btn_delete.clicked.connect(self.on_delete_clicked)
        button_layout.addWidget(self.btn_delete)

        self.btn_list = QPushButton("목록")
        self.btn_list.clicked.connect(self.on_list_clicked)
        button_layout.addWidget(self.btn_list)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_post(self, post_id: int):
        self.current_post_id = post_id
        self.controller.load_post(post_id)

    def on_post_loaded(self, post: Post):
        """Controller의 post_loaded Signal을 받아 UI 갱신"""
        self.label_title.setText(post.title)
        self.label_author.setText(post.author)
        created_at = post.created_at.strftime("%Y-%m-%d %H:%M:%S") if post.created_at else ""
        updated_at = post.updated_at.strftime("%Y-%m-%d %H:%M:%S") if post.updated_at else ""
        self.label_created.setText(created_at)
        self.label_updated.setText(updated_at)
        self.text_content.setPlainText(post.content)

    def on_edit_clicked(self):
        if self.current_post_id:
            self.request_edit.emit(self.current_post_id)

    def on_delete_clicked(self):
        if not self.current_post_id:
            return

        reply = QMessageBox.question(
            self,
            "삭제 확인",
            "정말 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_post(self.current_post_id)
            self.current_post_id = None

    def on_list_clicked(self):
        self.request_list.emit()
