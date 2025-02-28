from tests.file_tests import run_file_test
from tests.runner import run_tests


def _tests(args) -> None:
    if args.file:
        run_file_test(args.file)
    else:
        run_tests()


def add_subparser(subparsers) -> None:
    p = subparsers.add_parser("tests", aliases=["t"], help="run test suite")
    p.set_defaults(func=_tests)

    p.add_argument(
        "--file",
        "-f",
    )
