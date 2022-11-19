from argparse import Namespace

class SRTeArgs():
    file: str | None
    verbose: bool

    def __init__(self, args: Namespace):
        self.file = args.file
        self.verbose = args.verbose if args.verbose is not None else False