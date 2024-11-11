from dask.core import literal

from ShapNodes import Literal, Constant, Variable, Root, AndGate, NotGate


class ShapTree():

    def __init__(self, vars_num, mode):
        self.literals = {i: Literal(i) for i in range(1, vars_num + 1)}
        self.inputs = {}
        self.outputs = {}
        self.bad_states = {}
        self.latches_prev = {}
        self.latches_next = {}
        self.mode = mode

    def roots(self):
        for output in self.outputs.values():
            yield output
        for latch_next in self.latches_next.values():
            yield latch_next
        for bad_state in self.bad_states.values():
            yield bad_state

    def get_root_node(self, root_id):
        root_list = [node for node in self.roots() if node.id == root_id]
        assert len(root_list) == 1
        return root_list[0]

    def variables(self):
        for input in self.inputs.values():
            yield input
        for latch_prev in self.latches_prev.values():
            yield latch_prev

    def _add_variable(self, literal: int, id: str, init_value: int = None):
        my_variable = Variable(id, init_value)

        if literal % 2 == 0:
            my_variable.parent = self.literals[literal // 2]
            self.literals[literal // 2].child = my_variable
        else:
            my_not = NotGate()
            my_not.child = my_variable
            my_variable.parent = my_not
            my_not.parent = self.literals[literal // 2]
            self.literals[literal // 2].child = my_not
        return my_variable

    def _add_root(self, literal: int, id: str):
        my_root = Root(id)

        if literal == 0 or literal == 1:
            my_constant = Constant(literal)
            my_root.child = my_constant
            my_constant.parent = my_root
        elif literal % 2 == 0:
            my_root.child = self.literals[literal // 2]
            self.literals[literal // 2].parents.append(my_root)
        else:
            my_not = NotGate()
            my_not.child = self.literals[literal // 2]
            self.literals[literal // 2].parents.append(my_not)
            my_not.parent = my_root
            my_root.child = my_not
        return my_root

    def add_input(self, literal: int):
        assert literal // 2 in self.literals
        my_id = 'i' + str(len(self.inputs))
        my_input = self._add_variable(literal, my_id)
        self.inputs[my_id] = my_input

    def add_output(self, literal: int):
        assert literal // 2 in self.literals
        my_id = 'o' + str(len(self.outputs))
        my_output = self._add_root(literal, my_id)
        self.outputs[my_id] = my_output

    def add_bad_state(self, literal: int):
        my_id = 'b' + str(len(self.bad_states))
        my_bad_state = self._add_root(literal, my_id)
        self.bad_states[my_id] = my_bad_state

    def add_latch(self, literal_prev: int, literal_next: int, init_value: int):
        assert literal_prev // 2 in self.literals
        assert literal_next // 2 in self.literals or literal_next == 0 or literal_next == 1
        assert init_value is None or init_value == 0 or init_value == 1 or init_value == literal_prev #FIXME: maybe it is an inverter?
        if init_value == literal_prev:
            init_value = None
        prev_id = 'lp' + str(len(self.latches_prev))
        next_id = 'ln' + str(len(self.latches_next))
        my_latch_prev = self._add_variable(literal_prev, prev_id, init_value)
        my_latch_next = self._add_root(literal_next, next_id)
        self.latches_prev[prev_id] = my_latch_prev
        self.latches_next[next_id] = my_latch_next

    def _add_and_gate_in(self, literal_in, i, my_and_gate):
        if literal_in % 2 == 0:
            my_and_gate.children[i] = self.literals[literal_in // 2]
            self.literals[literal_in // 2].parents.append(my_and_gate)
        else:
            my_not_in = NotGate()
            my_not_in.parent = my_and_gate
            my_and_gate.children[i] = my_not_in
            my_not_in.child = self.literals[literal_in // 2]
            self.literals[literal_in // 2].parents.append(my_not_in)

    def add_and_gate(self, literal_out: int, literal_in1: int, literal_in2: int):
        assert literal_out // 2 in self.literals
        assert literal_in1 // 2 in self.literals
        assert literal_in2 // 2 in self.literals

        my_and_gate = AndGate()

        # Out
        if literal_out % 2 == 0:
            my_and_gate.parent = self.literals[literal_out // 2]
            self.literals[literal_out // 2].child = my_and_gate
        else:
            my_not_out = NotGate()
            my_not_out.child = my_and_gate
            my_and_gate.parent = my_not_out
            my_not_out.parent = self.literals[literal_out // 2]
            self.literals[literal_out // 2].child = my_not_out

        # In
        self._add_and_gate_in(literal_in1, 0, my_and_gate)
        self._add_and_gate_in(literal_in2, 1, my_and_gate)

    def add_label(self, type, index, label):
        if type == 'i':
            id = type + index
            self.inputs[id].name = label
        elif type == 'o':
            id = type + index
            self.outputs[id].name = label
        elif type == 'l':
            id_p = 'lp' + index
            id_n = 'ln' + index
            self.latches_prev[id_p].name = label
            self.latches_next[id_n].name = label
        else:
            assert False

    def calc_vars(self):
        for root in self.roots():
            root.calc_vars(self.mode)

    def print(self, root_to_print):
        if root_to_print is None:
            for root in self.roots():
                print("Printing tree for " + root.id + ":")
                root.print(0)
                print()
        else:
            assert root_to_print in self.roots()
            print("Printing tree for " + root_to_print.id + ":")
            root_to_print.print(0)

    def simulate(self, variables_assignment, root_to_simulate):
        print("Variables assignment: ", variables_assignment)
        assert root_to_simulate in self.roots()
        print("Simulating for " + root_to_simulate.id + ":")
        res = root_to_simulate.simulate(variables_assignment)
        root_to_simulate.reset_visited()

        print("Result: ", res)
        return res

    def calculate_gamma_delta(self, root_to_shap_node, variable_to_shap, variables_assignment):
        root_to_shap_node.calc_gamma_delta(variable_to_shap, variables_assignment, self.mode)
        root_to_shap_node.reset_visited()

    def decomposable_roots_num(self):
        decomposable_roots_num = 0
        for root in self.roots():
            for var_to_check in root.vars:
                if len([1 for var in root.vars_with_repetition if var == var_to_check]) > 1:
                    decomposable_roots_num += 1
                    break

        return decomposable_roots_num



