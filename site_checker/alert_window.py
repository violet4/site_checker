from typing import Optional

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AlertWindow(QWidget):
    _window: 'Optional[AlertWindow]' = None
    _message: str

    def __init__(self, message:str):
        super().__init__()
        self._message = message
        self.init_ui()

    @classmethod
    def open(cls, message:str):
        if cls._window is not None:
            cls._window.close()

        cls._window = cls(message)
        cls._window.show()
        return cls._window

    def init_ui(self):
        self.setWindowTitle('Alert')
        project_layout = QVBoxLayout()
        title_label = QLabel(self._message)
        project_layout.addWidget(title_label)
        self.setLayout(project_layout)
