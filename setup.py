import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "hmf", "__about__.py"), "rb") as f:
    exec(f.read(), about)


setup(
    name="hmf",
    version=about["__version__"],
    packages=find_packages(),
    url="https://github.com/nschloe/hmf",
    project_urls={
        "Code": "https://github.com/nschloe/hmf",
        "Issue tracker": "https://github.com/nschloe/hmf/issues",
    },
    author=about["__author__"],
    author_email=about["__email__"],
    install_requires=["meshio", "lxml", "h5py"],
    description="Tar + XDMF mesh format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=about["__license__"],
    classifiers=[
        about["__license__"],
        about["__status__"],
        # See <https://pypi.org/classifiers/> for all classifiers.
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.6",
    data_files=[("paraview-plugins", ["scripts/paraview-hmf-plugin.py"])],
    entry_points={
        "console_scripts": [
            "hmf-info = hmf._cli:info",
            "hmf-convert = hmf._cli:convert",
            "hmf-compress = hmf._cli:compress",
            "hmf-uncompress = hmf._cli:uncompress",
        ]
    },
)
