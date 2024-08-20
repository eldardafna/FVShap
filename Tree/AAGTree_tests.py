from AAGTree import AAGTree

# c = BinaryCircuit(3)
# c.add_input(2)
# c.add_input(4)
# c.add_and_gate(6,2, 4)
# c.add_output(7)

# c = BinaryCircuit(1)
# c.add_latch(2, 3)
# c.add_output(2)
# c.add_output(3)
# c.print()

aag = AAGTree('../aag/and.aag')
aag.circuit.print()
print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 0, 'i1': 0}, 'o0'))
print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 1, 'i1': 0}, 'o0'))
print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 0, 'i1': 1}, 'o0'))
print(aag.circuit.calculate_shap_scores(['i0', 'i1'], {'i0': 1, 'i1': 1}, 'o0'))

aag = AAGTree('../aag/latch.aag')
aag.circuit.print()
print(aag.shap_scores(['lp0'], {'lp0': 0}, 'o0'))
print(aag.shap_scores(['lp0'], {'lp0': 0}, 'o1'))
print(aag.shap_scores(['lp0'], {'lp0': 0}, 'ln0'))
print(aag.shap_scores(['lp0'], {'lp0': 1}, 'o0'))
print(aag.shap_scores(['lp0'], {'lp0': 1}, 'o1'))
print(aag.shap_scores(['lp0'], {'lp0': 1}, 'ln0'))


aag = AAGTree('../aag/half_adder.aag')
aag.circuit.print()
for out in ['o0', 'o1']:
    for i0 in [0, 1]:
        for i1 in [0, 1]:
            print("Shap score of output '", out, "' with i0=", i0, ", i1=", i1, ": ", aag.shap_scores(['i0', 'i1'], {'i0': i0, 'i1': i1}, out))

# aag = AAGTree('ff.aag')
# aag.circuit.print()
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'o0'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'o1'))
# print(aag.shap_scores(['i0', 'i1', 'lp0'], {'i0': 0, 'i1': 0, 'lp0': 0}, 'ln0'))
