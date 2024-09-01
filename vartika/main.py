"""
Allow graphcodemapper to be importable by a start script (e.g. installed by pip) as a standalone tool.
"""

from vartika.appear import Graphcodemapper


def run():
    Graphcodemappers = Graphcodemapper()
    Graphcodemappers.start()


if __name__ == "__main__":
    run()
