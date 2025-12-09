from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Signal
from database import DBManager


class ViewPage(QWidget):
    request_edit = Signal(int)
    post_deleted = Signal()
    request_list = Signal()

    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_post_id = None
        self.init_ui()

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
        post = self.db_manager.get_post_by_id(post_id)

        if post:
            self.label_title.setText(post['title'])
            self.label_author.setText(post['author'])
            self.label_created.setText(post['created_at'])
            self.label_updated.setText(post['updated_at'])
            self.text_content.setPlainText(post['content'])
        else:
            QMessageBox.warning(self, "오류", "게시글을 찾을 수 없습니다.")
            self.request_list.emit()

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
            success = self.db_manager.delete_post(self.current_post_id)

            if success:
                QMessageBox.information(self, "삭제 완료", "게시글이 삭제되었습니다.")
                self.current_post_id = None
                self.post_deleted.emit()
            else:
                QMessageBox.warning(self, "삭제 실패", "게시글 삭제에 실패했습니다.")

    def on_list_clicked(self):
        self.request_list.emit()
