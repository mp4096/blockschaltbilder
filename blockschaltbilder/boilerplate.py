"""Frontend file parser for Blockschaltbilder."""


from .bsb import Blockschaltbild
import fnmatch
import os
import re


# Specify exports
__all__ = ["convert_to_tikz"]

# Define regexen for the detection of file sections
_PATTERN_SKETCH = r"(?:sketch|skizze)\:$"
_RE_SKETCH = re.compile(_PATTERN_SKETCH, re.IGNORECASE)
_PATTERN_CONNECTIONS = r"(?:connections|verbindungen)\:$"
_RE_CONNECTIONS = re.compile(_PATTERN_CONNECTIONS, re.IGNORECASE)
_PATTERN_NAMES = r"(?:names|namen)\:$"
_RE_NAMES = re.compile(_PATTERN_NAMES, re.IGNORECASE)


# We use a state machine to parse the *.bsb files
class Reader:
    """State machine for reading *.bsb files."""

    def __init__(self):
        """Create a new reader state machine."""
        # Initialise with inactive state
        self.transit_to(Inactive)

        # Initialise accumulator lists
        self.sketch = []
        self.connections = []
        self.names = []

    def transit_to(self, new_state):
        """Transit to new state."""
        self._state = new_state

    def read_line(self, line):
        """Read one line.

        This method reads one line and decides what to do:
        Depending on the line contents, it either performs a transition to
        new state (file section) or stores the line in the appropriate
        state-dependent accumulator list.

        Parameters
        ----------
        line : str
            One line of a *.bsb file.

        """
        # We strip the line only for tag matching; the original line is
        # stored in accumulator lists in order to preserve indentation.
        stripped_line = line.strip()

        # Try to match section tags and transit to the corresponding state;
        # otherwise just chomp this line.
        if _RE_SKETCH.match(stripped_line) is not None:
            self.transit_to(Sketch)
        elif _RE_CONNECTIONS.match(stripped_line) is not None:
            self.transit_to(Connections)
        elif _RE_NAMES.match(stripped_line) is not None:
            self.transit_to(Names)
        else:
            self._store(line)

    def _store(self, line):
        """Store a line in an appropriate accumulator list.

        Delegates this to the state's static method.

        Parameters
        ----------
        line : str
            One line of a *.bsb file.

        """
        return self._state.store_line(self, line)


# Classes representing reader's states; self-explanatory
class ReaderState:
    """Parent class for reader state."""

    @staticmethod
    def store_line(reader, line):
        raise NotImplementedError()


class Inactive(ReaderState):
    @staticmethod
    def store_line(reader, line):
        pass


class Sketch(ReaderState):
    @staticmethod
    def store_line(reader, line):
        reader.sketch.append(line)


class Connections(ReaderState):
    @staticmethod
    def store_line(reader, line):
        reader.connections.append(line)


class Names(ReaderState):
    @staticmethod
    def store_line(reader, line):
        reader.names.append(line)


def _convert_text(lines):
    """Create a Blockschaltbild from text.

    Parameters
    ----------
    lines : list of str
        Text lines with the Blockschaltbild specification.

    Returns
    -------
    Blockschaltbild
        A block diagram created from text.

    """
    # Set current status to inactive
    reader = Reader()

    # Read the text line by line, replacing hard tabs with 4 whitespaces
    for l in lines:
        reader.read_line(l.replace("\t", " "*4))

    # Create an empty block diagram
    bsb = Blockschaltbild()
    # Import sketch; note that it is mandatory since it defines the blocks
    if reader.sketch:
        bsb.import_sketch(reader.sketch)
    else:
        raise ValueError("The input file must contain a sketch")
    # If the connections are specified, import them
    if reader.connections:
        bsb.import_connections(reader.connections)
    # If new names are specified, rename blocks
    if reader.names:
        bsb.import_names(reader.names)

    # Add auto joints instead of blocks with multiple outgoing connections
    bsb.add_auto_joints()

    return bsb


def _convert_single_file(filename):
    """Convert a single .bsb file into a boilerplate .tex file.

    Parameters
    ----------
    filename : str
        Path to the file to be converted.

    """
    # Check file extension
    if not fnmatch.fnmatch(filename, '*.bsb'):
        raise ValueError("The input file must have a 'bsb' extension")

    # Open this file and read all its contents into a list
    with open(filename, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    # Convert them into a Blockschaltbild with automatically placed joints
    bsb = _convert_text(lines)

    # Export to a *.tex file
    bsb.export_to_file(re.sub(r"\.bsb$", ".tex", filename))


def _find_bsb_files(root_directory):
    """Walk recursively through subfolders and yield *.bsb files.

    Parameters
    ----------
    root_directory : str
        Root directory to look in.

    Returns
    -------
    str
        Full filename to a *.bsb file.

    """
    for root, _, files in os.walk(root_directory):
        for basename in fnmatch.filter(files, "*.bsb"):
            yield os.path.join(root, basename)


def convert_to_tikz(paths):
    """Convert *.bsb file(s) into boilerplate TikZ file(s).

    Parameters
    ----------
    paths : list of str
        File or folder specification.
        If a 'path' element is a file, only it is converted;
        if it is a folder, all '*.bsb' files in it and its subfolders
        will be converted.

    """
    for p in paths:
        if os.path.isdir(p):
            for file in _find_bsb_files(p):
                try:
                    _convert_single_file(file)
                except ValueError as e:
                    print("ValueError in {:s}:".format(file), e)
                except TypeError as e:
                    print("TypeError in {:s}:".format(file), e)
        elif os.path.isfile(p):
            _convert_single_file(p)
        else:
            raise ValueError("File or folder '{:s}' not found.".format(p))
