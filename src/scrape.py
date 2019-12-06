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

SAVE_FOLDER = '../resources/'
KEYS_PATH = '../keys.yaml'


def document_pull_request_info(pr, bug_label=None):
    """
    This saves all info related to a pull request
    :param pr: The pull request
    :param bug_label: The desired label on the pull request
    :return:
    """
    # Get a dictionary of the pull request's attributes
    pr_dict = pr.__dict__

    # Check if this matches the label we desire
    if bug_label is not None:
        has_bug_label = False
        for label in pr_dict['_rawData']['labels']:
            if label['name'] == bug_label:
                has_bug_label = True
        if not has_bug_label:
            return
        else:
            print('Desired Pull Request Found!')

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
        yaml.dump(pr_dict, outfile, default_flow_style=False)

    # Save the diff patch data
    diff_filename = os.path.join(project_folder, 'pull_request.diff')
    diff_url = pr_dict['_rawData']['diff_url']
    urllib.request.urlretrieve(diff_url, diff_filename)


def main():
    """
    Used to go through pull requests and take those that are labeled in a certain way. Currently for bugs.

    Example usage python3 --repo_yaml ../labled_repos.yaml
    :return:
    """
    # Takes in argument for the repo and label that you are looking for
    parser = ArgumentParser()
    parser.add_argument('-r', '--repo_yaml', required=False, default=None,
                        help='YAML Containing repo and keys to look for')
    args = parser.parse_args()

    # Takes the github access key from the key yaml file
    with open(KEYS_PATH, "r") as stream:
        github_key = yaml.load(stream, Loader=yaml.BaseLoader)['github_key']

    # Makes a request to github for pull requests from the given repo
    github = Github(github_key)

    with open(args.repo_yaml, "r") as ry:
        yaml_dir = yaml.load(ry, Loader=yaml.BaseLoader)

    # pprint.pprint(yaml_dir)
    for key in yaml_dir:
        directory_dir = os.path.join('../resources', yaml_dir[key]['repo'].split('/')[1])
        if not os.path.isdir(directory_dir):
            repo = github.get_repo(yaml_dir[key]['repo'])
            pull_requests = repo.get_pulls(state='closed', sort='created', direction='asc')

            # Documents all pull requests
            counter = 1
            for pull_request in pull_requests:
                print('#{} Examing PR {} From Repo {}'.format(counter, pull_request.__dict__['_rawData']['number'],
                                                          yaml_dir[key]['repo']))
                document_pull_request_info(pull_request, bug_label=yaml_dir[key]['label'])
                counter += 1


if __name__ == '__main__':
    main()
