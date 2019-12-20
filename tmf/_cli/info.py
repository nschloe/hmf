import argparse
import os

import numpy

from .._main import read
from .common import _get_version_text


def info(argv=None):
    # Parse command line arguments.
    parser = _get_info_parser()
    args = parser.parse_args(argv)

    # read mesh data
    mesh = read(args.infile)
    size = os.stat(args.infile).st_size / 1024.0 ** 2
    print(f"File size: {size} MB")
    print(mesh)

    # check if the cell arrays are consistent with the points
    is_consistent = True
    for cells in mesh.cells.values():
        if numpy.any(cells > mesh.points.shape[0]):
            print("\nATTENTION: Inconsistent mesh. Cells refer to nonexistent points.")
            is_consistent = False
            break

    # check if there are redundant points
    if is_consistent:
        point_is_used = numpy.zeros(mesh.points.shape[0], dtype=bool)
        for cells in mesh.cells.values():
            point_is_used[cells] = True
        if numpy.any(~point_is_used):
            print("ATTENTION: Some points are not part of any cell.")


def _get_info_parser():
    parser = argparse.ArgumentParser(
        description=("Print tmf mesh info."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("infile", type=str, help="tmf mesh file to be read from")

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )
    return parser
