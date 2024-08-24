from typing import Callable
import math
import re

class TreeNode:
    def __init__(self):
        self.influencers = None
        self.gamma = None
        self.delta = None

    def init_influencers(self):
        self.influencers = set()

    def init_gamma_delta(self):
        assert self.influencers is not None
        assert len(self.influencers) > 0
        self.gamma = [None] * (len(self.influencers)+1)
        self.delta = [None] * (len(self.influencers)+1)

    def calculate_influencers(self):
        assert 0
        pass

    def calculate_gamma_delta(self, feature, features_sample):
        assert 0
        pass

    def simulate(self, leaves_sample):
        assert 0
        pass

class Variable(TreeNode):
    def __init__(self, var_num):
        TreeNode.__init__(self)
        self.var_num = var_num
        self.parents = []
        self.child = None

    def print(self, level):
        print(' '*(level*4) + str(self.var_num))
        self.child.print(level+1)

    def search_up(self, func:Callable[[], None]):
        func(self)
        for parent in self.parents:
            parent.search_up(func)

    def search_down(self, func:Callable[[], None]):
        self.child.search_down(func)
        func(self)

    def calculate_influencers(self):
        self.child.calculate_influencers()
        self.influencers = self.child.influencers

    def calculate_gamma_delta(self, feature, features_sample):
        if None not in self.gamma:
            assert None not in self.delta
            return
        self.child.calculate_gamma_delta(feature, features_sample)
        self.gamma = self.child.gamma
        self.delta = self.child.delta

    def simulate(self, leaves_sample) -> bool:
        return self.child.simulate(leaves_sample)


class Leaf(TreeNode):
    def __init__(self, id):
        TreeNode.__init__(self)
        self.name = None
        self.parent = None
        self.id = id

    def search_up(self, func: Callable[[TreeNode], None]):
        func(self)
        self.parent.search_up(func)

    def search_down(self, func:Callable[[], None]):
        func(self)

    def calculate_influencers(self):
        self.influencers = {self.id}


    def calculate_gamma_delta(self, feature, features_sample):
        assert len(self.influencers) == 1

        if list(self.influencers)[0] == feature:
            self.gamma = [1]
            self.delta = [0]
        else:
            self.gamma[0] = 0.5
            self.delta[0] = 0.5
            self.gamma[1] = features_sample[list(self.influencers)[0]]
            self.delta[1] = features_sample[list(self.influencers)[0]]

    def simulate(self, leaves_sample)  -> bool:
        return bool(leaves_sample[self.id])


class Root(TreeNode):
    def __init__(self, id):
        TreeNode.__init__(self)
        self.name = None
        self.child = None
        self.id = id

    def search_up(self, func: Callable[[TreeNode], None]):
        func(self)
        pass

    def search_down(self, func:Callable[[], None]):
        self.child.search_down(func)
        func(self)

    def calculate_influencers(self):
        self.child.calculate_influencers()
        self.influencers = self.child.influencers

    def calculate_gamma_delta(self, feature, features_sample):
        self.child.calculate_gamma_delta(feature, features_sample)
        self.gamma = self.child.gamma
        self.delta = self.child.delta

    def simulate(self, leaves_sample) -> bool:
        return self.child.simulate(leaves_sample)

class Input(Leaf):
    def __init__(self, id):
        Leaf.__init__(self, id)

    def print(self, level):
        print(' ' * (level * 4) + "Input " + str(self.id) + (": " + self.name if self.name is not None else ""))


class LatchPrev(Leaf):
    def __init__(self, id, init_value=None):
        Leaf.__init__(self, id)
        assert (not init_value) or init_value==0 or init_value==1
        self.init_value = init_value

    def print(self, level):
        print(' ' * (level * 4) + "LatchPrev " + str(self.id)
              + (": " + self.name if self.name is not None else "")
              + ("(init: " + self.init_value + ")" if self.init_value is not None else ""))


class Output(Root):
    def __init__(self, id):
        Root.__init__(self, id)

    def print(self):
        print("Output " + str(self.id) + (": " + self.name if self.name is not None else ""))
        self.child.print(1)

class BadState(Root):
    def __init__(self, id):
        Root.__init__(self, id)

    def print(self):
        print("BadState " + str(self.id) + (": " + self.name if self.name is not None else ""))
        self.child.print(1)


class LatchNext(Root):
    def __init__(self, id):
        Root.__init__(self, id)

    def print(self):
        print("LatchNext " + str(self.id) + (": " + self.name if self.name is not None else ""))
        self.child.print(1)

