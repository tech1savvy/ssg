import os
import shutil
import sys

from ssg.generate import genrate_pages_recursive


def main() -> None:
    base_path = "/"

    # Parse cli args
    args = sys.argv
    if len(args) >= 2 and args[1] != "":
        base_path = args[1]

    # Prepare docs
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    rcp("static", "docs")

    #  Genrate html pages
    genrate_pages_recursive("content", "template.html", "docs", base_path)


def rcp(source, destination):
    # Prepare destination
    if not os.path.exists(destination):
        os.mkdir(destination)
    # Recursive copy dir
    for content in os.listdir(source):
        if os.path.isfile(os.path.join(source, content)):
            shutil.copy(os.path.join(source, content), destination)
            print(os.path.join(source, content))
        else:
            rcp(os.path.join(source, content), os.path.join(destination, content))


if __name__ == "__main__":
    main()
