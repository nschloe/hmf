import sys

from ..__about__ import __copyright__, __version__


def _get_version_text():
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    return f"hmf {__version__} [Python {python_version}]\n{__copyright__}"
