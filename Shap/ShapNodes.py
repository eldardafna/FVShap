import math

class ShapNode():
    def __init__(self):
        self.vars = None
        self.vars_with_repetition = None
        self.gamma = None
        self.delta = None
        self.visited = False
        self.last_simulation = None

    def calc_vars(self, mode):
        assert 0
        pass

    def print(self, level):
        assert 0
        pass

    def simulate(self, variables_assignment):
        assert 0
        pass

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        assert 0
        pass

    def reset_visited(self):
        assert 0
        pass

    def vars_num_without_variable_to_shap(self, variable_to_shap, mode):
        if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
            return len(self.vars_with_repetition) - len([1 for var in self.vars_with_repetition if var == variable_to_shap])
        else:
            return len(self.vars) - (1 if variable_to_shap in self.vars else 0)



class Literal(ShapNode):
    def __init__(self, literal):
        ShapNode.__init__(self)
        self.literal = literal
        self.parents = []
        self.child = None

    def calc_vars(self, mode):
        if self.vars is None:
            self.child.calc_vars(mode)
            self.vars = self.child.vars
            if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
                self.vars_with_repetition = self.child.vars_with_repetition

    def print(self, level):
        print(' ' * (level * 4) + str(self.literal))
        self.child.print(level + 1)

    def simulate(self, variables_assignment):
        if not self.visited:
            self.visited = True
            self.last_simulation = self.child.simulate(variables_assignment)
        return self.last_simulation

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        if self.visited:
            return
        self.visited = True
        self.child.calc_gamma_delta(variable_to_shap, variables_assignment, mode)
        self.gamma = self.child.gamma
        self.delta = self.child.delta

    def reset_visited(self):
        if self.visited:
            self.visited = False
            self.child.reset_visited()



class Variable(ShapNode):
    def __init__(self, id, init_value=None):
        ShapNode.__init__(self)
        self.id = id
        self.parent = None
        self.label = None
        self.init_value = init_value

    def calc_vars(self, mode):
        self.vars = {self.id}
        if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
            self.vars_with_repetition = [self.id]

    def print(self, level):
        shap_type = "Input" if self.id.startswith("i") else "LatchPrev" if self.id.startswith("lp") else None
        assert shap_type is not None
        print(' ' * (level * 4) + shap_type + " " + str(self.id) + (": " + self.label if self.label is not None else ""))

    def simulate(self, variables_assignment):
        self.visited = True
        return variables_assignment[self.id]

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        if self.visited:
            return
        self.visited = True
        if variable_to_shap == self.id:
            self.gamma = [1]
            self.delta = [0]
        else:
            self.gamma = [0.5, variables_assignment[self.id]]
            self.delta = [0.5, variables_assignment[self.id]]

    def reset_visited(self):
        self.visited = False

class Constant(ShapNode):
    def __init__(self, const_value):
        ShapNode.__init__(self)
        self.parent = None
        assert const_value == 0 or const_value == 1
        self.value = const_value

    def calc_vars(self, mode):
        self.vars = {}
        if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
            self.vars_with_repetition = []

    def print(self, level):
        shap_type = "Constant"
        print(' ' * (level * 4) + shap_type + " " + str(self.value))

    def simulate(self, variables_assignment):
        self.visited = True
        return self.value

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        self.visited = True
        return

    def reset_visited(self):
        self.visited = False

class Root(ShapNode):
    def __init__(self, id):
        ShapNode.__init__(self)
        self.id = id
        self.child = None
        self.label = None

    def calc_vars(self, mode):
        if self.vars is None:
            self.child.calc_vars(mode)
            self.vars = self.child.vars
            if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
                self.vars_with_repetition = self.child.vars_with_repetition

    def print(self, level):
        assert level == 0
        shap_type = "Output" if self.id.startswith("o") else "LatchNext" if self.id.startswith("ln") else "BadState" if self.id.startswith("b") else None
        assert shap_type is not None
        print(shap_type + " " + str(self.id) + (": " + self.label if self.label is not None else ""))
        self.child.print(1)

    def simulate(self, variables_assignment):
        if not self.visited:
            self.visited = True
            self.last_simulation = self.child.simulate(variables_assignment)
        return self.last_simulation

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        if self.visited:
            return
        self.visited = True
        self.child.calc_gamma_delta(variable_to_shap, variables_assignment, mode)
        self.gamma = self.child.gamma
        self.delta = self.child.delta

    def reset_visited(self):
        if self.visited:
            self.visited = False
            self.child.reset_visited()


