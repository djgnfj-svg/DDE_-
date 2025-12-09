from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QMessageBox, QLabel
)
from PySide6.QtCore import Signal
from database import DBManager


class CreatePage(QWidget):
    post_created = Signal()
    request_cancel = Signal()

    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("새 게시글 작성")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("게시글 제목을 입력하세요")
        form_layout.addRow("제목:", self.title_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("작성자 이름 (미입력시 '익명')")
        form_layout.addRow("작성자:", self.author_input)

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

    def on_save_clicked(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        author = self.author_input.text().strip()

        if not title:
            QMessageBox.warning(self, "입력 오류", "제목을 입력해주세요.")
            self.title_input.setFocus()
            return

        if not content:
            QMessageBox.warning(self, "입력 오류", "내용을 입력해주세요.")
            self.content_input.setFocus()
            return

        if not author:
            author = "익명"

        try:
            self.db_manager.create_post(title, content, author)
            self.clear_inputs()
            self.post_created.emit()
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"게시글 저장 중 오류 발생:\n{str(e)}")

    def on_cancel_clicked(self):
        if self.has_unsaved_content():
            reply = QMessageBox.question(
                self,
                "작성 취소",
                "작성 중인 내용이 있습니다. 취소하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.clear_inputs()
        self.request_cancel.emit()

    def has_unsaved_content(self):
        """작성 중인 내용이 있는지 확인"""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        author = self.author_input.text().strip()
        return bool(title or content or author)

    def clear_inputs(self):
        self.title_input.clear()
        self.content_input.clear()
        self.author_input.clear()
