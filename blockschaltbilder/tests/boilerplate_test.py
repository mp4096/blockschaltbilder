"""Test suit for the Blockschaltbild boilerplate generator."""


import unittest
from ..boilerplate import _convert_text


class TestBoilerplate(unittest.TestCase):
    def test_no_sketch(self):
        """Test if an exception is raised if the text contains is no sketch."""
        lines = [
            "spam",
            "",
            "",
            "eggs",
            ]
        self.assertRaises(ValueError, _convert_text, lines)

    def test_names(self):
        """Test the renaming of block IDs."""
        lines = [
            "                            ",
            "Skizze:                     ",
            "    C1  S1  S2  I1  I2  C2  ",
            "       PTZ1         P1      ",
            "     TZ2    PTE10       P2  ",
            "                            ",
            "       names:               ",  # test if the parser is
            "    PTZ1  :  pt 2 glied     ",  # robust enough
            "  TZ2 : totzeit             ",
            "    PTE10  :    pt eins     ",
            "                            ",
            "Namen:                      ",
            "    C1: eingang             ",
            "    C2: ausgang             ",
            "    S1: sum 1               ",
            "    S2: sum 2               ",
            "    I1: int 1               ",
            "    I2: int 2               ",
            "    P1: p 1                 ",
            "    P2: p 2                 ",
            ]

        bsb = _convert_text(lines)
        self.assertTrue(bsb._does_this_block_exist("pt 2 glied"))
        self.assertTrue(bsb._does_this_block_exist("totzeit"))
        self.assertTrue(bsb._does_this_block_exist("pt eins"))
        self.assertTrue(bsb._does_this_block_exist("eingang"))
        self.assertTrue(bsb._does_this_block_exist("ausgang"))
        self.assertTrue(bsb._does_this_block_exist("sum 1"))
        self.assertTrue(bsb._does_this_block_exist("sum 2"))
        self.assertTrue(bsb._does_this_block_exist("int 1"))
        self.assertTrue(bsb._does_this_block_exist("p 1"))
        self.assertTrue(bsb._does_this_block_exist("p 2"))
