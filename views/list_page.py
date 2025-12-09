from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Signal
from controllers import PostController
from models import Post


class ListPage(QWidget):
    request_create = Signal()
    request_view = Signal(int)     # 행 더블클릭 시 (post_id)

    def __init__(self, controller: PostController):
        super().__init__()
        self.controller = controller
        self.init_ui()
        self.controller.posts_loaded.connect(self.on_posts_loaded)
        self.refresh_posts()

    def init_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.btn_create = QPushButton("새 글 작성")
        self.btn_create.clicked.connect(self.on_create_clicked)
        top_layout.addWidget(self.btn_create)
        layout.addLayout(top_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "제목", "작성자", "작성일"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.table.doubleClicked.connect(self.on_row_double_clicked)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def refresh_posts(self):
        self.controller.load_posts()

    def on_posts_loaded(self, posts: list[Post]):
        self.table.setRowCount(len(posts))

        for row_idx, post in enumerate(posts):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(post.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(post.title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(post.author))
            created_at = post.created_at.strftime("%Y-%m-%d %H:%M:%S") if post.created_at else ""
            self.table.setItem(row_idx, 3, QTableWidgetItem(created_at))

    def on_create_clicked(self):
        self.request_create.emit()

    def on_row_double_clicked(self, index):
        row = index.row()
        post_id = int(self.table.item(row, 0).text())
        self.request_view.emit(post_id)
