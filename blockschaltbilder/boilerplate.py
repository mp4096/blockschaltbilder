from .bsb import Blockschaltbild
import codecs
import fnmatch
import os
import re
import yaml


"""Frontend file parser for Blockschaltbilder."""


# Specify exports
__all__ = ["convert_to_tikz"]

# Specify German-English equivalents for keys
_GERMAN_KEYS_TO_ENGLISH = {
    "skizze": "sketch",
    "verbindungen": "connections",
    "namen": "names",
    }


def _convert_single_file(filename):
    """Convert a single file to a *.tex file.

    Parameters
    ----------
    filename : str
        Path to the file to be converted.

    """

    # Check file extension
    if not fnmatch.fnmatch(filename, '*.bsb'):
        raise ValueError("The input file must have a 'bsb' extension")

    # Create an empty list for the modified contents of the file
    modified_lines = []
    # Open the file and save its modified contents line by line
    with codecs.open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            # Replace hard tabs with soft tabs
            line = line.replace("\t", " "*4).rstrip()
            # Specify chomping indent of 1 for all multiline string literals
            # This is required for parsing sketches correctly
            modified_lines.append(re.sub(r":\s*\|$", r": |1", line))
    # Create an empty block diagram and a dictionary for the contents of the file
    bsb = Blockschaltbild()
    contents = {}
    # Iterate through the modified lines
    for key, value in yaml.load("\n".join(modified_lines)).items():
        # Transform German keys into English analogues
        if key.lower() in _GERMAN_KEYS_TO_ENGLISH:
            normalised_key = _GERMAN_KEYS_TO_ENGLISH[key.lower()]
        else:
            normalised_key = key.lower()
        # Add the contents to the dict
        contents[normalised_key] = value

    # Import sketch; note that it is mandatory since it defines the blocks
    bsb.import_sketch(contents["sketch"].splitlines())
    # If the connections are specified, import them
    if "connections" in contents:
        bsb.import_connections(contents["connections"].splitlines())
    # If new names are specified, rename blocks
    if "names" in contents:
        bsb.import_names(contents["names"].splitlines())
    # Add auto joints instead of blocks with multiple outgoing connections
    bsb.add_auto_joints()
    # Export to a *.tex file
    bsb.export_to_file(re.sub(r"\.bsb$", ".tex", filename))


def _find_bsb_files(root_directory):
    """Walk recursively through subfolders and yield *.bsb files

    Parameters
    ----------
    root_directory : str
        Root directory to look in.

    Returns
    -------
    str
        Full filename to a *.bsb file.

    """
    for root, dirs, files in os.walk(root_directory):
        for basename in files:
            if fnmatch.fnmatch(basename, '*.bsb'):
                filename = os.path.join(root, basename)
                yield filename


def convert_to_tikz(paths):
    """Convert *.bsb file(s) into boilerplate TikZ file(s).

    Parameters
    ----------
    paths : list of str
        File or folder specification. If a 'path' element is a file, only it is converted;
        if it is a folder, all '*.bsb' files in it and its subfolders will be converted.

    """
    for p in paths:
        if os.path.isdir(p):
            for file in _find_bsb_files(p):
                _convert_single_file(file)
        elif os.path.isfile(p):
            _convert_single_file(p)
        else:
            raise ValueError("File or folder '{:s}' not found.".format(p))
