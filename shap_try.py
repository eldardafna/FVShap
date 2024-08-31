from Tree.AAGTree import AAGTree
import aiger
import math
#
# aag_tree = AAGTree("aag/and.aag")
# aag_tree.circuit.print()
# print(aag_tree.simulate({'i0': 0, 'i1': 0}, 'o0'))
# print(aag_tree.simulate({'i0': 0, 'i1': 1}, 'o0'))
# print(aag_tree.simulate({'i0': 1, 'i1': 0}, 'o0'))
# print(aag_tree.simulate({'i0': 1, 'i1': 1}, 'o0'))
#
aag_tree = AAGTree("aag/coverted_aig/miim.aag")
aag_tree.circuit.print()
# print(aag_tree.simulate({'i0': 0, 'i1': 1, 'lp0': 1}, 'ln0'))
sample = {leaf.id: 0 for leaf in aag_tree.circuit.inputs+aag_tree.circuit.latches_prev}
shaps = aag_tree.shap_scores([leaf.id for leaf in aag_tree.circuit.inputs+aag_tree.circuit.latches_prev], sample, 'ln35')
shaps_nonzero = {leaf: shaps[leaf] for leaf in shaps.keys() if shaps[leaf]!=0}
print(shaps_nonzero)
# print(list(shaps_nonzero.keys()))
# print(sum(shaps_nonzero.values()))
# print(aag_tree.simulate( {leaf.id: 0 for leaf in aag_tree.circuit.inputs+aag_tree.circuit.latches_prev}, 'ln35'))

# new_list = ['lp7', 'lp8', 'lp9', 'lp10', 'lp11', 'lp12', 'lp13', 'lp14', 'lp18', 'lp24', 'lp25', 'lp26', 'lp27', 'lp28', 'lp29', 'lp30', 'lp31', 'lp34', 'lp35']
# for leaf in new_list:
#     sample[leaf] = 1
# shaps = aag_tree.shap_scores([leaf.id for leaf in aag_tree.circuit.inputs+aag_tree.circuit.latches_prev], sample, 'ln35')
# shaps_nonzero = {leaf: shaps[leaf] for leaf in shaps.keys() if shaps[leaf]!=0}
# shaps_sorted = sorted(shaps_nonzero, key=lambda leaf: abs(shaps_nonzero[leaf]))
# print({leaf: shaps_nonzero[leaf] for leaf in shaps_sorted})
# print(sum(shaps_nonzero.values()))
# print(aag_tree.simulate(sample, 'ln35'))

# count = 0
# for leaf in shaps_sorted:
#     count += 1
#     sample[leaf] = 1-sample[leaf]
#     sim = aag_tree.simulate(sample, 'ln35')
#     print(sim)
#     if not sim:
#         print(count)
#         exit(0)




# import sympy as sp
#
# # Define N
# N = 5  # For example, if you want 5 symbols
# INPUTS = ['a', 'b', 'c']
#
# # Generate N symbols named x1, x2, ..., xN
# symbols_list = []
# for i in INPUTS:
#     symbols_list.append(sp.symbols(f'y{i}'))
# # symbols_list = symbols(f'x1:{N+1}')  # This will create symbols x1, x2, ..., xN
#
# # Display the generated symbols
# print(symbols_list)
#
# a = sp.symbols(f'za')
# b = sp.symbols(f'zb')
# formula1 = a - b
# formula2 = a + b
# print(formula1+formula2)
# print(formula1*formula2)
# print(sp.expand(formula1+formula2))
# print(sp.expand(formula1*formula2))
# print(formula1.subs({"za": 1, "yb": 2, 'yc': 3}))
#
