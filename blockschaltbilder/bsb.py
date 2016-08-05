from abc import ABCMeta, abstractmethod
import codecs
import numpy as np
import re

"""This module contains the Blockschaltbild class."""

# Export only the Blockschaltbild class
__all__ = ["Blockschaltbild"]

# Constant IDs for scalar-typed and vector-typed connections
# Please do not modify these!
# And in case you do, these must be unique, positive, int numbers
_SCALAR_EDGE = 1
_VECTOR_EDGE = 2

# Const dict specifying how many additional parameters are required by each block type
_BLOCKS_NUM_PARS = {
    "coordinate": 0,
    "Summationsstelle": 0,
    "Verzweigung": 0,
    "PGlied": 1,
    "IGlied": 1,
    "DGlied": 1,
    "PTEinsGlied": 2,
    "PTZweiGlied": 2,
    "TZGlied": 2,
    "UeFunk": 1,
    "MGlied": 1,
    "KLGlied": 3,
    "Saettigung": 2,
    }

# Const dict for 'translation' of short IDs into the full-fledged block types
# Required for import from ASCII graphics-like sketches
_SHORT_ID_TO_BLOCK_TYPES = {
    "c": "coordinate",
    "s": "Summationsstelle",
    "v": "Verzweigung",
    "p": "PGlied",
    "i": "IGlied",
    "d": "DGlied",
    "pte": "PTEinsGlied",
    "ptz": "PTZweiGlied",
    "tz": "TZGlied",
    "u": "UeFunk",
    "m": "MGlied",
    "kl": "KLGlied",
    "sat": "Saettigung",
    }

# Prepare OR-ed short IDs to be used later in regexen
_ALL_SHORT_IDS = "|".join(_SHORT_ID_TO_BLOCK_TYPES.keys())

# Pattern and regex for matching blocks in sketches
_PATTERN_IMPORT_SKETCH = r"""
(?P<b_id>{all_short_ids:s})  # Capture the short ID...
(?P<b_num>\d+)               # and at least one digit or more
""".format(all_short_ids=_ALL_SHORT_IDS)
_RE_IMPORT_SKETCH = re.compile(_PATTERN_IMPORT_SKETCH, re.VERBOSE | re.IGNORECASE)

# Pattern and regex for matching connections specifications
_PATTERN_IMPORT_CONNECTION = r"""
(?P<from_id>{all_short_ids:s}) # Capture the short ID of the 'from'-block...
(?P<from_num>\d+)              # and at least one digit or more.
                               #
\s*?                           # Here can be some whitespaces.
                               #
(?P<line_type>-|=)             # Capture the line type. It can be '-' for scalar and '=' for vector
                               #
\s*?                           # Here can be some whitespaces.
                               #
(?P<to_id>{all_short_ids:s})   # Capture the short ID of the 'to'-block...
(?P<to_num>\d+)                # and at least one digit or more.
""".format(all_short_ids=_ALL_SHORT_IDS)
_RE_IMPORT_CONNECTION = re.compile(_PATTERN_IMPORT_CONNECTION, re.VERBOSE | re.IGNORECASE)

# Pattern and regex for matching renaming specifications
_PATTERN_IMPORT_RENAME = r"""
(?P<old_id>{all_short_ids:s}) # Capture the short ID of the block to be renamed...
(?P<old_num>\d+)              # and at least one digit or more.
                              #
\s*?                          # Here can be some whitespaces.
                              #
\:                            # Capture a literal colon.
                              #
(?P<new_name>.*)$             # Capture the rest of the line.
""".format(all_short_ids=_ALL_SHORT_IDS)
_RE_IMPORT_RENAME = re.compile(_PATTERN_IMPORT_RENAME, re.VERBOSE | re.IGNORECASE)


