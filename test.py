import yaml
from pprint import pprint


def main():
    with open('/home/akettere/PycharmProjects/ECE_60872/resources/ardupilot/2045/pull_request.yaml', 'r') as x:
        test = yaml.load(x, Loader=yaml.BaseLoader)
        pprint(test)


if __name__ == '__main__':
    main()
