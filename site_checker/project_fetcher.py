import datetime
from typing import Optional

from PySide6.QtCore import QTimer
import requests

from site_checker.alert_window import AlertWindow
from site_checker.gui import ProjectWindow
from site_checker.dat_session_handler import DATSession
from site_checker.project_page_parser import ParserPlugin, default_parser
from site_checker.project_parser import parse_project_data


def send_message(message):
    url = 'http://127.0.0.1:31471/send'
    headers = {'Content-Type': 'application/json'}
    data = {'message': message}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


class ProjectFetcher:
    def __init__(self, session:DATSession, minutes:int=5,
                 debug:bool=False,
                 min_value:int=0,
                 parser:ParserPlugin=default_parser):
        self.parser = parser
        self.session = session
        self.minutes = minutes
        self.debug = debug
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_projects)
        self.min_value = min_value

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
        if not project_data:
            with open('no_project_data_found.html', 'w') as fw:
                print(content, file=fw)
            message = "No project data found; See no_project_data_found.html"
            print(message)
            AlertWindow.open(message)
            return

        projects = parse_project_data(project_data)
        if not projects:
            with open('no_projects_found.txt', 'w') as fw:
                print(project_data, file=fw)
            message = "No projects found inside of project data; See no_projects_found.txt"
            print(message)
            AlertWindow.open(message)

        total_project_count = len(projects)
        # ignore projects that don't pay or don't have tasks.
        projects = [p for p in projects if p.rate_per_hour > 0 and p.available_tasks > 0]
        if self.min_value > 0:
            projects = [p for p in projects if p.rate_per_hour >= self.min_value]
        print(f"Total project count: {total_project_count}; pay>0 and tasks>0: {len(projects)}")

        # unique-ify project list by uuid
        project_dict = dict()
        for p in projects:
            project_dict[p.uuid] = p
        projects = list(project_dict.values())

        if projects:
            ProjectWindow.open(projects)
            message = f"{len(projects)} projects!\n\n{'\n----------\n\n'.join(map(str,projects))}"
            send_message(message)

        print("Project fetch finished successfully")

    def start(self, run_now:bool=True):
        if run_now:
            self.timer.singleShot(0, self.fetch_projects)
        self.timer.start(self.minutes * 60 * 1000)
