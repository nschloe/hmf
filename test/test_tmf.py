import meshio
import tempfile
import os
import numpy
import tmf


tri_mesh_2d = meshio.Mesh(
    numpy.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]) / 3,
    {"triangle": numpy.array([[0, 1, 2], [0, 2, 3]])},
)


def test_write_read():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "out.tmf")
        tmf.write(filename, tri_mesh_2d)
        mesh = tmf.read(filename)

    tol = 1.0e-12
    assert numpy.all(numpy.abs(mesh.points - tri_mesh_2d.points) < tol)
    for key in mesh.cells.keys():
        assert numpy.all(mesh.cells[key] == tri_mesh_2d.cells[key])


if __name__ == "__main__":
    test_write_read()
