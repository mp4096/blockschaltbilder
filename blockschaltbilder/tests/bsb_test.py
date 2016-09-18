import unittest
from ..bsb import Blockschaltbild, BlockschaltbildCoordinate, Block


"""Test suit for the Blockschaltbild boilerplate generator."""


class TestBlock(unittest.TestCase):
    def test_no_pars(self):
        """Test if a block is initialised correctly if no parameters are specified."""
        x, y = 3.14, 2.72
        b = Block("Spam", "eggs", (x, y), "1 cm")
        self.assertEqual(len(b.pars), 0)

    def test_some_pars(self):
        """Test if a block is initialised correctly if some parameters are specified."""
        x, y = 3.14, 2.72
        b = Block("Spam", "eggs", (x, y), "1 cm", ["par1", "par2"])
        self.assertEqual(b.pars, ["par1", "par2"])

    def test_auto_coord(self):
        """Test auto TikZ coordinate specification for a block."""
        x, y = 3.14, 2.72
        b = Block("Spam", "eggs", (x, y), "1 cm")
        self.assertEqual(b.get_tikz_coordinate("g"),
                         r"\coordinate (eggs--coord) at (3.14, 2.72);")

    def test_latex_def_no_pars(self):
        """Test LaTeX block definition if there are no parameters."""
        x, y = 3.14, 2.72
        b = Block("Spam", "eggs", (x, y), "1 cm")
        self.assertEqual(b.get_latex_definition(),
                         r"\Spam{eggs}{eggs--coord}{1 cm}")

    def test_latex_def_some_pars(self):
        """Test LaTeX block definition if there are some parameters."""
        x, y = 3.14, 2.72
        b = Block("Spam", "eggs", (x, y), "1 cm", ["par1", "par2"])
        self.assertEqual(b.get_latex_definition(),
                         r"\Spam{eggs}{eggs--coord}{1 cm}{par1}{par2}")


class TestBlockschaltbildCoordinate(unittest.TestCase):
    def test_auto_coord(self):
        """Test TikZ coordinate specification."""
        x, y = 3.14, 2.72
        c = BlockschaltbildCoordinate("eggs", (x, y))
        self.assertEqual(c.get_tikz_coordinate("g"),
                         r"\coordinate (eggs) at (3.14, 2.72);")

    def test_latex_def(self):
        """Test LaTeX definition -- must return None."""
        x, y = 3.14, 2.72
        c = BlockschaltbildCoordinate("eggs", (x, y))
        self.assertIsNone(c.get_latex_definition())


