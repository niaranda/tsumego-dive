import unittest

from src.preprocessing.corrections.sgf_corrections import apply_corrections
from src.preprocessing.errors.preprocessing_exception import PreprocessingException


class TestSgfCorrections(unittest.TestCase):

    def test_wrong_delimiters_fix(self):
        sgf = "(;SZ[19]FF[4]AB[br][cr][dr][er][eq][ep][eo][fo][go][ho][hp][dp]AW[bq][cq][dq][ar][co][dn][en][fn][gn][" \
              "hn][io][ip][jq][fp][gp][gq][fr]N[黑先活](N[正解];B[gr];W[hr];B[gs];W[hs];B[hq];W[fs];B[ir];W[iq];B[gr];W[" \
              "gs];B[es];W[jr];B[fq])) "
        expected = "(;SZ[19]FF[4]AB[br][cr][dr][er][eq][ep][eo][fo][go][ho][hp][dp]AW[bq][cq][dq][ar][co][dn][en][" \
                   "fn][gn][hn][io][ip][jq][fp][gp][gq][fr]N[黑先活](;N[正解];B[gr];W[hr];B[gs];W[hs];B[hq];W[fs];B[ir];W[" \
                   "iq];B[gr];W[gs];B[es];W[jr];B[fq])) "
        self.assertEqual(apply_corrections(sgf), expected)

    def test_multiple_stone_placing_check(self):
        sgf = "(;GM[1]SZ[19]AW[pq][dr][cr][er][dq][cp][bp][qo][ds][fs][cn]GN[ ]AB[dc][jq][ep][gr][gs][gp][dp][ce][" \
              "fr][cq][eq]PM[1];B[es];W[pd];B[fs];W[jc]C[Correct Answer]AB[pd] "
        with self.assertRaises(PreprocessingException):
            apply_corrections(sgf)

    def test_multiple_init_property_fix(self):
        sgf = "(;SZ[19]FF[4]AW[br][bq]AB[bp][bo][co]AW[cp][dp][ep]AB[cq][dq][er][fr][fs][gs]AW[gp][gq][gr][hs][ir]N[" \
              "黑先胜](;N[正解];B[ds];W[cr];B[dr];W[fq];B[aq];W[ar];B[cs];W[ap];B[bs];W[eq];B[ao])) "
        expected = "(;SZ[19]FF[4]AW[br][bq][cp][dp][ep][gp][gq][gr][hs][ir]AB[bp][bo][co][cq][dq][er][fr][fs][gs]N[" \
                   "黑先胜](;N[正解];B[ds];W[cr];B[dr];W[fq];B[aq];W[ar];B[cs];W[ap];B[bs];W[eq];B[ao])) "
        self.assertEqual(apply_corrections(sgf), expected)

    def test_empty_initial_board_check(self):
        sgf = "(;SZ[19]C[黑先];B[pe];W[pc];B[qc];W[qb];B[qd];W[ob];B[qi])"
        with self.assertRaises(PreprocessingException):
            apply_corrections(sgf)
