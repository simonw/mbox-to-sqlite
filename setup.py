from setuptools import setup
import os

VERSION = "0.1a0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="mbox-to-sqlite",
    description="Load email from .mbox files into SQLite",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/mbox-to-sqlite",
    project_urls={
        "Issues": "https://github.com/simonw/mbox-to-sqlite/issues",
        "CI": "https://github.com/simonw/mbox-to-sqlite/actions",
        "Changelog": "https://github.com/simonw/mbox-to-sqlite/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["mbox_to_sqlite"],
    entry_points="""
        [console_scripts]
        mbox-to-sqlite=mbox_to_sqlite.cli:cli
    """,
    install_requires=["click", "sqlite-utils"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
