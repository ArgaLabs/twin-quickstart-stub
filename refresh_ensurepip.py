"""Keep Python's offline pip bootstrap wheel aligned with the patched installed pip."""

from __future__ import annotations

import ensurepip
import importlib.metadata
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    version = importlib.metadata.version("pip")
    if tuple(int(part) for part in version.split(".")[:2]) < (26, 2):
        raise RuntimeError(
            "Upgrade installed pip to >=26.2 before refreshing ensurepip"
        )

    module = Path(ensurepip.__file__)
    bundled = module.parent / "_bundled"
    source, replacements = re.subn(
        r'(?m)^_PIP_VERSION = [\'"][^\'"\n]+[\'"]$',
        f'_PIP_VERSION = "{version}"',
        module.read_text(),
    )
    if replacements != 1:
        raise RuntimeError(
            "Unsupported ensurepip layout; refusing to leave bootstrap inconsistent"
        )

    with tempfile.TemporaryDirectory() as directory:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--no-cache-dir",
                "--no-deps",
                "--only-binary=:all:",
                "--dest",
                directory,
                f"pip=={version}",
            ],
            check=True,
        )
        wheel = Path(directory) / f"pip-{version}-py3-none-any.whl"
        if not wheel.is_file():
            raise RuntimeError("Expected pip bootstrap wheel was not downloaded")
        shutil.copyfile(wheel, bundled / wheel.name)
        module.write_text(source)
        for old_wheel in bundled.glob("pip-*.whl"):
            if old_wheel.name != wheel.name:
                old_wheel.unlink()

    subprocess.run([sys.executable, "-m", "ensurepip", "--version"], check=True)


if __name__ == "__main__":
    main()