class AndGate(ShapNode):
    def __init__(self):
        ShapNode.__init__(self)
        self.parent = None
        self.children = [None, None]
        self.composable = None

    def calc_vars(self, mode):
        if self.vars is None:
            self.children[0].calc_vars(mode)
            self.children[1].calc_vars(mode)
            self.vars = self.children[0].vars | self.children[1].vars
            self.composable = len(self.children[0].vars & self.children[1].vars) > 0
            if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
                self.vars_with_repetition = self.vars | self.vars # Because of "smoothing" the children

    def print(self, level):
        print(' ' * (level * 4) + "AND")
        self.children[0].print(level + 1)
        self.children[1].print(level + 1)

    def simulate(self, variables_assignment):
        if not self.visited:
            self.visited = True
            child_0_simulate = self.children[0].simulate(variables_assignment)
            child_1_simulate = self.children[1].simulate(variables_assignment)
            self.last_simulation = 1 if (child_0_simulate & child_1_simulate) else 0
        return self.last_simulation

    def _combine_children_for_and_gate(self, l_range, l0_range, l1_range, child0_vec, child1_vec):
        combined_vec = [0] * (l_range+1)
        # iterate over all l1+l2=l, such that l0 represents child0.vars-x, l1 represents child1.vars-x
        for l in range(l_range + 1):
            for l0 in range(min(l0_range + 1, l + 1)):
                l1 = l - l0
                if l1 <= l1_range:
                    combined_vec[l] += child0_vec[l0] * child1_vec[l1]
        return combined_vec

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        if self.visited:
            return
        self.visited = True
        self.children[0].calc_gamma_delta(variable_to_shap, variables_assignment, mode)
        self.children[1].calc_gamma_delta(variable_to_shap, variables_assignment, mode)

        # TODO: with average
        vars_num_without_variable_to_shap = self.vars_num_without_variable_to_shap(variable_to_shap, mode)

        if not (mode == "CHANGE_TO_AVERAGE_GATE" and self.composable):
            l_range = vars_num_without_variable_to_shap
            l0_range = self.children[0].vars_num_without_variable_to_shap(variable_to_shap, mode)
            l1_range = self.children[1].vars_num_without_variable_to_shap(variable_to_shap, mode)

            self.gamma = self._combine_children_for_and_gate(l_range, l0_range, l1_range, self.children[0].gamma, self.children[1].gamma)
            self.delta = self._combine_children_for_and_gate(l_range, l0_range, l1_range, self.children[0].delta, self.children[1].delta)

        else: # (mode == "CHANGE_TO_AVERAGE_GATE" and self.composable)
            smoothen_gamma = [None, None]
            smoothen_delta = [None, None]
            # Smoothing children
            """ In order to smooth child0 we will add an invisible gate that his "vars" are child0.vars-child1.vars and
                            always equal 1. Then we will add an invisible and gate between that gate and the original child0. That
                             way, we would have a new child that his vars equal child0.vars+child1.vars.
                             The same thing will be done for child1"""
            for i in range(2):  # iterate over children
                l_range = vars_num_without_variable_to_shap
                lorig_range = self.children[i].vars_num_without_variable_to_shap(variable_to_shap, mode)
                lsmooth_range = l_range-lorig_range

                if(lsmooth_range == 0): # no smoothen needed
                    smoothen_gamma[i] = self.children[i].gamma
                    smoothen_delta[i] = self.children[i].delta
                    continue

                to_smooth = [None] * (lsmooth_range + 1)
                for k in range(lsmooth_range+1):
                    to_smooth[k] = math.comb(lsmooth_range, k)

                smoothen_gamma[i] = self._combine_children_for_and_gate(l_range, lorig_range, lsmooth_range, self.children[i].gamma, to_smooth)
                smoothen_delta[i] = self._combine_children_for_and_gate(l_range, lorig_range, lsmooth_range, self.children[i].delta, to_smooth)

            self.gamma = [None] * (vars_num_without_variable_to_shap+1)
            self.delta = [None] * (vars_num_without_variable_to_shap+1)

            for k in range(vars_num_without_variable_to_shap+1):
                """ option 1 """
                self.gamma[k] = 0.5*(smoothen_gamma[0][k]+smoothen_gamma[1][k])
                self.delta[k] = 0.5*(smoothen_delta[0][k]+smoothen_delta[1][k])

                """ option 2 """
                # assert smoothen_gamma[0][0]<=1
                # assert smoothen_gamma[1][0]<=1
                # assert smoothen_delta[0][0]<=1
                # assert smoothen_delta[1][0]<=1
                # child0_w = 1-smoothen_gamma[0][0]
                # child1_w = 1-smoothen_gamma[1][0]
                #
                # if child0_w + child1_w == 0:
                #     self.gamma[k] = math.comb(vars_num_without_variable_to_shap, k)
                #     assert smoothen_gamma[0][k] == smoothen_gamma[1][k] == self.gamma[k]
                # else:
                #     self.gamma[k] = (child0_w * smoothen_gamma[0][k] + child1_w * smoothen_gamma[1][k]) / (
                #             child0_w + child1_w)
                #
                # child0_w = 1 - smoothen_delta[0][0]
                # child1_w = 1 - smoothen_delta[1][0]
                # if child0_w + child1_w == 0:
                #     self.delta[k] = math.comb(vars_num_without_variable_to_shap, k)
                #     assert smoothen_delta[0][k] == smoothen_delta[1][k] == self.delta[k]
                # else:
                #     self.delta[k] = (child0_w * smoothen_delta[0][k] + child1_w * smoothen_delta[1][k]) / (
                #                 child0_w + child1_w)

                """ option 3"""
                # self.gamma[k] = (smoothen_gamma[1][0]*smoothen_gamma[0][k]+smoothen_gamma[0][0]*smoothen_gamma[1][k]) / (smoothen_gamma[1][0]+smoothen_gamma[0][0])
                # self.delta[k] = (smoothen_delta[1][0]*smoothen_delta[0][k]+smoothen_delta[0][0]*smoothen_delta[1][k]) / (smoothen_delta[1][0]+smoothen_delta[0][0])


                eldar = 1


    def reset_visited(self):
        if self.visited:
            self.visited = False
            self.children[0].reset_visited()
            self.children[1].reset_visited()