def _write_a_tikz_coordinate(name, xy, num_fmt):
    """Writes a TikZ coordinate definition.

    Parameters
    ----------
    name : str
        TikZ coordinate identified / name.
    xy : list or tuple of floats
        (x, y)-coordinates.
    num_fmt : str
        Specification of the numbers format, e.g. '.4f'.


    Returns
    -------
    str
        TikZ coordinate definition without newline char.

    """

    fmt_str = "{:" + num_fmt + "}"

    tex_str = "\\coordinate ({:s})".format(name)
    tex_str += " at ("
    tex_str += ", ".join(map(fmt_str.format, xy))
    tex_str += ");"

    return tex_str


class AbstractBlock(metaclass=ABCMeta):
    """Class for an abstract block."""

    @abstractmethod
    def get_tikz_coordinate(self, num_fmt):
        pass

    @abstractmethod
    def get_latex_definition(self):
        pass


class Block(AbstractBlock):
    """Blockschaltbild block class."""

    def __init__(self, block_type, name, xy, size, pars=None):
        """Creates a new block.

        Parameters
        ----------
        block_type : str
            Block type specification.
        name : str
            Block name.
        xy : list or tuple of floats
            Block (x, y)-coordinates.
        size : str
            Block size (including units!).
        pars : list or tuple or None, optional
            Additional parameters for the block.

        """

        #: str: Block type specification
        self.block_type = block_type
        #: str: Block name
        self.name = name
        #: list or tuple of floats: Block (x, y)-coordinates
        self.xy = xy
        #: str: Block size (including units!)
        self.size = size
        #: list or tuple or None: Additional parameters for the block
        if pars is None:
            self.pars = []
        else:
            self.pars = pars

    def get_tikz_coordinate(self, num_fmt):
        """Get a str with a TikZ coordinate definition for the block.

        The coordinate's name is the block's name extended with a "--coord" suffix.

        Parameters
        ----------
        num_fmt : str
            Specification of the numbers format.

        Returns
        -------
        str
            TikZ coordinate definition for the block.

        """
        return _write_a_tikz_coordinate(self.name + "--coord", self.xy, num_fmt)

    def get_latex_definition(self):
        """Get LaTeX definition of the block.

        Returns
        -------
        str
            LaTeX command with the block definition.

        """

        tex_str = "\\"
        # Write block type
        tex_str += self.block_type
        # Write block node name
        tex_str += "{" + self.name + "}"
        # Write block coordinate's node
        tex_str += "{" + self.name + "--coord}"
        # Write block size
        tex_str += "{" + self.size + "}"
        # Write parameters only if there are any
        if self.pars:
            tex_str += "{" + "}{".join(self.pars) + "}"
        # Return LaTeX str
        return tex_str


class BlockschaltbildCoordinate(AbstractBlock):
    """Blockschaltbild coordinate class."""

    def __init__(self, name, xy):
        """Creates a new coordinate.

        Parameters
        ----------
        name : str
            Coordinate name.
        xy : list or tuple of floats
            Coordinate (x, y)-location.

        """

        #: str: Coordinate name
        self.name = name
        #: str: Block type, constant
        self.block_type = "coordinate"
        #: list or tuple of floats: Block (x, y)-coordinates
        self.xy = xy

    def get_tikz_coordinate(self, num_fmt):
        """Get a str with a TikZ coordinate definition.

        Parameters
        ----------
        num_fmt : str
            Specification of the numbers format.

        Returns
        -------
        str
            TikZ coordinate definition.

        """
        return _write_a_tikz_coordinate(self.name, self.xy, num_fmt)

    def get_latex_definition(self):
        """Implements the superclass method.

        Returns
        -------
        None
            Always returns None.

        """
        return None


