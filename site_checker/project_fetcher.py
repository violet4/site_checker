import datetime

from PySide6.QtCore import QTimer

from site_checker.alert_window import AlertWindow
from site_checker.gui import ProjectWindow
from site_checker.dat_session_handler import DATSession
from site_checker.project_page_parser import ParserPlugin, default_parser
from site_checker.project_parser import parse_project_data


class ProjectFetcher:
    def __init__(self, session:DATSession, minutes:int=5, debug:bool=False,
                 parser:ParserPlugin=default_parser):
        self.parser = parser
        self.session = session
        self.minutes = minutes
        self.debug = debug
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_projects)

    def fetch_projects(self):
        try:
            self._fetch_projects()
        except Exception as e:
            message = f"Failed to fetch projects: {type(e)}: {e}"
            print(message)
            AlertWindow.open(message)

    def _fetch_projects(self):
        print("Begin project fetch at", datetime.datetime.now())

        content = self.session.get_project_webpage(debug=self.debug)
        project_data = self.parser.parse(content)
        if project_data:
            projects = parse_project_data(project_data)
            ProjectWindow.open(projects)
        print("Project fetch finished successfully")

    def start(self, run_now:bool=True):
        if run_now:
            self.timer.singleShot(0, self.fetch_projects)
        self.timer.start(self.minutes * 60 * 1000)