class NotGate(ShapNode):
    def __init__(self):
        ShapNode.__init__(self)
        self.parent = None
        self.child = None

    def calc_vars(self, mode):
        if self.vars is None:
            self.child.calc_vars(mode)
            self.vars = self.child.vars
            if mode == "VARIABLE_INSTANCES_AS_PLAYERS":
                self.vars_with_repetition = self.child.vars_with_repetition

    def print(self, level):
        print(' ' * (level * 4) + "NOT")
        self.child.print(level + 1)

    def simulate(self, variables_assignment):
        if not self.visited:
            self.visited = True
            self.last_simulation = 1-self.child.simulate(variables_assignment)
        return self.last_simulation

    def calc_gamma_delta(self, variable_to_shap, variables_assignment, mode):
        if self.visited:
            return
        self.visited = True
        self.child.calc_gamma_delta(variable_to_shap, variables_assignment, mode)

        vars_num_without_variable_to_shap = self.vars_num_without_variable_to_shap(variable_to_shap, mode)

        self.gamma = [None] * (vars_num_without_variable_to_shap + 1)
        self.delta = [None] * (vars_num_without_variable_to_shap + 1)
        for l in range(vars_num_without_variable_to_shap+1):
            comb = math.comb(vars_num_without_variable_to_shap, l)
            self.gamma[l] = comb - self.child.gamma[l]
            self.delta[l] = comb - self.child.delta[l]

    def reset_visited(self):
        if self.visited:
            self.visited = False
            self.child.reset_visited()