class TestBlockschaltbildBasics(unittest.TestCase):
    def test_add_block(self):
        """Test block addition."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        self.assertEqual(bsb.num_blocks, 2)
        self.assertEqual(bsb.get_block("block 1").xy, (0, 0))
        self.assertEqual(bsb.get_block("block 2").xy, (1, 0))

    def test_delete_existing_block(self):
        """Test deletion of an existing block."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        self.assertEqual(bsb.num_blocks, 2)
        bsb.delete_block("block 1")
        self.assertRaises(ValueError, bsb.get_block, "block 1")
        self.assertEqual(bsb.num_blocks, 1)
        bsb.delete_block("block 2")
        self.assertRaises(ValueError, bsb.get_block, "block 2")
        self.assertEqual(bsb.num_blocks, 0)

    def test_delete_nonexisting_block(self):
        """Test deletion of an non-existing block -- must raise exception."""
        bsb = Blockschaltbild()
        self.assertRaises(ValueError, bsb.delete_block, "spam")

    def test_rename_block(self):
        """Test renaming of an existing block."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        # "block 3" does not exist
        self.assertRaises(ValueError,
                          bsb.rename_block, "block 3", "spam")
        # "block 2" already exists
        self.assertRaises(ValueError,
                          bsb.rename_block, "block 1", "block 2")
        bsb.rename_block("block 1", "block A")
        self.assertRaises(ValueError, bsb.get_block, "block 1")
        self.assertEqual(bsb.num_blocks, 2)
        self.assertEqual(bsb.get_block("block A").xy, (0, 0))

    def test_add_connection(self):
        """Test addition of a connection."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        bsb.add_connection("block 1", "block 2")
        self.assertRaises(ValueError,
                          bsb.add_connection, "block A", "block 1")

    def test_delete_connection(self):
        """Test deletion of a connection."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        bsb.add_connection("block 1", "block 2")
        bsb.delete_connection("block 1", "block 2")
        self.assertRaises(ValueError,
                          bsb.delete_connection, "block 1", "block 2")

    def test_add_existing_connection(self):
        """Test addition of an already existing connection -- must raise exception."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        bsb.add_connection("block 1", "block 2")
        self.assertRaises(ValueError,
                          bsb.add_connection, "block 1", "block 2")

    def test_auto_joints(self):
        """Test auto joints placement."""
        bsb = Blockschaltbild()
        bsb.add_block("PGlied", "block 1", (0, 0))
        bsb.add_block("IGlied", "block 2", (1, 0))
        bsb.add_block("IGlied", "block 3", (1, 1))
        bsb.add_connection("block 1", "block 2")
        bsb.add_connection("block 1", "block 3")
        bsb.add_auto_joints()
        self.assertEqual(bsb.num_blocks, 4)
        self.assertEqual(bsb.get_block("ajnt1").block_type, "Verzweigung")

    def test_import_sketch(self):
        """Test import of a sketch."""
        bsb = Blockschaltbild()
        sketch = """

            I1    P1
            PTE1 PTZ1

              D31415


        """
        bsb.import_sketch(sketch.splitlines())
        self.assertEqual(bsb.num_blocks, 5)
        self.assertEqual(bsb.get_block("I1").block_type, "IGlied")
        self.assertEqual(bsb.get_block("P1").block_type, "PGlied")
        self.assertEqual(bsb.get_block("PTE1").block_type, "PTEinsGlied")
        self.assertEqual(bsb.get_block("PTZ1").block_type, "PTZweiGlied")
        self.assertEqual(bsb.get_block("D31415").block_type, "DGlied")

    def test_import_invalid_sketch(self):
        """Test import of an invalid sketch -- must raise exception."""
        bsb = Blockschaltbild()
        sketch = ["I1 I1",]
        self.assertRaises(ValueError, bsb.import_sketch, sketch)

    def test_import_names(self):
        """Test import of names."""
        bsb = Blockschaltbild()
        sketch = ["P1 I1", "D1 C1"]
        bsb.import_sketch(sketch)
        names = ["P1: spam", "I1  :  eggs"]
        bsb.import_names(names)
        self.assertEqual(bsb.num_blocks, 4)
        self.assertEqual(bsb.get_block("spam").block_type, "PGlied")
        self.assertEqual(bsb.get_block("eggs").block_type, "IGlied")

    def test_import_invalid_names(self):
        """Test import of a invalid names -- must raise exception."""
        bsb = Blockschaltbild()
        names = ["P1: spam", "I1: eggs"]
        self.assertRaises(ValueError, bsb.import_names, names)

    def test_import_connections(self):
        """Test import of connections."""
        bsb = Blockschaltbild()
        sketch = ["P1 I1", "D1 C1"]
        bsb.import_sketch(sketch)
        conns = ["P1 - I1", "I1 - D1", "D1 = C1"]
        bsb.import_connections(conns)
        self.assertRaises(ValueError,
                          bsb.add_connection, "P1", "I1")
        self.assertRaises(ValueError,
                          bsb.add_connection, "I1", "D1")
        self.assertRaises(ValueError,
                          bsb.add_connection, "D1", "C1")

    def test_import_invalid_connections(self):
        """Test import of an invalid connections -- must raise exception."""
        bsb = Blockschaltbild()
        conns = ["P1 - I1",]
        self.assertRaises(ValueError, bsb.import_connections, conns)
