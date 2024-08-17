import re
from typing import List
from decimal import Decimal

from .project import Project


pay_number_re = re.compile(r'\d+(\.\d{0,2})?')


def parse_project_data(data: dict) -> List[Project]:
    projects = []
    for project in data:
        uuid: str = project['id']
        title: str = project['name']
        rate = pay_number_re.search(project['pay'])
        rate = rate.group(0) if rate else '0.0'
        available_tasks = int(project['availableTasksFor'])
        project = Project(
            uuid=uuid.strip(),
            title=title.strip(),
            rate_per_hour=Decimal(rate),
            available_tasks=available_tasks,
        )
        projects.append(project)
    return projects
