from utilis import *

# half_adder = init_aag("aag/half_adder.aag")
# latch = init_aag("aag/latch.aag")
# bad_state = init_aag("aag/bad_state.aag")


# open_gui(half_adder)

# always_zero = init_aag("aag/eldar3.aag", True)
# open_gui(always_zero)

# eldar = init_aag("aag/eldar.aag", True)
# open_gui(eldar)

# and_gate = init_aag("aag/and4.aag", True)
# open_gui(and_gate)

# nand_gate = init_aag("aag/nand.aag", True)
# open_gui(nand_gate)

# nand = init_aag("aag/nand3.aag", True)
# open_gui(nand)

# or_gate = init_aag("aag/or3.aag", True)
# open_gui(or_gate)

# ff = init_aag("aag/ff.aag", True)
# open_gui(ff)

# alu = init_aag("aag/simple_alu.aag")
# open_gui(alu)

# miim = init_aag("aag/miim.aag")
# open_gui(miim)

paper = init_aag("../aag/paper.aag", True)
open_gui(paper)

# always_a = init_aag("aag/always_a.aag", True)
# open_gui(always_a)

# https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html
# cnf = init_aag("cnf/uf100-01.aag", True)
# open_gui(cnf)

# clause = init_aag("aag/clause.aag", True)
# open_gui(clause)

# arbitrated = init_aag("aag/arbitrated.aag")
# open_gui(arbitrated)

# cal2 = init_aag("aag/cal2.aag")
# open_gui(cal2, init_sample={'lp389': 1, 'lp259': 1})


# and_gate = init_aag("aag/and.aag", True)
# calculate_shap_scores(and_gate, sample_from_ones(and_gate, ['i0', 'i1']), ['o0'])
# cal2 = init_aag("aag/cal2.aag")
# calculate_shap_scores(cal2, sample_rand(cal2, [], ['lp268' , 'lp401']), ['b0'])
# calculate_shap_scores(cal2, sample_from_ones(cal2, ['lp268' , 'lp401', 'lp396']), ['b0'])

# cnf = init_aag("cnf/uf50-01.aag", True)
# open_gui(cnf)
#
# sample =  {'i0': 0, 'i1': 1, 'i2': 1, 'i3': 0, 'i4': 1, 'i5': 1, 'i6': 1, 'i7': 1, 'i8': 1, 'i9': 0, 'i10': 0, 'i11': 1, 'i12': 0, 'i13': 1, 'i14': 0, 'i15': 0, 'i16': 0, 'i17': 0, 'i18': 1, 'i19': 1, 'i20': 0, 'i21': 0, 'i22': 0, 'i23': 0, 'i24': 0, 'i25': 0, 'i26': 1, 'i27': 0, 'i28': 0, 'i29': 0, 'i30': 0, 'i31': 1, 'i32': 0, 'i33': 1, 'i34': 0, 'i35': 1, 'i36': 1, 'i37': 1, 'i38': 0, 'i39': 0, 'i40': 0, 'i41': 0, 'i42': 0, 'i43': 0, 'i44': 0, 'i45': 0, 'i46': 1, 'i47': 1, 'i48': 1, 'i49': 0}
# for feature, score in [('i13', 2.8686243847945982e-05), ('i45', 2.842152519423156e-05), ('i20', 2.7981908346708785e-05), ('i42', 2.7927478994084192e-05), ('i8', 2.7865060848734744e-05), ('i10', 2.773073188866683e-05), ('i47', 2.7629579390742102e-05), ('i0', 2.699758414010635e-05), ('i48', 2.6962723885068347e-05), ('i19', 2.695377137622554e-05), ('i6', 2.676392204675539e-05), ('i26', 2.5998943426304876e-05), ('i43', 2.598893953329177e-05), ('i33', 2.595349272654881e-05), ('i41', 2.594343738744342e-05), ('i21', 2.5938931855023343e-05), ('i23', 2.5894276465960147e-05), ('i44', 2.5891891889354776e-05), ('i29', 2.588407005764216e-05), ('i40', 2.573638663946603e-05), ('i30', 2.5727146405002724e-05), ('i22', 2.5717936357375982e-05), ('i49', 2.5691305859145802e-05), ('i15', 2.3992513725987934e-05), ('i11', 2.3972233006029832e-05), ('i5', 2.3868921924596874e-05), ('i38', 2.3866452576158083e-05), ('i46', 2.3774895646183764e-05), ('i12', 2.3687653776911608e-05), ('i39', 2.366851568910429e-05), ('i7', 2.366551137961268e-05), ('i37', 2.356116518698884e-05), ('i24', 2.3559712520406946e-05), ('i31', 2.355270154223613e-05), ('i1', 2.3476180012553512e-05), ('i4', 2.3450839255179866e-05), ('i16', 2.3319455796831682e-05), ('i28', 1.8258609776677255e-05), ('i35', 1.6799571878347527e-05), ('i36', 1.6558881079440357e-05), ('i34', 1.6489709921068066e-05), ('i32', -4.702933942573761e-06), ('i18', 2.323702450171564e-06), ('i3', -1.7527919888090926e-06), ('i9', 1.6150425288621056e-06), ('i2', -1.1549314555258224e-06), ('i25', -1.1547402842256375e-06), ('i17', 9.172671103110644e-07), ('i27', 7.884631977309324e-08), ('i14', -3.960270074131518e-08)]:
#     if score < 0:
#         sample[feature] = 1 - sample[feature]
#
# calculate_shap_scores(cnf, sample, ['o0'])
#
#TESTS
# tested = init_aag("aag/simple_alu.aag")
# tested_output = 'b0'
# TEST_sanity_random(tested, tested_output)
# for _ in range(500):
#     if not TEST_change_all_negatives_at_once(tested, tested_output):
#         exit(1)
# for _ in range(1):
#     # if not TEST_the_change_threshold(tested, tested_output):
#     # if not TEST_change_one_by_one(tested, tested_output):
#     if not TEST_change_one_by_one_after_trying(tested, tested_output):
#         exit(1)


