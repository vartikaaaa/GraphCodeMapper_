import pathlib
import re
import ast

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('vartika/appear.py', 'rb') as f:
    _re_searched = _version_re.search(f.read().decode('utf-8'))

    if _re_searched is None:
        raise RuntimeError('Cannot find version string')

    VERSION = str(ast.literal_eval(_re_searched.group(1)))

# This call to setup() does all the work
setup(
    name="vartika-viz",
    version=VERSION,
    description="GRAPH CODE MAPPER",
    long_description=README,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],

    install_requires=[
        "wheel",
        "autopep8",
        "coloredlogs",
        "interrogate",
        "networkx",
        "scikit-learn",
        "numpy",
        "prettytable",
        "py",
        "pycodestyle",
        "pylint",
        "pyparsing",
        "python-louvain",
        "PyYAML",
        "tabulate",
        "PyDriller",
        "pyperclip"
    ],
    package_dir={
        "vartika": "vartika",
        "vartika/languages": "./vartika/languages",
        "vartika/metrics": "./vartika/metrics",
        "vartika/metrics/faninout": "./vartika/metrics/faninout",
        "vartika/metrics/modularity": "./vartika/metrics/modularity",
        "vartika/metrics/methodsnumber": "./vartika/metrics/methodsnumber",
        "vartika/metrics/sloc": "./vartika/metrics/sloc",
        "vartika/metrics/tfidf": ".vartika/metrics/tfidf",
        "vartika/metrics/whitespace": ".vartika/metrics/whitespace",
        "vartika/metrics/git": ".vartika/metrics/git"
    },
    packages=[
        'vartika',
        'vartika.languages',
        'vartika.metrics',
        'vartika.metrics.faninout',
        'vartika.metrics.modularity',
        'vartika.metrics.methodsnumber',
        'vartika.metrics.sloc',
        'vartika.metrics.tfidf',
        'vartika.metrics.whitespace',
        'vartika.metrics.git'
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "vartika = vartika.main:run"
        ]
    },
)
