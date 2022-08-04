from Pasteparser import Pasteparser
from Bot import Bot


def main():
    Bot().start()
    Pasteparser().start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
