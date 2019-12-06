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

SAVE_FOLDER = '/home/akettere/PycharmProjects/ECE_60872/resources/'
KEYS_PATH = '/home/akettere/PycharmProjects/ECE_60872/keys.yaml'


def document_pull_request_info(pr, bug_label=None):
    """
    This saves all info related to a pull request
    :param pr: The pull request
    :param label: The desired label on the pull request
    :return:
    """
    # Get a dictionary of the pull request's attributes
    pr_dict = pr.__dict__
    # print('Writing Data for Pull Request: {} {}'.format(pr_dict['_rawData']['base']['repo']['name'],
    #                                                     pr_dict['_rawData']['number']))

    # pprint.pprint(pr_dict['_rawData']['labels'])
    if bug_label is not None:
        has_bug_label = False
        for label in pr_dict['_rawData']['labels']:
            if label['name'] == bug_label:
                has_bug_label = True
        if not has_bug_label:
            # print('Does not have the bug label')
            return
        else:
            print('Has the bug label')

    # pprint.pprint(pr_dict) # pprint (Pretty Print) is a nice way to view the dict

    # Create a directory for this project
    project_folder = os.path.join(SAVE_FOLDER,
                                  pr_dict['_rawData']['base']['repo']['name'],
                                  str(pr_dict['_rawData']['number']))
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    # Save the pull request data
    pr_filename = os.path.join(project_folder, 'pull_request.yaml')
    with open(pr_filename, 'w') as outfile:
        yaml.dump(pr.__dict__, outfile, default_flow_style=False)

    # Save the diff patch data
    diff_filename = os.path.join(project_folder, 'pull_request.diff')
    diff_url = pr.__dict__['_rawData']['diff_url']
    urllib.request.urlretrieve(diff_url, diff_filename)


def main():
    # Takes in argument for the repo and label that you are looking for
    parser = ArgumentParser()
    parser.add_argument('-r', '--repo', required=False, default='arduino/Arduino', help='Name of Github repo.')
    parser.add_argument('-b', '--label', required=False, default='Type: Bug', help='Desired label.')
    args = parser.parse_args()

    # Takes the github access key from the key yaml file
    with open(KEYS_PATH, "r") as stream:
        github_key = yaml.load(stream, Loader=yaml.BaseLoader)['github_key']

    # Makes a request to github for pull requests from the given repo
    github = Github(github_key)
    repo = github.get_repo(args.repo)
    pull_requests = repo.get_pulls(state='closed', sort='created', direction='desc')

    # # Documents all pull requests
    i = 0
    for pull_request in pull_requests:
        i += 1
        print(i)
        document_pull_request_info(pull_request, bug_label=args.label)

    # pr = repo.get_pull(8281)
    # document_pull_request_info(pr, bug_label=args.label)


if __name__ == '__main__':
    main()
