from AAGTree import AAGTree
#
#
# aag = AAGTree('../aag/and.aag')
# aag.circuit.print()
# print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 0, 'i1': 0}, 'o0'))
# print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 1, 'i1': 0}, 'o0'))
# print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 0, 'i1': 1}, 'o0'))
# print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 1, 'i1': 1}, 'o0'))
#
# aag = AAGTree('../aag/latch.aag')
# aag.circuit.print()
# print(aag.shap_scores(['lp0'], {'lp0': 0}, 'o0'))
# print(aag.shap_scores(['lp0'], {'lp0': 0}, 'o1'))
# print(aag.shap_scores(['lp0'], {'lp0': 0}, 'ln0'))
# print(aag.shap_scores(['lp0'], {'lp0': 1}, 'o0'))
# print(aag.shap_scores(['lp0'], {'lp0': 1}, 'o1'))
# print(aag.shap_scores(['lp0'], {'lp0': 1}, 'ln0'))
#
#
# aag = AAGTree('../aag/half_adder.aag')
# aag.circuit.print()
# for out in ['o0', 'o1']:
#     for i0 in [0, 1]:
#         for i1 in [0, 1]:
#             print("Shap score of output '", out, "' with i0=", i0, ", i1=", i1, ": ", aag.shap_scores(['i0', 'i1'], {'i0': i0, 'i1': i1}, out))
#
# aag = AAGTree('../aag/ff.aag')
# aag.circuit.print()
# # print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'o0'))
# # print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'o1'))
# # print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'ln0'))

import unittest
from unittest.mock import patch
from io import StringIO
class Tests(unittest.TestCase):
    def setUp(self):
        # This method is called before each test
        pass

    def _check_print(self, print_func, expected):
        with unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_func()
            self.assertEqual(
                mock_stdout.getvalue().split(),
                expected.split()  # It's important to remember about '\n'
            )

    def _check_circuit(self, aag_path, expected):
        aag = AAGTree(aag_path)
        self._check_print(
            aag.circuit.print,
            expected
        )

    def test_and(self):
        self._check_circuit(
            '../aag/and.aag',
            "Output o0\
                        3\
                             AND\
                                 1\
                                     Input i0\
                                2\
                                      Input i1"
        )

    def test_latch(self):
        self._check_circuit(
            '../aag/latch.aag',
            "Output o0\
                        1\
                            LatchPrev lp0\
                    Output o1\
                        NOT\
                            1\
                                LatchPrev lp0\
                    LatchNext ln0\
                        NOT\
                            1\
                                LatchPrev lp0"
        )

    def test_half_adder(self):
        self._check_circuit(
            '../aag/half_adder.aag',
            "Output o0: s\
                    \
                        3\
                            AND\
                                NOT\
                                    6\
                                        AND\
                                            1\
                                                Input i0: x\
                    \
                                            2\
                                                Input i1: y\
                    \
                                NOT\
                                    7\
                                        AND\
                                            NOT\
                                                1\
                                                    Input i0: x\
                    \
                                            NOT\
                                                2\
                                                    Input i1: y\
                    \
                    \
                    Output o1: c\
                    \
                        6\
                            AND\
                                1\
                                    Input i0: x\
                    \
                                2\
                                    Input i1: y"
        )

    def test_ff(self):
        self._check_circuit(
            '../aag/ff.aag',
            "Output o0\
                        3\
                            LatchPrev lp0\
                    Output o1\
                        NOT\
                            3\
                                LatchPrev lp0\
                    LatchNext ln0\
                        4\
                            AND\
                                2\
                                    Input i1\
                                5\
                                    AND\
                                        NOT\
                                            6\
                                                AND\
                                                    1\
                                                        Input i0\
                                                    3\
                                                        LatchPrev lp0\
                                        NOT\
                                            7\
                                                AND\
                                                    NOT\
                                                        1\
                                                            Input i0\
                                                    NOT\
                                                        3\
                                                            LatchPrev lp0"
        )

if __name__ == '__main__':
    unittest.main()
