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
    ipdb: bool
    min_value: Optional[int]


def main():
    parser = argparse.ArgumentParser(description="Check for new projects periodically.")
    parser.add_argument("--interval", type=int, default=5, help="Interval between checks in minutes.")
    parser.add_argument("--debug", default=False, action='store_true', help="Don't actually check the website; use a pre-saved webpage sample.")
    parser.add_argument("--skip", default=False, action='store_true', help="Skip the first occurrence, i.e. sleep before our first project check.")
    parser.add_argument("--parser", type=str, help='Path to module in webserver format, e.g. parsers.div_attribute_json:MyParser')
    parser.add_argument("--ipdb", default=False, action='store_true', help="Debug the code using ipdb (or pdb if ipdb isn't installed)")
    parser.add_argument("--min-value", default=0, type=int, help="Minimum dollar value of tasks to show; filters out tasks below this value.")
    args = parser.parse_args(namespace=ProjectCheckerNamespace)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if args.ipdb:
        try:
            import ipdb as pdb
        except ImportError:
            import pdb
        pdb.set_trace()

    kwargs = dict()
    if args.parser:
        kwargs['parser'] = load_parser(*args.parser.split(':', maxsplit=1))
        print("Loaded parser:", type(kwargs['parser']))

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    dat_session = DATSession()
    pf = ProjectFetcher(dat_session, args.interval, debug=args.debug, min_value=args.min_value, **kwargs)
    pf.start(run_now=not args.skip)
    app.exec()


if __name__ == "__main__":
    main()
