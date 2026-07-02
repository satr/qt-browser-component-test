import sys
from pathlib import Path

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWebView import QWebView, QWebViewLoadingInfo, QtWebView


def make_home_url() -> QUrl:
    return QUrl.fromLocalFile(str(Path(__file__).with_name("home.html")))


def normalize_url(raw_url: str, fallback: QUrl) -> QUrl:
    url = QUrl.fromUserInput(raw_url.strip())
    return url if url.isValid() and not url.isEmpty() else fallback


class BrowserWindow(QMainWindow):
    def __init__(self, start_url: QUrl, home_url: QUrl) -> None:
        super().__init__()
        self._home_url = home_url

        self.setWindowTitle("QWebView test app")
        self.resize(1200, 800)

        self.web_view = QWebView()
        self.web_view.urlChanged.connect(self._on_url_changed)
        self.web_view.titleChanged.connect(self._on_title_changed)
        self.web_view.loadProgressChanged.connect(self._on_load_progress_changed)
        self.web_view.loadingChanged.connect(self._on_loading_changed)

        self.back_action = QAction("Back", self)
        self.back_action.triggered.connect(self.web_view.goBack)

        self.forward_action = QAction("Forward", self)
        self.forward_action.triggered.connect(self.web_view.goForward)

        self.reload_action = QAction("Reload", self)
        self.reload_action.triggered.connect(self.web_view.reload)

        self.stop_action = QAction("Stop", self)
        self.stop_action.triggered.connect(self.web_view.stop)

        self.home_action = QAction("Home", self)
        self.home_action.triggered.connect(self._go_home)

        toolbar = QToolBar("Navigation", self)
        toolbar.setMovable(False)
        toolbar.addAction(self.back_action)
        toolbar.addAction(self.forward_action)
        toolbar.addAction(self.reload_action)
        toolbar.addAction(self.stop_action)
        toolbar.addAction(self.home_action)

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter a URL and press Enter")
        self.address_bar.returnPressed.connect(self._navigate_from_bar)
        self.address_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        toolbar.addWidget(self.address_bar)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self._navigate_from_bar)
        toolbar.addWidget(self.go_button)

        self.addToolBar(toolbar)

        wrapper = QWidget(self)
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        web_container = QWidget.createWindowContainer(self.web_view, wrapper)
        web_container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout.addWidget(web_container)

        status_row = QWidget(wrapper)
        status_layout = QHBoxLayout(status_row)
        status_layout.setContentsMargins(8, 4, 8, 4)
        status_layout.setSpacing(8)
        self.status_label = QLabel("Ready", status_row)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch(1)
        layout.addWidget(status_row)

        self.setCentralWidget(wrapper)
        self.web_view.setUrl(start_url)

    def _update_actions(self) -> None:
        self.back_action.setEnabled(self.web_view.canGoBack())
        self.forward_action.setEnabled(self.web_view.canGoForward())

    def _go_home(self) -> None:
        self.web_view.setUrl(self._home_url)

    def _navigate_from_bar(self) -> None:
        self.web_view.setUrl(normalize_url(self.address_bar.text(), self._home_url))

    def _on_url_changed(self, url: QUrl) -> None:
        self.address_bar.setText(url.toString())
        self._update_actions()

    def _on_title_changed(self, title: str) -> None:
        self.setWindowTitle(title or "QWebView test app")

    def _on_load_progress_changed(self, progress: int) -> None:
        self.status_label.setText(f"Loading... {progress}%")

    def _on_loading_changed(self, info: QWebViewLoadingInfo) -> None:
        status = info.status()
        if status == QWebViewLoadingInfo.LoadStatus.Started:
            self.status_label.setText("Loading...")
        elif status == QWebViewLoadingInfo.LoadStatus.Succeeded:
            self.status_label.setText("Loaded")
        elif status == QWebViewLoadingInfo.LoadStatus.Failed:
            self.status_label.setText(f"Load failed: {info.errorString()}")
        else:
            self.status_label.setText("Ready")
        self._update_actions()


def main() -> int:
    QtWebView.initialize()
    app = QApplication(sys.argv)

    home_url = make_home_url()
    start_url = home_url
    for argument in sys.argv[1:]:
        if not argument.startswith("-"):
            start_url = normalize_url(argument, home_url)
            break

    window = BrowserWindow(start_url, home_url)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
