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
SUBMISSION_DIR = '../submission/'
RESOURCES_DIR = '../resources/'


def add_n_files_from_folder(moss, folder_name, n=10):
    """
    Takes up to n files from the given resource folder and submits them to MOSS
    :param moss: The moss instance
    :param folder_name: Name of the folder (must be in resources)
    :param n: The number of files to send
    :return:
    """
    counter = 0
    paths = glob(os.path.join(RESOURCES_DIR, folder_name, "*"))
    for path in paths:
        # Only add so many files from each directory
        counter += 1
        if counter > n:
            break

        pr_number = path.split('/')[-1]

        # Take files we made and put them into a special submission directory
        diff_file = os.path.join(path, 'pull_request.diff')
        diff_file_new = os.path.join(SUBMISSION_DIR, folder_name)
        if not os.path.exists(diff_file_new):
            os.makedirs(diff_file_new)
        diff_file_new = os.path.join(diff_file_new, str(pr_number) + '.diff')

        # Erase many of the unncessary lines such as diff comments and import statements
        try:
            with open(diff_file, 'r') as df:
                with open(diff_file_new, 'w') as dfn:
                    line = df.readline()
                    while line:
                        if (line[0:4] != 'diff' and line[0:5] != 'index' and line[0:3] != '---' and line[0:3] != '+++'
                                and line[1:7] != 'import'):
                            dfn.write(line)
                        else:
                            dfn.write('\n')
                        line = df.readline()
        except UnicodeDecodeError as e:
            pass

        # copyfile(diff_file, diff_file_new)
        if os.path.getsize(diff_file_new) > 0:
            moss.addFile(diff_file_new)


def main():
    """
    This allows us to send all of the diff bug reports that we generated into MOSS to compare them.
    :return:
    """
    with open(KEYS_PATH, "r") as stream:
        moss_key = yaml.load(stream, Loader=yaml.BaseLoader)['moss_key']

    # The MOSS instance
    m = mosspy.Moss(moss_key, "C")

    # This means that only files from separate directories will be compared to eachother
    m.setDirectoryMode(1)

    # The directories files will be taken from
    compare_list = ['Arduino', 'ardupilot', 'elasticsearch']

    # The number of files sent from each directory
    n = 10

    # Add's files to the MOSS request that will be send
    for name in compare_list:
        add_n_files_from_folder(m, name, n)

    print('Sending files to MOSS')

    url = m.send()  # Submission Report URL

    print("Report Url: " + url)
    m.saveWebPage(url, "../submission/report.html")
    mosspy.download_report(url, "../submission/report/", connections=8)


if __name__ == "__main__":
    main()
