import argparse


class ArgsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.init_arguments()

    def init_arguments(self):
        self.parser.add_argument('--workers', type=int, default=1)
        self.parser.add_argument('--delay', type=float, default=1.0)
        self.parser.add_argument('--timeout', type=int, default=30)
        self.parser.add_argument('--retries', type=int, default=3)

    def get_args(self):
        return self.parser.parse_args()
