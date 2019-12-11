# tmf

The XDMF data and mesh format is arguably one of the best mesh format out there in terms
of file size, I/O speed, and ecosystem. There is one annoyance though that has bugged me
over the years: When using the Binary or HDF data type (which you should), an XDMF
archive consists of multiple files. When copying things over, it is easy to miss or
accidentally replace one of those.

Along comes TMF, tar + XDMF. It's just like XDMF, except that it puts all files in on
tarball, the tmf file.
