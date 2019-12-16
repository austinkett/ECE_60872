"""
scrape.py

The goal of this file is to request and save pull request information from Github repos.
"""

from github import Github
import pprint
import os
import yaml
import urllib.request
from argparse import ArgumentParser
import shutil

SAVE_FOLDER = '../resources/'
KEYS_PATH = '../keys.yaml'


def main():
    """
    This file was used to load issues for the ML analysis on Defects4J's JacksonDatabind. It is not as automated
    as the pull requests are as I only needed this for a small analysis.
    :return:
    """
    with open('C:\\Users\\Austin\\PycharmProjects\\ECE_60872\\resources\\defects4j_JacksonDatabind') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    buggy_patches = []

    for line in content:
        buggy_patches.append(line.split('/')[-1])

    with open(KEYS_PATH, "r") as stream:
        github_key = yaml.load(stream, Loader=yaml.BaseLoader)['github_key']

    g = Github(github_key)
    repo = g.get_repo("FasterXML/jackson-databind")
    issues = repo.get_issues(sort='created', direction='asc', state='closed')

    CHOSEN_PATH = 'C:\\Users\\Austin\\PycharmProjects\\ECE_60872\\resources\\ml_data_JD\\chosen_bug'
    OTHERS = 'C:\\Users\\Austin\\PycharmProjects\\ECE_60872\\resources\\ml_data_JD\\other_patch'

    for issue in issues:
        try:
            print(issue)
            if issue.number > 2400:
                break

            if issue.number in buggy_patches:
                path = CHOSEN_PATH
            else:
                path = OTHERS

            path = os.path.join(path, str(issue.number) + '.txt')

            with open(path, 'w') as f:
                comments = issue.get_comments()
                for comment in comments:
                    print(comment.body, file=f)
        except Exception as e:
            pass

    for i in buggy_patches:
        try:
            shutil.move('C:\\Users\\Austin\\PycharmProjects\\ECE_60872\\resources\\ml_data_JD\\other_patch\\'
                        + str(i) + '.txt',
                        'C:\\Users\\Austin\\PycharmProjects\\ECE_60872\\resources\\ml_data_JD\\chosen_bug\\'
                        + str(i) + '.txt')
        except FileNotFoundError as e:
            pass

    return


if __name__ == '__main__':
    main()
