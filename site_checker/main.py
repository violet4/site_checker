import argparse
import signal
from typing import Optional

from PySide6.QtWidgets import QApplication

from site_checker.project_fetcher import ProjectFetcher
from site_checker.project_page_parser import load_parser
from .dat_session_handler import DATSession


class ProjectCheckerNamespace(argparse.Namespace):
    interval: int
    debug: bool
    skip: bool
    parser: Optional[str]


def main():
    parser = argparse.ArgumentParser(description="Check for new projects periodically.")
    parser.add_argument("--interval", type=int, default=5, help="Interval between checks in minutes.")
    parser.add_argument("--debug", default=False, action='store_true', help="Don't actually check the website; use a pre-saved webpage sample.")
    parser.add_argument("--skip", default=False, action='store_true', help="Skip the first occurrence, i.e. sleep before our first project check.")
    parser.add_argument("--parser", type=str, help='Path to module in webserver format, e.g. parsers.div_attribute_json:MyParser')
    args = parser.parse_args(namespace=ProjectCheckerNamespace)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    kwargs = dict()
    if args.parser:
        kwargs['parser'] = load_parser(*args.parser.split(':', maxsplit=1))
        print("Loaded parser:", type(kwargs['parser']))

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    dat_session = DATSession()
    pf = ProjectFetcher(dat_session, args.interval, debug=args.debug, **kwargs)
    pf.start(run_now=not args.skip)
    app.exec()


if __name__ == "__main__":
    main()