# Failure checks
# alu = init_aag("aag/simple_alu.aag")
# print_tree(alu, 'ln10')
# open_gui(alu, init_sample={'i0': 0, 'i1': 1, 'i2': 0, 'i3': 1, 'i4': 1, 'i5': 1, 'i6': 0, 'i7': 1, 'i8': 1, 'i9': 0, 'i10': 1, 'i11': 0, 'i12': 1, 'i13': 1, 'i14': 1, 'i15': 1, 'i16': 1, 'i17': 1, 'i18': 0, 'i19': 0, 'i20': 1, 'i21': 1, 'i22': 0, 'i23': 1, 'i24': 1, 'i25': 1, 'i26': 1, 'i27': 0, 'i28': 0, 'i29': 1, 'i30': 1, 'i31': 0, 'i32': 1, 'i33': 0, 'lp0': 1, 'lp1': 0, 'lp2': 0, 'lp3': 1, 'lp4': 0, 'lp5': 1, 'lp6': 0, 'lp7': 1, 'lp8': 0, 'lp9': 1, 'lp10': 0, 'lp11': 0, 'lp12': 1, 'lp13': 0, 'lp14': 1, 'lp15': 1, 'lp16': 1, 'lp17': 1, 'lp18': 1, 'lp19': 1, 'lp20': 1})

# xor = init_aag("aag/xor3.aag", True)
# open_gui(xor)

# xor3 = init_aag("aag/xor3e.aag", True)
# open_gui(xor3)

# eldar = init_aag("aag/eldar4.aag", True)
# open_gui(eldar)


# alu = init_aag("aag/simple_alu.aag")
# print_tree(alu, 'ln12')
# open_gui(alu, init_sample={'i0': 0, 'i1': 0, 'i2': 0, 'i3': 1, 'i4': 1, 'i5': 1, 'i6': 1, 'i7': 0, 'i8': 0, 'i9': 1, 'i10': 0, 'i11': 0, 'i12': 0, 'i13': 1, 'i14': 0, 'i15': 0, 'i16': 1, 'i17': 1, 'i18': 0, 'i19': 0, 'i20': 0, 'i21': 0, 'i22': 0, 'i23': 0, 'i24': 1, 'i25': 0, 'i26': 0, 'i27': 1, 'i28': 1, 'i29': 0, 'i30': 0, 'i31': 0, 'i32': 1, 'i33': 0, 'lp0': 0, 'lp1': 1, 'lp2': 1, 'lp3': 1, 'lp4': 0, 'lp5': 0, 'lp6': 0, 'lp7': 1, 'lp8': 0, 'lp9': 0, 'lp10': 0, 'lp11': 0, 'lp12': 0, 'lp13': 1, 'lp14': 1, 'lp15': 1, 'lp16': 1, 'lp17': 1, 'lp18': 1, 'lp19': 1, 'lp20': 1})

