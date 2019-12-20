<p align="center">
  <a href="https://github.com/nschloe/tmf"><img alt="tmf" src="https://nschloe.github.io/tmf/logo.svg" width="30%"></a>
  <p align="center">Tarred XDMF.</p>
</p>

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/tmf/master.svg?style=flat-square)](https://circleci.com/gh/nschloe/tmf/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/tmf.svg?style=flat-square)](https://codecov.io/gh/nschloe/tmf)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![PyPi Version](https://img.shields.io/pypi/v/tmf.svg?style=flat-square)](https://pypi.org/project/tmf)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/tmf.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/tmf)
[![PyPi downloads](https://img.shields.io/pypi/dm/tmf.svg?style=flat-square)](https://pypistats.org/packages/tmf)

The XDMF data and mesh format is arguably one of the best mesh format out there in terms
of file size, I/O speed, and ecosystem. There is one annoyance though that has bugged me
over the years: When using the Binary or HDF data type (which you should), an XDMF
archive consists of multiple files. When copying things over, it is easy to miss or
accidentally replace one of those.

Along comes TMF, tar + XDMF. It's just like XDMF, except that it puts all files in on
tarball, the tmf file. It also restricts itself to HDF data (which most XDMF files use
anyway).

This repository contains a Python package that makes working with tmf files easy.
Install with
```
pip install tmf
```
and use the command-line tools
```
tmf-convert <input-mesh-file> <output-mesh-file>   # convert to/from tmf into other formats
tmf-info <input-tmf>                               # print some info about the file
tmf-compress <input-tmf>                           # compress the tmf file
tmf-uncompress <input-tmf>                         # uncompress the tmf file
```
Note that compressed tmf files (which is the default) tend to be much smaller, but
require a _bit_ longer to read. Depending on how often you need to read a file, you
might want to `tmf-uncompress` it first.


### License

The code in this repository is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
