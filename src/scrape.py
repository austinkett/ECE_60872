from github import Github
import pprint
import os
import yaml
import urllib.request

SAVE_FOLDER = '/home/akettere/PycharmProjects/ECE_60872/resources/'


def document_pull_request_info(pr):
    # Get a dictionary of the pull request's attributes
    pr_dict = pr.__dict__
    print('Writing Data for Pull Request: {} {}'.format(pr_dict['_rawData']['base']['repo']['name'],
                                                        pr_dict['_rawData']['number']))
    # pprint.pprint(pr_dict)

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
    github = Github()
    repo = github.get_repo('angr/angr-doc')
    pull_requests = repo.get_pulls(state='closed')
    for pull_request in pull_requests:
        document_pull_request_info(pull_request)
    # pr = repo.get_pull(226)


if __name__ == '__main__':
    main()
