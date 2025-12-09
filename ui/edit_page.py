from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QMessageBox, QLabel
)
from PySide6.QtCore import Signal
from database import DBManager


class EditPage(QWidget):
    post_updated = Signal()
    request_cancel = Signal()

    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_post_id = None
        self.init_ui()

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
        post = self.db_manager.get_post_by_id(post_id)

        if post:
            self.title_input.setText(post['title'])
            self.content_input.setPlainText(post['content'])
            self.label_author.setText(post['author'])
        else:
            QMessageBox.warning(self, "오류", "게시글을 찾을 수 없습니다.")
            self.request_cancel.emit()

    def on_save_clicked(self):
        if not self.current_post_id:
            return

        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "입력 오류", "제목을 입력해주세요.")
            self.title_input.setFocus()
            return

        if not content:
            QMessageBox.warning(self, "입력 오류", "내용을 입력해주세요.")
            self.content_input.setFocus()
            return

        try:
            success = self.db_manager.update_post(self.current_post_id, title, content)

            if success:
                QMessageBox.information(self, "저장 완료", "게시글이 수정되었습니다.")
                self.post_updated.emit()
            else:
                QMessageBox.warning(self, "저장 실패", "게시글 수정에 실패했습니다.")
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"게시글 수정 중 오류 발생:\n{str(e)}")

    def on_cancel_clicked(self):
        self.request_cancel.emit()
