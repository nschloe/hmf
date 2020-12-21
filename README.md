<p align="center">
  <a href="https://github.com/nschloe/hmf"><img alt="hmf" src="https://nschloe.github.io/hmf/logo.svg" width="30%"></a>
  <p align="center"><a href="https://en.wikipedia.org/wiki/Hierarchical_Data_Format">HDF</a>-only <a href="http://xdmf.org/index.php/Main_Page">XDMF</a>.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/hmftools.svg?style=flat-square)](https://pypi.org/project/hmftools)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/hmftools.svg?style=flat-square)](https://pypi.org/pypi/hmftools/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/hmftools.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/hmftools)
[![PyPi downloads](https://img.shields.io/pypi/dm/hmftools.svg?style=flat-square)](https://pypistats.org/packages/hmftools)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/hmftools/ci?style=flat-square)](https://github.com/nschloe/hmftools/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/hmftools.svg?style=flat-square)](https://codecov.io/gh/nschloe/hmftools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

[The XDMF data and mesh format](http://xdmf.org/index.php/Main_Page) is arguably one of
the best mesh formats out there in terms of file size, I/O speed, and ecosystem support.
There is one annoyance though that has bugged me over the years: If using the binary or
HDF data type (which you should), an XDMF archive consists of _multiple_ files. When
copying things over, it is easy to miss or accidentally replace one of those.

Along comes HMF. It's just like XDMF, except that it restricts itself to HDF data (which
most XDMF files use anyway) and puts all the meta data (which for XDMF is found in the
XML file) into the HDF file. This way, you're only ever dealing with one file.

This repository contains a Python package that makes working with HMF files easy.
Install with
```
pip install hmftools
```
and use the command-line tools
```bash
hmf-info <input-hmf>                               # print some info about the file
hmf-convert <input-mesh-file> <output-mesh-file>   # convert to/from HMF into other formats
hmf-compress <input-hmf>                           # compress the HMF file
hmf-uncompress <input-hmf>                         # uncompress the HMF file
```
Note that compressed HMF files (which is the default) tend to be much smaller, but
require a bit longer to read. Depending on how often you need to read a file, you might
want to `hmf-uncompress` it first.

#### ParaView plugin

After installing the hmftools, you can use a plugin to read HMF files with ParaView.
Open ParaView, go to

> _Tools_ -> _Manage Plugins..._ -> _Load New ..._

and select the file `paraview-hmf-plugin.py` (typically installed at
`$HOME/.local/paraview-plugins/paraview-hmf-plugin.py`). Also activate _Auto Load_.

After that, you can view any HMF file with ParaView. Note that you might have to start
ParaView with
```
HDF5_DISABLE_VERSION_CHECK=1 paraview out.hmf
```
to avoid a version warning/error.


### License

The code in this repository is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
