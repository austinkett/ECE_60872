"""
compare.py

The goal of this file is to use MOSS to compare all of the diff files which have been uploaded

Example Output: http://moss.stanford.edu/results/612995158

Usage Example: https://github.com/soachishti/moss.py
"""
import mosspy
import yaml
import os
from glob import glob

KEYS_PATH = '../keys.yaml'
COMPARE_DIR = '../resources/angr-doc/'


def main():
    with open(KEYS_PATH, "r") as stream:
        moss_key = yaml.load(stream, Loader=yaml.BaseLoader)['moss_key']

    m = mosspy.Moss(moss_key, "python")

    paths = glob(os.path.join(COMPARE_DIR, "*"))
    for path in paths:
        diff_file = os.path.join(path, 'pull_request.diff')
        if os.path.getsize(diff_file) > 0:
            m.addFile(diff_file)

    url = m.send()  # Submission Report URL

    print("Report Url: " + url)


if __name__ == "__main__":
    main()
