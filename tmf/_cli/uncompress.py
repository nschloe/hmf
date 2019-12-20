import argparse

from .._main import read as tmf_read
from .._main import write as tmf_write
from .common import _get_version_text


def uncompress(argv=None):
    # Parse command line arguments.
    parser = _get_parser()
    args = parser.parse_args(argv)
    mesh = tmf_read(args.file)
    tmf_write(args.file, mesh, compression=None)


def _get_parser():
    parser = argparse.ArgumentParser(
        description=("Uncompress tmf file."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("file", type=str, help="tmf mesh file to uncompress")

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )
    return parser
