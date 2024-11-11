import math
import re
import subprocess

from ShapTree import ShapTree
from cnf2aag import cnf2aag

AIG_TO_AAG_TEMP_RELATIVE_PATH = "../aiger/aiger/aigtoaig"

class Shap():
    def _parse_header(self, header):
        header_pattern = r"aag (?P<M>\d+) (?P<I>\d+) (?P<L>\d+) (?P<O>\d+) (?P<A>\d+)( (?P<B>\d+))?"
        match = re.match(header_pattern, header)
        assert match
        self.vars_num = int(match.group('M'))
        self.inputs_num = int(match.group('I'))
        self.latches_num = int(match.group('L'))
        self.outputs_num = int(match.group('O'))
        self.and_gates_num = int(match.group('A'))
        self.bad_states_num = int(match.group('B')) if match.group('B') else 0

    def _convert_aig_to_aag(self, aig_path):
        print("Converting aig to aag format")

        aag_path = "tmp_covertend_aig.aag"
        cmd = AIG_TO_AAG_TEMP_RELATIVE_PATH + " -a " + aig_path + " > " + aag_path
        convert_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if convert_process.returncode != 0:
            print("Error: aig conversion failed!")
            print(convert_process.stderr)
            exit(1)
        print("Aig conversion succeeded!")
        return aag_path

    def _convert_cnf_to_aag(self, cnf_path):
        aag_path = "tmp_covertend_aig.aag"
        cnf2aag(cnf_path, aag_path)
        return aag_path


    def __init__(self, path, mode="VARIABLE_INSTANCES_AS_PLAYERS"):
        # Mode Select
        """
        Modes that available for SHAP in order to handle with decomposability:
        1. VARIABLE_INSTANCES_AS_PLAYERS: each variable instance is a different player for calculating the shap score. That may
                                          consider unreal assignments where two different instances of the same variable are
                                          given different value.
        2. CHANGE_TO_AVERAGE_GATE: each composable and gate will be interpreted as an "average gate", which means that instead
                                   of calculateing z=max{x,y}, we will be calculating z=0.5(x+y). This can be calculated in
                                   polynomial time. The gate will be smoothen beforehand, which means that var(child0)=var(child1)
        """
        assert mode == "VARIABLE_INSTANCES_AS_PLAYERS" or mode == "CHANGE_TO_AVERAGE_GATE"
        self.mode = mode

        # Classify File
        print("Initializing ShapTree from " + path)
        if path.endswith(".aag"):
            aag_path = path
        elif path.endswith(".aig"):
            aag_path = self._convert_aig_to_aag(path)
        elif path.endswith(".cnf"):
            aag_path = self._convert_cnf_to_aag(path)
        else:
            assert 0

        # Parse AAG file
        print("Parsing file to tree")
        with open(aag_path) as file:
            line_num = 1
            for line in file:
                splitted_line = line.split(' ')

                # Header
                if line_num == 1:
                    self._parse_header(line)
                    self.tree = ShapTree(self.vars_num, mode)

                # Inputs
                elif line_num <= 1 + self.inputs_num:
                    assert len(splitted_line) == 1
                    input_literal = int(splitted_line[0])
                    self.tree.add_input(input_literal)

                 # Latches
                elif line_num <= 1 + self.inputs_num + self.latches_num:
                    assert len(splitted_line) == 2 or len(splitted_line) == 3
                    latch_perv_literal = int(splitted_line[0])
                    latch_next_literal = int(splitted_line[1])
                    latch_init_value = int(splitted_line[2]) if len(splitted_line) == 3 else None
                    self.tree.add_latch(latch_perv_literal, latch_next_literal, latch_init_value)

                # Outputs
                elif line_num <= 1 + self.inputs_num + self.latches_num + self.outputs_num:
                    assert len(splitted_line) == 1
                    output_literal = int(splitted_line[0])
                    self.tree.add_output(output_literal)

                # Bad states
                elif line_num <= 1 + self.inputs_num + self.latches_num + self.outputs_num + self.bad_states_num:
                    assert len(splitted_line) == 1
                    bad_states_literal = int(splitted_line[0])
                    self.tree.add_bad_state(bad_states_literal)

                # And Gates
                elif line_num <= 1 + self.inputs_num + self.latches_num + self.outputs_num + self.bad_states_num + self.and_gates_num:
                    assert len(splitted_line) == 3
                    and_out_literal = int(splitted_line[0])
                    and_in_0_literal = int(splitted_line[1])
                    and_in_1_literal = int(splitted_line[2])
                    self.tree.add_and_gate(and_out_literal, and_in_0_literal, and_in_1_literal)

                # Labels and Comments
                else:
                    if (splitted_line[0][0] == 'i' or splitted_line[0][0] == 'o' or splitted_line[0][0] == 'l') and splitted_line[0][1:].isdigit():
                        assert len(splitted_line) == 2
                        self.tree.add_label(splitted_line[0][0], splitted_line[0][1:], splitted_line[1])

                line_num += 1
        print("Parsing file to tree has ended successfully!")

        # Vars property calculation
        print("Calculating 'vars' property for tree")
        self.tree.calc_vars()
        print("Calculating 'vars' property for tree has ended successfully!")

    def print(self, root_to_print=None):
        print("Printing tree:")
        self.tree.print(self.tree.get_root_node(root_to_print) if root_to_print is not None else None)

    def simulate(self, variables_assignment, root_to_simulate=None):
        print("Simulating:")
        if root_to_simulate is None:
            simulations = []
            for root in self.tree.roots():
                simulations.append(self.tree.simulate(variables_assignment, root_to_simulate))
                return simulations
        else:
            return self.tree.simulate(variables_assignment, self.tree.get_root_node(root_to_simulate))

    def get_sample(self, default_value=0, ones=[], zeros=[], dict={}):
        assert default_value == 0 or default_value == 1
        # FIXME: assert ones zeros dict are in variables
        sample = {variable.id: (dict[variable.id] if variable.id in dict
                             else 0 if variable.id in zeros
                             else 1 if variable.id in ones
                             else default_value)
                  for variable in self.tree.variables()}
        return sample

    def calculate_shap_scores(self, root_to_shap, variables_assignment):
        # Get root node and check it
        root_to_shap_node = None
        if root_to_shap.startswith('o'):
            assert root_to_shap in self.tree.outputs
            root_to_shap_node = self.tree.outputs[root_to_shap]
        elif root_to_shap.startswith('ln'):
            assert root_to_shap in self.tree.latches_next
            root_to_shap_node = self.tree.latches_next[root_to_shap]
        elif root_to_shap.startswith('b'):
            assert root_to_shap in self.tree.bad_states
            root_to_shap_node = self.tree.bad_states[root_to_shap]
        else:
            assert 0

        # Check variable assignment
        variables_id = [variable.id for variable in self.tree.variables()]
        for variable in self.tree.variables():
            assert variables_assignment[variable.id] == 0 or variables_assignment[variable.id] == 1

        # Calculate shap scores
        shap_scores = {variable_id: 0 for variable_id in variables_id}
        for variable_to_shap in root_to_shap_node.vars: # only variables in coi
            print("Calculating Shap scores for variable:", variable_to_shap)

            # Calculating gammas and deltas
            self.tree.calculate_gamma_delta(root_to_shap_node, variable_to_shap, variables_assignment)

            # Combining gammas and deltas to shap score
            X = root_to_shap_node.vars_num_without_variable_to_shap(variable_to_shap, self.mode) + 1
            e_var_minus_p_var = variables_assignment[variable_to_shap] - 0.5
            for k in range(X):
                # coefficient = 1/((math.comb(X, k))*(X-k))
                coefficient = 1/((math.comb(X, k))*(X-k))
                # assert coefficient == math.factorial(k) * math.factorial(X - k - 1) / math.factorial(X)
                if coefficient == 0: # due to too small coefficient
                    continue
                shap_scores[variable_to_shap] += coefficient * (
                    e_var_minus_p_var * (root_to_shap_node.gamma[k] - root_to_shap_node.delta[k]))

            print(variable_to_shap, ": ", shap_scores[variable_to_shap])

        return shap_scores

    def decomposable_roots_num(self):
        return self.tree.decomposable_roots_num()



# test = Shap("../aag/paper.aag")
# # test = Shap("../aag/always_zero.aag")
# test.print()
# sample = test.get_sample(default_value=0, ones=['i1', 'i2'])
# print(sample)
# test.simulate(sample)
# print(test.calculate_shap_scores('b0', sample))
# # print(test.decomposable_roots_num(), '/', len([1 for root in test.tree.roots()]))
