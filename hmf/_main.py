import h5py
import meshio
import numpy

meshio_to_xdmf_type = {
    "vertex": ["Polyvertex"],
    "line": ["Polyline"],
    "triangle": ["Triangle"],
    "quad": ["Quadrilateral"],
    "tetra": ["Tetrahedron"],
    "pyramid": ["Pyramid"],
    "wedge": ["Wedge"],
    "hexahedron": ["Hexahedron"],
    "line3": ["Edge_3"],
    "triangle6": ["Triangle_6", "Tri_6"],
    "quad8": ["Quadrilateral_8", "Quad_8"],
    "tetra10": ["Tetrahedron_10", "Tet_10"],
    "pyramid13": ["Pyramid_13"],
    "wedge15": ["Wedge_15"],
    "hexahedron20": ["Hexahedron_20", "Hex_20"],
}
xdmf_to_meshio_type = {v: k for k, vals in meshio_to_xdmf_type.items() for v in vals}


def raw_from_cell_data(cell_data):
    # merge cell data
    cell_data_raw = {}
    for d in cell_data.values():
        for name, values in d.items():
            if name in cell_data_raw:
                cell_data_raw[name].append(values)
            else:
                cell_data_raw[name] = [values]
    for name in cell_data_raw:
        cell_data_raw[name] = numpy.concatenate(cell_data_raw[name])

    return cell_data_raw


def cell_data_from_raw(cells, cell_data_raw):
    cell_data = {k: {} for k in cells}
    for key in cell_data_raw:
        d = cell_data_raw[key]
        r = 0
        for k in cells:
            cell_data[k][key] = d[r : r + len(cells[k])]
            r += len(cells[k])
    return cell_data


def read(filename):
    with h5py.File(filename, "r") as f:
        assert f.attrs["type"] == "hmf"
        assert f.attrs["version"] == "0.1"

        assert len(f) == 1, "only one domain supported for now"
        domain = f["domain"]

        assert len(domain) == 1, "only one grid supported for now"
        grid = domain["grid"]

        points = None
        cells = {}
        point_data = {}
        cell_data_raw = {}
        field_data = {}

        for key, value in grid.items():
            if key[:8] == "Topology":
                cell_type = value.attrs["TopologyType"]
                cells[xdmf_to_meshio_type[cell_type]] = value[()]

            elif key == "Geometry":
                # TODO is GeometryType really needed?
                assert value.attrs["GeometryType"] in ["XY", "XYZ"]
                points = value[()]

            else:
                assert key == "Attribute"
                name = value.attrs["Name"]
                if value.attrs["Center"] == "Node":
                    point_data[name] = value[()]
                else:
                    assert value.attrs["Center"] == "Cell"
                    cell_data_raw[name] = value[()]

        cell_data = cell_data_from_raw(cells, cell_data_raw)

        return meshio.Mesh(
            points,
            cells,
            point_data=point_data,
            cell_data=cell_data,
            field_data=field_data,
        )


def write_points_cells(filename, points, cells, **kwargs):
    write(filename, meshio.Mesh(points, cells), **kwargs)


def write(filename, mesh, compression="gzip", compression_opts=None):
    with h5py.File(filename, "w") as h5_file:
        h5_file.attrs["type"] = "hmf"
        h5_file.attrs["version"] = "0.1"
        domain = h5_file.create_group("domain")
        grid = domain.create_group("grid")
        # information = grid.create_group("information")
        # information.attrs["value"] = len(mesh.field_data)

        write_points(grid, mesh.points, compression, compression_opts)
        # self.field_data(mesh.field_data, information)
        write_cells(mesh.cells, grid, compression, compression_opts)
        write_point_data(mesh.point_data, grid, compression, compression_opts)
        write_cell_data(mesh.cell_data, grid, compression, compression_opts)


def write_points(grid, points, compression, compression_opts):
    if points.shape[1] == 1:
        geometry_type = "X"
    elif points.shape[1] == 2:
        geometry_type = "XY"
    else:
        assert points.shape[1] == 3
        geometry_type = "XYZ"

    geo = grid.create_dataset(
        "Geometry",
        data=points,
        compression=compression,
        compression_opts=compression_opts,
    )
    geo.attrs["GeometryType"] = geometry_type


def write_cells(cells, grid, compression, compression_opts):
    for k, (meshio_type, value) in enumerate(cells.items()):
        xdmf_type = meshio_to_xdmf_type[meshio_type][0]
        topo = grid.create_dataset(
            f"Topology{k}",
            data=value,
            compression=compression,
            compression_opts=compression_opts,
        )
        topo.attrs["TopologyType"] = xdmf_type


def write_point_data(point_data, grid, compression, compression_opts):
    for name, data in point_data.items():
        att = grid.create_dataset(
            "Attribute",
            data=data,
            compression=compression,
            compression_opts=compression_opts,
        )
        att.attrs["Name"] = name
        att.attrs["Center"] = "Node"


def write_cell_data(cell_data, grid, compression, compression_opts):
    raw = raw_from_cell_data(cell_data)
    for name, data in raw.items():
        att = grid.create_dataset(
            "Attribute",
            data=data,
            compression=compression,
            compression_opts=compression_opts,
        )
        att.attrs["Name"] = name
        att.attrs["Center"] = "Cell"
