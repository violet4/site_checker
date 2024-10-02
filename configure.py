import csv
import os

from site_checker.dat_session_handler import (
    DATSession, _default_cookies_path, _sample_html_path,
    _default_headers_path,
)
from site_checker.project import _url_base_filename


def main():
    if not os.path.exists(DATSession._project_url_file):
        project_url = input("What website URL would you like to use? ")
        with open(DATSession._project_url_file, 'w') as fw:
            print(project_url, file=fw)
    if not os.path.exists(_url_base_filename):
        url = input("If the extracted data needs a url prefix, what should that be?\n"
                    "e.g. https://mysite.com/?id=\n"
                    "Enter here: ")
        with open(_url_base_filename, 'w') as fw:
            print(url, file=fw)
    if not os.path.exists(_default_cookies_path):
        print(f"Please fill out the cookies file {_default_cookies_path} created for you with any session cookies needed to authorize yourself to the website.")
        with open(_default_cookies_path, 'w') as fw:
            csvw = csv.writer(fw, delimiter='\t')
            headers = 'name	value	domain	path	expires'.split('\t')
            csvw.writerows(headers)
            # empty row shows csv structure
            csvw.writerow(['']*len(headers))
    if not os.path.exists(_default_headers_path):
        with open(_default_headers_path, 'w') as fw:
            pass
        print(f"Please copy-paste headers from a sample call from your web browser into file {_default_headers_path}")
    if not os.path.exists(_sample_html_path):
        with open(_sample_html_path, 'w') as fw:
            print(file=fw)
        print("If you have a sample html/api call response content, please place it in:", _sample_html_path)