class Blockschaltbild:
    """Class for block diagrams."""

    def __init__(self, x_scale=0.5, y_scale=1.5,
                 block_sizes=None, scalar_style=None, vector_style=None, arrow_style=None):
        """Create a Blockschaltbild object.

        Parameters
        ----------
        x_scale : float, optional
            Default x-axis scale in cm.
        y_scale : float, optional
            Default y-axis scale in cm. It should be larger than the x-scale (2x..3x).
        block_sizes : dict, optional
            Default block sizes.
        scalar_style : str, optional
            Style of scalar-valued connections.
        vector_style : str, optional
            Style of vector-valued connections.
        arrow_style : str, optional
            Style of the arrow tips.

        """

        # Store scale information
        self.x_scale = x_scale
        self.y_scale = y_scale

        # Create an empty list for blocks and coordinates
        self._blocks = []

        # Create an empty adjacency matrix
        self._adj_mat = np.zeros((0, 0), dtype=np.int)

        # Create a default block sizes dict if none is given
        if block_sizes is None:
            self.block_sizes = {
                "coordinate": None,
                "Summationsstelle": "0.4 cm",
                "Verzweigung": "2 pt",
                "PGlied": "1 cm",
                "IGlied": "1 cm",
                "DGlied": "1 cm",
                "PTEinsGlied": "1 cm",
                "PTZweiGlied": "1 cm",
                "TZGlied": "1 cm",
                "UeFunk": "1 cm",
                "MGlied": "1 cm",
                "KLGlied": "1 cm",
                "Saettigung": "1 cm",
                }
        else:
            self.block_sizes = block_sizes

        # Create a default scalar style if none is given
        if scalar_style is None:
            self.scalar_style = "thick"
        else:
            self.scalar_style = scalar_style

        # Create a default vector style if none is given
        if vector_style is None:
            self.vector_style = "very thick"
        else:
            self.vector_style = vector_style

        # Create a default arrow style if none is given
        if arrow_style is None:
            self.arrow_style = "-latex"
        else:
            self.arrow_style = arrow_style

        # Initialise a counter for automatically placed joints
        self._auto_joints_counter = 0

    @property
    def num_blocks(self):
        """int: Number of blocks in the Blockschaltbild."""
        return len(self._blocks)

    def _does_this_block_exist(self, block_name):
        """ Check if a block exists.

        Parameters
        ----------
        block_name: str
            Query string for the block name.

        Returns
        -------
        bool
            True if the block with name 'block_name' exists.

        """
        return any(b.name == block_name for b in self._blocks)

    def _get_block_idx_by_name(self, block_name):
        """ Search for a block, return its index or raise an exception if not found.

        Parameters
        ----------
        block_name: str
            Query string for the block name.

        Returns
        -------
        int
            Block index.

        """

        idx = next((idx for idx, b in enumerate(self._blocks) if b.name == block_name), None)

        if idx is None:
            raise ValueError("Block '{:s}' not found!".format(block_name))

        return idx

    def _get_sorted_blocks(self):
        """Get a list of sorted blocks.

        Blocks (and coordinates) are sorted by the x-position in ascending order,
        i.e. from left to right.

        Returns
        -------
        list of Block or BlockschaltbildCoordinate
            List of sorted blocks.

        """
        return sorted(self._blocks, key=lambda b: b.xy[0])

    def _get_sorted_connections_list(self):
        """Get a sorted list of connections.

        Connections are the edges between blocks (nodes).
        They are sorted by the x-coordinate of the 'from'-block,
        i.e. from left to right.

        Returns
        -------
        list of tuples
            List with connections; they are specified by a 3-tuple:
            * Name of the 'from'-block
            * Name of the 'to'-block
            * String with the TikZ style specification

        """

        # Get edges, i.e. non-zero entries of the adjacency matrix
        # However, 'np.nonzero' returns a tuple of lists; we want a list of tuples:
        edges = list(zip(*np.nonzero(self._adj_mat)))
        # Sort the edges by the x-coordinate of the 'from'-block
        edges.sort(key=lambda idx: self._blocks[idx[0]].xy[0])

        # Create an empty list of connections
        connections = []

        for idx_from, idx_to in edges:
            style_str = ""

            # Decide which line style to use
            if self._adj_mat[idx_from, idx_to] == _SCALAR_EDGE:
                style_str += self.scalar_style
            elif self._adj_mat[idx_from, idx_to] == _VECTOR_EDGE:
                style_str += self.vector_style

            # Add an arrow tip if we're not going to a joint
            if self._blocks[idx_to].block_type != "Verzweigung":
                style_str += ", " + self.arrow_style

            # Create and append a connection
            c = (self._blocks[idx_from].name, self._blocks[idx_to].name, style_str)
            connections.append(c)

        return connections

    def add_block(self, block_type, name, xy, size=None, pars=None):
        """ Add a block or a coordinate

        Parameters
        ----------
        block_type : str
            Block type specification.
        name : str
            Block name.
        xy : list or tuple of floats
            Block (x, y)-coordinates.
        size : str or None, optional
            Block size (including units!).
        pars : list or tuple or None, optional
            Additional parameters for the block.

        """

        # Raise an exception if a block with this name already exists
        if self._does_this_block_exist(name):
            raise ValueError("Block '{:s}' already exists!".format(name))

        # Create default values for block size and parameters if none are given
        if size is None:
            size = self.block_sizes[block_type]
        if pars is None:
            pars = ["" for _ in range(_BLOCKS_NUM_PARS[block_type])]

        # Call a Block or a BlockschaltbildCoordinate constructor
        # depending on 'block_type'
        if block_type == "coordinate":
            b = BlockschaltbildCoordinate(name, xy)
        else:
            b = Block(block_type, name, xy, size, pars)

        # Add the new block to the list
        self._blocks.append(b)

        # Extend the adjacency matrix with a row and a column
        # Do not use 'np.pad' here! It does not function for empty matrices.
        temp_mat = self._adj_mat
        new_num_blocks = self.num_blocks
        self._adj_mat = np.zeros((new_num_blocks, new_num_blocks), dtype=np.int)
        self._adj_mat[:-1, :-1] = temp_mat

    def get_block(self, block_name):
        """ Get a handle to a block.

        Parameters
        ----------
        block_name: str
            Query string for the block name.

        Returns
        -------
        Block or BlockschaltbildCoordinate
            Block or coordinate object.

        """
        return self._blocks[self._get_block_idx_by_name(block_name)]

    def delete_block(self, block_name):
        """Delete a block.

        Parameters
        ----------
        block_name : str
            Name of the block to delete.

        """

        idx_to_delete = self._get_block_idx_by_name(block_name)

        # Delete the block from the list
        del self._blocks[idx_to_delete]

        # Delete the corresponding row and column from the adjacency matrix
        self._adj_mat = np.delete(self._adj_mat, idx_to_delete, 0)
        self._adj_mat = np.delete(self._adj_mat, idx_to_delete, 1)

    def rename_block(self, old_name, new_name):
        """Rename a block.

        Parameters
        ----------
        old_name : str
            Name of the block to rename.
        new_name : str
            New block name.

        """

        # Raise an exception if a block with the new name already exists
        if self._does_this_block_exist(new_name):
            raise ValueError("Block '{:s}' already exists!".format(new_name))

        idx_to_rename = self._get_block_idx_by_name(old_name)

        self._blocks[idx_to_rename].name = new_name

    def add_connection(self, from_block_name, to_block_name, is_vector=False):
        """Add a connection between two blocks.

        Parameters
        ----------
        from_block_name: str
            Name of the 'from'-block.
        to_block_name: str
            Name of the 'to'-block.
        is_vector: bool, optional
            True if the connection is vector-valued, False if scalar.

        """

        # Get block indices
        from_idx = self._get_block_idx_by_name(from_block_name)
        to_idx = self._get_block_idx_by_name(to_block_name)

        # Check if this connection already exists
        if self._adj_mat[from_idx, to_idx] != 0:
            msg = "Blocks "
            msg += "'" + self._blocks[from_idx].name + "'"
            msg += " and "
            msg += "'" + self._blocks[to_idx].name + "'"
            msg += " are already connected!"
            raise ValueError(msg)

        # Add an entry into the adjacency matrix
        if is_vector:
            edge_type = _VECTOR_EDGE
        else:
            edge_type = _SCALAR_EDGE

        self._adj_mat[from_idx, to_idx] = edge_type

    def delete_connection(self, from_block_name, to_block_name):
        """Delete a connection between two blocks.

        Parameters
        ----------
        from_block_name: str
            Name of the 'from'-block.
        to_block_name: str
            Name of the 'to'-block.

        """

        # Get block indices
        from_idx = self._get_block_idx_by_name(from_block_name)
        to_idx = self._get_block_idx_by_name(to_block_name)

        # Check if this connection exists
        if self._adj_mat[from_idx, to_idx] == 0:
            msg = "No connection between blocks "
            msg += "'" + self._blocks[from_idx].name + "'"
            msg += " and "
            msg += "'" + self._blocks[to_idx].name + "'"
            raise ValueError(msg)

        self._adj_mat[from_idx, to_idx] = 0

    def add_auto_joints(self):
        """Add joints automatically.

        A joint is added for each block that is not a joint
        and has multiple connections going out of it.

        """

        def add_a_single_joint(old_idx, joint_name, xy):
            """Add a single default joint to the Blockschaltbild.

            Parameters
            ----------
            old_idx: int
                Index of the block with multiple outgoing connections.
            joint_name: str
                Name of the new joint.
            xy: list or tuple of floats
                (x, y)-coordinates of the new joint.
            """

            # Use default joint size
            self.add_block("Verzweigung", joint_name, xy, self.block_sizes["Verzweigung"])
            # The last row corresponds to the new joint;
            # copy the old row (= old outgoing connections) to the joint
            self._adj_mat[-1, :] = self._adj_mat[old_idx, :]
            # Remove all outgoing connections from the old block
            self._adj_mat[old_idx, :] = 0
            # Add a single connection to the freshly created joint
            # I don't want to implement fancy smart scalar/vector detection here
            self._adj_mat[old_idx, -1] = _SCALAR_EDGE

        # Now we have to go through the adjacency matrix and
        # add an auto joint for each row with multiple outgoing connections.
        #
        # The problem is, The adjacency matrix grows with each operations.
        # Hence, we will use an infinite while loop. In each iteration,
        # we check if there are rows with multiple outgoing connections.
        # If yes, a joint is added instead of the _first_ row and the iteration
        # is repeated. If no, we break out of the while loop.
        while True:
            # First, for each row check if it has multiple outgoing connections
            has_multiple_connections = np.sum(self._adj_mat, axis=1) > _SCALAR_EDGE
            # Second, for each row check if it corresponds to a non-joint block
            is_not_a_joint = [b.block_type != "Verzweigung" for b in self._blocks]
            # Now make an element-wise AND of these two lists
            # The second operand (plain list) will be converted to an np.array automatically
            is_relevant = has_multiple_connections & is_not_a_joint
            # Make a list of indices corresponding to non-joint blocks
            # with multiple outgoing connections
            idx_relevant = [idx for idx, cond in enumerate(is_relevant) if cond]

            # If the list is not empty, ...
            if idx_relevant:
                # Increase the counter of automatic joints
                self._auto_joints_counter += 1
                # Create a name for the auto joint
                ajnt_name = "ajnt{:d}".format(self._auto_joints_counter)
                # Place it near the 'from'-block, shifted by 20% to the right
                from_block = self._blocks[idx_relevant[0]]
                ajnt_xy = (1.2 * from_block.xy[0], from_block.xy[1])
                # Add this joint to the Blockschaltbild
                add_a_single_joint(idx_relevant[0], ajnt_name, ajnt_xy)
            else:
                # If the list is empty, we're done, break the loop
                break

    def import_sketch(self, sketch):
        """Import blocks from an ASCII graphics-like sketch.

        Parameters
        ----------
        sketch : list of str
            ASCII graphics-like sketch, line by line.

        """

        # Delete all empty lines at the bottom of the sketch
        while not sketch[-1].strip():
            sketch.pop()
        # Reverse the list; we shall process the sketch lines upwards
        sketch.reverse()
        # Delete all empty lines at the top of the sketch
        while not sketch[-1].strip():
            sketch.pop()

        # Loop through lines
        # We need the line number in order to get the y-coordinate of the block
        for line_number, line in enumerate(sketch):
            # The y-coordinate is the same for the whole line
            y = line_number*self.y_scale

            # Get everything that matches to the block short ID pattern
            for m in _RE_IMPORT_SKETCH.finditer(line):
                # The x-coordinate is the mean of the match beginning and end positions
                x = self.x_scale*np.mean(m.span())
                # The block name is simply its short ID plus its number
                block_name = m.group("b_id") + m.group("b_num")
                # Get the block type from our conversion dictionary
                block_type = _SHORT_ID_TO_BLOCK_TYPES[m.group(1).lower()]
                # Add the block to the Blockschaltbild
                # 'size' and 'pars' are handled by the 'add_block()' method
                self.add_block(block_type, block_name, (x, y))

    def import_connections(self, connections):
        """Import connections between blocks.

        Parameters
        ----------
        connections : list of str
            Lines with connection specifications.

        """
        # Iterate through lines
        for line in connections:
            # Try to match the connection pattern once
            m = _RE_IMPORT_CONNECTION.search(line)
            if m is not None:
                # If found something, get the names of the 'from'- and 'to'-blocks
                b_from = m.group("from_id") + m.group("from_num")
                b_to = m.group("to_id") + m.group("to_num")
                # Distinguish between scalar and vector connections
                if m.group("line_type") == "=":
                    vector = True
                else:
                    vector = False
                # Add the connection to our block diagram object
                self.add_connection(b_from, b_to, vector)

    def import_names(self, new_names):
        """Import meaningful names of blocks instead of short IDs.

        Parameters
        ----------
        new_names : list of str
            Lines with renaming specifications.

        """
        # Iterate through lines
        for line in new_names:
            # Try to match the rename pattern once
            m = _RE_IMPORT_RENAME.search(line.strip())
            if m is not None:
                # If found something, get the name of the block to be renamed
                old_name = m.group("old_id") + m.group("old_num")
                # Remove some special characters from the new block name and strip the whitespaces
                new_name = re.sub(r"[~!@#$%^&*()/\\,.;']", " ", m.group("new_name")).strip()
                # Rename the block
                self.rename_block(old_name, new_name)

    def export_to_file(self, filename, num_fmt="g"):
        """Export the Blockschaltbild to a TikZ file.

        Parameters
        ----------
        filename : str
            Target filename; relative or absolute path.

        num_fmt : str, optional
            Specification of the numbers format, e.g. '.4f'.

        """

        with codecs.open(filename, 'w', encoding="utf-8") as f:
            # Place the opening tag
            f.write(r"\begin{tikzpicture}")
            f.write("\n\n\n")

            # Export coordinates
            f.write(r"% <coordinates>")
            f.write("\n")
            for b in self._get_sorted_blocks():
                f.write(b.get_tikz_coordinate(num_fmt))
                f.write("\n")
            f.write(r"% </coordinates>")
            f.write("\n\n\n")

            # Export block definitions
            f.write(r"% <blocks>")
            f.write("\n")
            for b in self._get_sorted_blocks():
                if b.get_latex_definition() is not None:
                    f.write(b.get_latex_definition())
                    f.write("\n")
            f.write(r"% </blocks>")
            f.write("\n\n\n")

            # Export connections
            f.write(r"% <connections>")
            f.write("\n")
            for from_block, to_block, style in self._get_sorted_connections_list():
                f.write("\\draw[{:s}] ({:s}) -- ({:s});".format(style, from_block, to_block))
                f.write("\n")
            f.write(r"% </connections>")
            f.write("\n\n\n")

            # Place the closing tag
            f.write(r"\end{tikzpicture}")
            f.write("\n")
