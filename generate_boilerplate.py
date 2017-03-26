import argparse
from blockschaltbilder import convert_to_tikz

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Convert *.bsb file(s) into boilerplate TikZ file(s).",
        )
    parser.add_argument(
        "paths", metavar="p", type=str, nargs='*', default=".",
        help="""specifies the location of files or folders to be converted
        (default: convert all in the current folder and it subfolders)""",
        )
    args = parser.parse_args()
    convert_to_tikz(args.paths)