class AndGate(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)
        self.parent = None
        self.children = [None, None]

    def print(self, level):
        print(' ' * (level * 4) + "AND")
        self.children[0].print(level + 1)
        self.children[1].print(level + 1)

    def search_up(self, func: Callable[[TreeNode], None]):
        func(self)
        self.parent.search_up(func)

    def search_down(self, func:Callable[[], None]):
        self.children[0].search_down(func)
        self.children[1].search_down(func)
        func(self)

    def calculate_influencers(self):
        self.children[0].calculate_influencers()
        self.children[1].calculate_influencers()
        self.influencers = self.children[0].influencers | self.children[1].influencers

    @staticmethod
    def _get_range_for_gamma_delta_calculation(node: TreeNode, feature):
        return len(node.influencers)-1 if (feature in node.influencers) else len(node.influencers)
    def calculate_gamma_delta(self, feature, features_sample):
        self.children[0].calculate_gamma_delta(feature, features_sample)
        self.children[1].calculate_gamma_delta(feature, features_sample)

        self.gamma = [0]*(len(self.influencers)+1)
        self.delta = [0]*(len(self.influencers)+1)
        l_range = self._get_range_for_gamma_delta_calculation(self, feature)
        l0_range = self._get_range_for_gamma_delta_calculation(self.children[0], feature)
        l1_range = self._get_range_for_gamma_delta_calculation(self.children[1], feature)
        for l in range(l_range+1):
            for l0 in range(l0_range+1):
                for l1 in  range(l1_range+1):
                    if l0+l1==l:
                        assert self.children[0].gamma[l0] is not None
                        assert self.children[1].gamma[l1] is not None
                        self.gamma[l] += self.children[0].gamma[l0]*self.children[1].gamma[l1]
                        self.delta[l] += self.children[0].delta[l0]*self.children[1].delta[l1]

    def simulate(self, leaves_sample) -> bool:
        return self.children[0].simulate(leaves_sample) and self.children[1].simulate(leaves_sample)



class NotGate(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)
        self.parent = None
        self.child = None

    def print(self, level):
        print(' ' * (level * 4) + "NOT")
        self.child.print(level + 1)

    def search_up(self, func: Callable[[TreeNode], None]):
        func(self)
        self.parent.search_up(func)

    def search_down(self, func:Callable[[], None]):
        self.child.search_down(func)
        func(self)

    def calculate_influencers(self):
        self.child.calculate_influencers()
        self.influencers = self.child.influencers

    def calculate_gamma_delta(self, influencer, features_sample):
        self.child.calculate_gamma_delta(influencer, features_sample)
        l_range = len(self.influencers)-1 if (influencer in self.influencers) else len(self.influencers)
        for l in range(l_range+1):
            self.gamma[l] = math.comb(l_range, l) - self.child.gamma[l]
            self.delta[l] = math.comb(l_range, l) - self.child.delta[l]

    def simulate(self, leaves_sample) -> bool:
        return not bool(self.child.simulate(leaves_sample))



