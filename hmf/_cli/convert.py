import argparse
import os

import numpy

from meshio._helpers import _writer_map, read, reader_map, write

from .._main import read as hmf_read
from .._main import write as hmf_write
from .common import _get_version_text


def convert(argv=None):
    # Parse command line arguments.
    parser = _get_convert_parser()
    args = parser.parse_args(argv)

    # read mesh data
    if args.input_format is None:
        is_hmf = os.path.splitext(args.infile)[-1] == ".hmf"
    else:
        is_hmf = args.input_format.lower() == "hmf"

    if is_hmf:
        mesh = hmf_read(args.infile)
    else:
        mesh = read(args.infile, file_format=args.input_format)

    if args.prune:
        mesh.prune()

    if (
        args.prune_z_0
        and mesh.points.shape[1] == 3
        and numpy.all(numpy.abs(mesh.points[:, 2]) < 1.0e-13)
    ):
        mesh.points = mesh.points[:, :2]

    # Some converters (like VTK) require `points` to be contiguous.
    mesh.points = numpy.ascontiguousarray(mesh.points)

    # write it out
    if args.output_format is None:
        is_hmf = os.path.splitext(args.outfile)[-1] == ".hmf"
    else:
        is_hmf = args.output_format.lower() == "hmf"

    if is_hmf:
        hmf_write(args.outfile, mesh)
    else:
        write(args.outfile, mesh, file_format=args.output_format)


def _get_convert_parser():
    parser = argparse.ArgumentParser(
        description=("Convert between mesh formats."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("infile", type=str, help="mesh file to be read from")

    parser.add_argument(
        "--input-format",
        "-i",
        type=str,
        choices=list(reader_map.keys()),
        help="input file format",
        default=None,
    )

    parser.add_argument(
        "--output-format",
        "-o",
        type=str,
        choices=list(_writer_map.keys()),
        help="output file format",
        default=None,
    )

    parser.add_argument("outfile", type=str, help="mesh file to be written to")

    parser.add_argument(
        "--prune",
        "-p",
        action="store_true",
        help="remove lower order cells, remove orphaned nodes",
    )

    parser.add_argument(
        "--prune-z-0",
        "-z",
        action="store_true",
        help="remove third (z) dimension if all points are 0",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )
    return parser
