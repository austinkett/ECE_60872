import mosspy
import yaml

KEYS_PATH = '/home/akettere/PycharmProjects/ECE_60872/keys.yaml'


def main():
    with open(KEYS_PATH, "r") as stream:
        moss_key = yaml.load(stream, Loader=yaml.BaseLoader)['moss_key']

    m = mosspy.Moss(moss_key, "python")

    # m.addBaseFile("submission/test1.c")
    # m.addBaseFile("submission/test.c")

    m.addFile("submission/test1.c")
    m.addFile("submission/test.c")

    # Submission Files
    # m.addFile("submission/a01-sample.py")
    # m.addFilesByWildcard("submission/a01-*.py")

    url = m.send()  # Submission Report URL

    print("Report Url: " + url)

    # Save report file
    m.saveWebPage(url, "submission/report.html")

    # Download whole report locally including code diff links
    mosspy.download_report(url, "submission/report/", connections=8)


if __name__ == "__main__":
    main()
