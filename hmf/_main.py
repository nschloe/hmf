"""
I/O for XDMF.
http://www.xdmf.org/index.php/XDMF_Model_and_Format
"""
import os
from io import BytesIO

import h5py
import meshio
import numpy

# from .._common import CDATA, cell_data_from_raw, raw_from_cell_data, write_xml
# from .._exceptions import ReadError, WriteError
# from .._helpers import register
# from .._mesh import Mesh
# from .common import (
#     attribute_type,
#     dtype_to_format_string,
#     meshio_to_xdmf_type,
#     meshio_type_to_xdmf_index,
#     numpy_to_xdmf_dtype,
#     translate_mixed_cells,
#     xdmf_to_meshio_type,
#     xdmf_to_numpy_type,
# )
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


def attribute_type(data):
    # <http://www.xdmf.org/index.php/XDMF_Model_and_Format#Attribute>
    if len(data.shape) == 1 or (len(data.shape) == 2 and data.shape[1] == 1):
        return "Scalar"
    elif len(data.shape) == 2 and data.shape[1] in [2, 3]:
        return "Vector"
    elif (len(data.shape) == 2 and data.shape[1] == 9) or (
        len(data.shape) == 3 and data.shape[1] == 3 and data.shape[2] == 3
    ):
        return "Tensor"
    elif len(data.shape) == 2 and data.shape[1] == 6:
        return "Tensor6"

    assert len(data.shape) == 3
    return "Matrix"


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
            print(key)

            if key[:8] == "Topology":
                cell_type = value.attrs["TopologyType"]
                cells[xdmf_to_meshio_type[cell_type]] = value[()]

            elif key == "Geometry":
                # TODO is GeometryType really needed?
                assert value.attrs["GeometryType"] in ["XY", "XYZ"]
                points = value[()]

            elif key == "Information":
                c_data = c.text
                if not c_data:
                    raise ReadError()
                field_data = self.read_information(c_data)

            else:
                assert key == "Attribute"
                # Don't be too strict here: FEniCS, for example, calls this
                # 'AttributeType'.
                # assert c.attrib['Type'] == 'None'

                data_items = list(c)
                if len(data_items) != 1:
                    raise ReadError()
                data_item = data_items[0]

                data = self._read_data_item(data_item)

                name = c.attrib["Name"]
                if c.attrib["Center"] == "Node":
                    point_data[name] = data
                else:
                    if c.attrib["Center"] != "Cell":
                        raise ReadError()
                    cell_data_raw[name] = data

        cell_data = cell_data_from_raw(cells, cell_data_raw)

        return meshio.Mesh(
            points,
            cells,
            point_data=point_data,
            cell_data=cell_data,
            field_data=field_data,
        )





def _read_data_item(self, data_item):
    info = data_item.text.strip()
    filename, h5path = info.split(":")

    # The HDF5 file path is given with respect to the XDMF (XML) file.
    full_hdf5_path = os.path.join(os.path.dirname(self.filename), filename)

    f = h5py.File(full_hdf5_path, "r")
    if h5path[0] != "/":
        raise ReadError()

    for key in h5path[1:].split("/"):
        f = f[key]
    # `[()]` gives a numpy.ndarray
    return f[()]


def read_information(self, c_data):
    field_data = {}
    root = ET.fromstring(c_data)
    for child in root:
        str_tag = child.attrib["key"]
        dim = int(child.attrib["dim"])
        num_tag = int(child.text)
        field_data[str_tag] = numpy.array([num_tag, dim])
    return field_data


def write_points_cells(
    filename, points, cells, compression=None, compression_opts=None
):
    write(
        filename, meshio.Mesh(points, cells), compression=None, compression_opts=None,
    )


def write(filename, mesh, compression=None, compression_opts=None):
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
        att.attrs["name"] = name
        att.attrs["center"] = "Node"
        att.attrs["AttributeType"] = attribute_type(data)


def write_cell_data(cell_data, grid, compression, compression_opts):
    raw = raw_from_cell_data(cell_data)
    for name, data in raw.items():
        att = grid.create_dataset(
            "Attribute",
            data=data,
            compression=compression,
            compression_opts=compression_opts,
        )
        att.attrs["name"] = name
        att.attrs["center"] = "Cell"
        att.attrs["AttributeType"] = attribute_type(data)


# def write_field_data(self, field_data, information):
#     info = ET.Element("main")
#     for name, data in field_data.items():
#         data_item = ET.SubElement(info, "map", key=name, dim=str(data[1]))
#         data_item.text = str(data[0])
#     # information.text = ET.CDATA(ET.tostring(info))
#     information.append(CDATA(ET.tostring(info).decode("utf-8")))