class BinaryCircuit:
    def __init__(self, vars_num):
        self.vars = {i : Variable(i) for i in range(1, vars_num+1)}
        self.inputs = []
        self.outputs = []
        self.bad_states = []
        self.latches_prev = []
        self.latches_next = []
        self.and_gates = []
        self.id_map = {}

    def search_from_leaves(self, func: Callable):
        for curr_input in self.inputs:
            curr_input.search_up(func)

    def _add_input_or_latch_prev(self, literal: int, is_input: bool, latch_prev_init_value: int =None):
        assert literal // 2 in self.vars
        my_id = 'i'+str(len(self.inputs)) if is_input else 'lp'+str(len(self.latches_prev))
        my_input = Input(my_id) if is_input else LatchPrev(my_id, latch_prev_init_value)
        self.id_map[my_id] = my_input
        if literal % 2 == 0:
            my_input.parent = self.vars[literal // 2]
            self.vars[literal // 2].child = my_input
        else:
            my_not = NotGate()
            my_not.child = my_input
            my_input.parent = my_not
            my_not.parent = self.vars[literal // 2]
            self.vars[literal // 2].child = my_not
        return  my_input

    def _add_output_or_bad_state_or_latch_next(self, literal: int, is_output: bool, is_bad_state: bool = False):
        assert literal // 2 in self.vars
        if is_output:
            my_id = 'o'+str(len(self.outputs))
            my_output = Output(my_id)
        elif is_bad_state:
            my_id = 'b'+str(len(self.bad_states))
            my_output = BadState(my_id)
        else:
            my_id = 'ln'+str(len(self.latches_next))
            my_output = LatchNext(my_id)
        self.id_map[my_id] = my_output
        if literal % 2 == 0:
            my_output.child = self.vars[literal // 2]
            self.vars[literal // 2].parents.append(my_output)
        else:
            my_not = NotGate()
            my_not.child = self.vars[literal // 2]
            self.vars[literal // 2].parents.append(my_not)
            my_not.parent = my_output
            my_output.child = my_not
        return my_output

    def add_input(self, literal: int):
        my_input = self._add_input_or_latch_prev(literal, True)
        self.inputs.append(my_input)

    def add_output(self, literal: int):
        my_output = self._add_output_or_bad_state_or_latch_next(literal, True)
        self.outputs.append(my_output)

    def add_bad_state(self, literal: int):
        my_bad_state = self._add_output_or_bad_state_or_latch_next(literal, False, True)
        self.bad_states.append(my_bad_state)

    def add_latch(self, literal_prev: int, literal_next: int):
        my_latch_prev = self._add_input_or_latch_prev(literal_prev, False)
        self.latches_prev.append(my_latch_prev)
        my_latch_next = self._add_output_or_bad_state_or_latch_next(literal_next, False)
        self.latches_next.append(my_latch_next)

    def _add_and_gate_in(self, literal_in, i, my_and_gate):
        assert literal_in // 2 in self.vars

        if literal_in %2 == 0:
            my_and_gate.children[i] = self.vars[literal_in // 2]
            self.vars[literal_in // 2].parents.append(my_and_gate)
        else:
            my_not_in = NotGate()
            my_not_in.parent = my_and_gate
            my_and_gate.children[i] = my_not_in
            my_not_in.child = self.vars[literal_in // 2]
            self.vars[literal_in // 2].parents.append(my_not_in)
    def add_and_gate(self,  literal_out: int, literal_in1: int, literal_in2: int):
        assert literal_out//2 in self.vars

        my_and_gate = AndGate()

        # Out
        if literal_out % 2 == 0:
            my_and_gate.parent = self.vars[literal_out // 2]
            self.vars[literal_out // 2].child = my_and_gate
        else:
            my_not_out = NotGate()
            my_not_out.child = my_and_gate
            my_and_gate.parent = my_not_out
            my_not_out.parent = self.vars[literal_out // 2]
            self.vars[literal_out // 2].child = my_not_out

        #In
        self._add_and_gate_in(literal_in1, 0, my_and_gate)
        self._add_and_gate_in(literal_in2, 1, my_and_gate)

    def add_label(self, type, index, label):
        if type=='i':
            self.inputs[index].name = label
        elif type=='o':
            self.outputs[index].name = label
        elif type=='l':
            self.latches_prev[index].name = label
            self.latches_next[index].name = label
        else:
            assert False


    def print(self, num_of_roots=None):
        roots = self.outputs+self.bad_states+self.latches_next
        if not num_of_roots:
            num_of_roots = len(roots)
        for root in roots:
            root.print()
            print()
            num_of_roots -= 1
            if num_of_roots == 0:
                return

    def simulate(self, leaves_sample, output_to_simulate) -> bool:
        assert output_to_simulate in self.id_map
        assert output_to_simulate.startswith('o') or output_to_simulate.startswith('b') or output_to_simulate.startswith('ln')
        assert len([feature for feature in leaves_sample.keys() if feature not in self.id_map]) == 0
        assert len([value for value in leaves_sample.values() if (value != 0 and value != 1)]) == 0

        output_node = self.id_map[output_to_simulate]
        return output_node.simulate(leaves_sample)



    #SHAP
    def calculate_gamma_delta(self, feature, features_sample, output_node):
        output_node.search_down(TreeNode.init_gamma_delta)
        output_node.calculate_gamma_delta(feature, features_sample)

    def calculate_shap_scores(self, features, features_sample, output_to_check):
        assert output_to_check in self.id_map
        assert output_to_check.startswith('o') or output_to_check.startswith('b') or output_to_check.startswith('ln')
        assert len([feature for feature in features if feature not in self.id_map]) == 0
        assert len([feature for feature in features if not (feature.startswith('i') or feature.startswith('lp'))]) == 0
        assert len([feature for feature in features_sample.keys() if feature not in self.id_map]) == 0
        assert len([value for value in features_sample.values() if (value!=0 and value!=1)]) == 0

        features_num = len(self.inputs + self.latches_prev)
        shap_scores = {feature: 0 for feature in features}

        output_node = self.id_map[output_to_check]
        output_node.search_down(TreeNode.init_influencers)
        output_node.calculate_influencers()

        for feature in features:
            if feature not in output_node.influencers:
                shap_scores[feature] = 0
                continue

            self.calculate_gamma_delta(feature, features_sample, output_node)

            # for k in range(features_num):
            #     coefficient = math.factorial(k) * math.factorial(features_num - k - 1) / math.factorial(features_num)
            #     assert len(output_node.gamma) >= k
            #     assert output_node.gamma[k] is not None
            #     assert len(output_node.delta) >= k
            #     assert output_node.delta[k] is not None
            #     shap_scores[feature] += coefficient * (
            #     (features_sample[feature] - 0.5) * (output_node.gamma[k] - output_node.delta[k]))

            #FIXME: changed because only calculate for inputs in coi
            coi_features_num = len(output_node.influencers)
            for k in range(coi_features_num):
                coefficient = math.factorial(k) * math.factorial(coi_features_num - k - 1) / math.factorial(coi_features_num)
                assert len(output_node.gamma) >= k
                assert output_node.gamma[k] is not None
                assert len(output_node.delta) >= k
                assert output_node.delta[k] is not None
                shap_scores[feature] += coefficient * (
                (features_sample[feature] - 0.5) * (output_node.gamma[k] - output_node.delta[k]))

        return shap_scores


class AAGTree:
    def _parse_header_aag(self, header):
        header_pattern = r"aag (?P<M>\d+) (?P<I>\d+) (?P<L>\d+) (?P<O>\d+) (?P<A>\d+)( (?P<B>\d+))?"
        match = re.match(header_pattern, header)
        assert match
        self.vars_num = int(match.group('M'))
        self.inputs_num = int(match.group('I'))
        self.latches_num = int(match.group('L'))
        self.outputs_num = int(match.group('O'))
        self.and_gates_num = int(match.group('A'))
        self.bad_states_num = int(match.group('B')) if match.group('B') else 0

    def _parse_header_cnf(self, header):
        header_pattern = r"p cnf (?P<propositional>\d+) (?P<clauses>)"
        match = re.match(header_pattern, header)
        assert match
        self.vars_num = int(match.group('propositional'))
        self.inputs_num = self.vars_num
        self.latches_num = 0
        self.outputs_num = 1
        self.and_gates_num = int(match.group('clauses'))
        self.bad_states_num = 0
        #FIXME

    def _parse_body_aag(self, line, line_num):
        assert line_num != 0

        # Inputs
        if line_num <= 1 + self.inputs_num:
            my_input = line.split(' ')
            assert len(my_input) == 1
            self.circuit.add_input(int(my_input[0]))

            # Latches
        elif line_num <= 1 + self.inputs_num + self.latches_num:
            my_latch = line.split(' ')
            assert len(my_latch) == 2 or len(my_latch) == 3
            self.circuit.add_latch(int(my_latch[0]), int(my_latch[1]))

            # Outputs
        elif line_num <= 1 + self.inputs_num + self.latches_num + self.outputs_num:
            my_output = line.split(' ')
            assert len(my_output) == 1
            self.circuit.add_output(int(my_output[0]))

            # Bad states
        elif line_num <= 1 + self.inputs_num + self.latches_num + self.outputs_num + self.bad_states_num:
            my_bad_state = line.split(' ')
            assert len(my_bad_state) == 1
            self.circuit.add_bad_state(int(my_bad_state[0]))

            # And Gates
        elif line_num <= 1 + self.inputs_num + self.latches_num + self.outputs_num + self.bad_states_num + self.and_gates_num:
            my_and_gate = line.split(' ')
            assert len(my_and_gate) == 3
            self.circuit.add_and_gate(int(my_and_gate[0]), int(my_and_gate[1]), int(my_and_gate[2]))

            # Labels and Comments
        else:
            label = line.split(' ')
            if (label[0][0] == 'i' or label[0][0] == 'o' or label[0][0] == 'l') and label[0][1:].isdigit():
                assert len(label) == 2
                self.circuit.add_label(label[0][0], int(label[0][1:]), label[1])

    def _parse_header(self, header, type):
        assert type == "aag"
        if type=="aag":
            self._parse_header_aag(header)

    def _parse_body(self, line, line_num, type):
        assert type == "aag"
        if type=="aag":
            self._parse_body_aag(line, line_num)

    def __init__(self, path: str):
        assert path.endswith(".aag") or path.endswith(".cnf")
        with open(path) as file:
            line_num = 1
            for line in file:
                # Header
                if line_num == 1:
                    self._parse_header(line, "aag")
                    self.circuit = BinaryCircuit(self.vars_num)
                # Body
                else:
                    self._parse_body(line, line_num, "aag")

                line_num += 1

    def shap_scores(self, features, features_sample, output_to_check):
        assert len(features_sample.keys())==self.inputs_num+self.latches_num
        return self.circuit.calculate_shap_scores(features, features_sample, output_to_check)

    def simulate(self, leaves_sample, output_to_sumulate):
        assert len(leaves_sample.keys()) == self.inputs_num + self.latches_num
        return self.circuit.simulate(leaves_sample, output_to_sumulate)

# aag = AAGTree('../aag/ff.aag')
# aag.circuit.print()
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'o0'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 1}, 'o0'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'o1'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 1}, 'o1'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'ln0'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 1, 'i1': 0, 'lp0': 1}, 'ln0'))