<p align="center">
  <a href="https://github.com/nschloe/hmf"><img alt="hmf" src="https://nschloe.github.io/hmf/logo.svg" width="30%"></a>
  <p align="center"><a href="https://en.wikipedia.org/wiki/Tar_(computing)">tar</a> + <a href="http://xdmf.org/index.php/Main_Page">XDMF</a>.</p>
</p>

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/hmf/ci?style=flat-square)](https://github.com/nschloe/hmf/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![PyPi Version](https://img.shields.io/pypi/v/hmf.svg?style=flat-square)](https://pypi.org/project/hmf)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/hmf.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/hmf)
[![PyPi downloads](https://img.shields.io/pypi/dm/hmf.svg?style=flat-square)](https://pypistats.org/packages/hmf)

[The XDMF data and mesh format](http://xdmf.org/index.php/Main_Page) is arguably one of
the best mesh formats out there in terms of file size, I/O speed, and ecosystem support.
There is one annoyance though that has bugged me over the years: If using the binary or
HDF data type (which you should), an XDMF archive consists of _multiple_ files. When
copying things over, it is easy to miss or accidentally replace one of those.

Along comes TMF, tar + XDMF convenience format. It's just like XDMF, except that it puts
all files in one: tarball, the TMF file. It also restricts itself to HDF data (which
most XDMF files use anyway).

_Disadvantage:_ Since tar is inheriently serial, all your data has to be pushed through
one core and its memory. If your files are too large for that, better stick with vanilla
XDMF.

This repository contains a Python package that makes working with TMF files easy.
Install with
```
pip install hmf
```
and use the command-line tools
```bash
hmf-info <input-hmf>                               # print some info about the file
hmf-convert <input-mesh-file> <output-mesh-file>   # convert to/from TMF into other formats
hmf-compress <input-hmf>                           # compress the TMF file
hmf-uncompress <input-hmf>                         # uncompress the TMF file
```
Note that compressed TMF files (which is the default) tend to be much smaller, but
require a bit longer to read. Depending on how often you need to read a file, you might
want to `hmf-uncompress` it first.

#### ParaView plugin

You can use a plugin to read TMF files with ParaView. Open ParaView and go to

> _Tools_ -> _Manage Plugins..._ -> _Load New ..._

and select the file `paraview-hmf-plugin.py` (typically installed at
`$HOME/.local/paraview-plugins/paraview-hmf-plugin.py`). Also activate _Auto Load_.

After that, you can view any TMF file with ParaView. Note that you might have to start
ParaView with
```
HDF5_DISABLE_VERSION_CHECK=1 paraview out.hmf
```
to avoid a version warning/error.


### License

The code in this repository is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
