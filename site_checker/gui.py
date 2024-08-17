import sys
from typing import List

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import QElapsedTimer

from site_checker.project import Project


class ProjectWindow(QWidget):
    _window: 'ProjectWindow|None' = None
    projects: List[Project]

    def __init__(self, projects):
        super().__init__()
        self.projects = projects
        self.timer = QElapsedTimer()
        self.timer.start()
        self.init_ui()

    @classmethod
    def open(cls, projects: List[Project]) -> 'ProjectWindow':
        if cls._window is not None:
            cls._window.close()
        cls._window = ProjectWindow(projects)
        cls._window.show()
        return cls._window

    def init_ui(self):
        self.setWindowTitle('Projects')
        layout = QVBoxLayout()
        for project in self.projects:
            project_layout = QVBoxLayout()
            title_label = QLabel(f'{project.title} (${project.rate_per_hour}/hr, {project.available_tasks} tasks left)')
            project_layout.addWidget(title_label)
            btn_layout = QHBoxLayout()
            for label, func in [('Copy URL', self.copy_url), ('Open', self.open_project), ('Copy Title', self.copy_title)]:
                button = QPushButton(label)
                button.clicked.connect(lambda _, b=button, f=func, p=project: self.delayed_wrapper(b, f, p))
                btn_layout.addWidget(button)
            project_layout.addLayout(btn_layout)
            layout.addLayout(project_layout)
        dismiss_button = QPushButton('Dismiss')
        dismiss_button.clicked.connect(self.close)
        layout.addWidget(dismiss_button)
        self.setLayout(layout)

    def copy_url(self, url):
        QApplication.clipboard().setText(url)

    def open_project(self, url):
        print(f'Open project at {url}')

    def copy_title(self, title):
        QApplication.clipboard().setText(title)

    def delayed_wrapper(self, button, func, project:Project):
        if self.timer.elapsed() > 2000:
            if func is self.copy_url:
                func(project.url)
            elif func is self.open_project:
                func(project.url)
            elif func is self.copy_title:
                func(project.title)


if __name__ == "__main__":
    from decimal import Decimal
    import time

    app = QApplication(sys.argv)
    example_projects = [
        Project(uuid="123", title="Project 1", rate_per_hour=Decimal("20.00"), available_tasks=8),
        Project(uuid="456", title="Project 2", rate_per_hour=Decimal("30.00"), available_tasks=3),
    ]
    example_projects_2 = [
        Project(uuid="789", title="Project 3", rate_per_hour=Decimal("20.00"), available_tasks=15),
        Project(uuid="098", title="Project 4", rate_per_hour=Decimal("25.00"), available_tasks=5),
    ]
    window = ProjectWindow.open(example_projects)
    opened_again = False
    def open_window_again(event:QCloseEvent):
        global opened_again
        event.accept()
        window.hide()
        if opened_again:
            return
        opened_again = True
        time.sleep(1)
        window.open(example_projects_2)

    window.closeEvent = open_window_again
    sys.exit(app.exec())
