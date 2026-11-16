import os
import shutil


def main() -> None:
    # Prepare public
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    rcp("static", "public")


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
