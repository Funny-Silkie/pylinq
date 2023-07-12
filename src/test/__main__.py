import os
from unittest import TestLoader, TestSuite, TextTestRunner


if __name__ == "__main__":
    dir: str = os.path.dirname(__file__)

    test: TestSuite = TestLoader().discover(dir, "[a-z]*.py")
    TextTestRunner().run(test)
