import os
import tarfile
import tempfile

import meshio


def write(filename, mesh, data_format="HDF", compression="gzip"):
    basename = os.path.splitext(os.path.basename(filename))[0]
    with tempfile.TemporaryDirectory() as tmpdir:
        meshio.xdmf.write(
            os.path.join(tmpdir, basename + ".xdmf"),
            mesh,
            data_format=data_format,
            compression=compression,
        )
        with tarfile.open(filename, "w") as tar:
            tar.add(tmpdir, arcname="")


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
