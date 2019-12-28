import os
import tarfile
import tempfile

import meshio


def write(filename, mesh, compression="gzip", compression_opts=None):
    data_format = "HDF"
    basename = os.path.splitext(os.path.basename(filename))[0]
    with tempfile.TemporaryDirectory() as tmpdir:
        meshio.xdmf.write(
            os.path.join(tmpdir, basename + ".xdmf"),
            mesh,
            data_format=data_format,
            compression=compression,
            compression_opts=compression_opts,
        )
        with tarfile.open(filename, "w") as tar:
            tar.add(tmpdir, arcname="")


def write_points_cells(
    filename, points, cells, compression="gzip", compression_opts=None
):
    write(
        filename,
        meshio.Mesh(points, cells),
        compression=compression,
        compression_opts=compression_opts,
    )


def read(filename):
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(filename, "r") as tar:
            tar.extractall(tmpdir)

        found_xdmf = False
        for f in os.listdir(tmpdir):
            if f.endswith(".xdmf") or f.endswith(".xmf"):
                mesh = meshio.read(os.path.join(tmpdir, f))
                found_xdmf = True

    if not found_xdmf:
        raise RuntimeError("Could not find XDMF file in archive.")

    return mesh
