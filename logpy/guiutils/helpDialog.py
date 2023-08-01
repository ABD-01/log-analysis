from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView


class HelpDialog(QDialog):
    def __init__(self, readme_content):
        super().__init__()

        self.initUI(readme_content)

    def initUI(self, readme_content):
        self.setWindowTitle("LogPy Help")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Create a QWebEngineView widget to display the README content
        web_view = QWebEngineView(self)
        web_view.setHtml(readme_content)
        layout.addWidget(web_view)

        self.setLayout(layout)