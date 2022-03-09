import unittest
from typing import Dict

import sgf

from src.preprocessing.corrections.tree_adapter_corrections import correct_only_comment_first_node


class TestTreeAdapterCorrections(unittest.TestCase):

    def test_only_comment_first_node_fix(self):
        sgf_str = "(;SZ[19]FF[4]AW[rb][rc][qd][re][qf][pf][pc][oc][nc][md][me][le][kf][jf][je][kb][jb][ic]AB[pg][of][" \
                  "nf][mf][lf][ld][kd][ke][kc][qc][qb][pb][ob][nb][mb][lb](;N[Correct];B[pd];W[od];B[mc];W[pe];B[" \
                  "nd]C[Correct])) "
        problem: sgf.GameTree = sgf.parse(sgf_str)[0]
        first_node = problem.children[0]
        self.assertEqual(len(first_node.nodes), 6)

        correct_only_comment_first_node(problem)
        self.assertEqual(len(first_node.nodes), 5)

        properties: Dict[str, str] = first_node.nodes[0].properties
        self.assertFalse("N" in properties)
