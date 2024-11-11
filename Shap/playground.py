from utilis import *

"""
Modes that available for SHAP in order to handle with decomposability:
1. VARIABLE_INSTANCES_AS_PLAYERS: each variable instance is a different player for calculating the shap score. That may
                                  consider unreal assignments where two different instances of the same variable are
                                  given different value.
2. CHANGE_TO_AVERAGE_GATE: each composable and gate will be interpreted as an "average gate", which means that instead
                           of calculateing z=max{x,y}, we will be calculating z=0.5(x+y). This can be calculated in
                           polynomial time. The gate will be smoothen beforehand, which means that var(child0)=var(child1)
"""

# file may be aag, aig or cnf
alu = init_from_file("../aag/simple_alu.aag", mode="CHANGE_TO_AVERAGE_GATE", should_print=False) # ln10
sample = alu.get_sample(default_value=0, dict={'i0': 0, 'i1': 1, 'i2': 0, 'i3': 1, 'i4': 1, 'i5': 1, 'i6': 0, 'i7': 1, 'i8': 1, 'i9': 0, 'i10': 1, 'i11': 0, 'i12': 1, 'i13': 1, 'i14': 1, 'i15': 1, 'i16': 1, 'i17': 1, 'i18': 0, 'i19': 0, 'i20': 1, 'i21': 1, 'i22': 0, 'i23': 1, 'i24': 1, 'i25': 1, 'i26': 1, 'i27': 0, 'i28': 0, 'i29': 1, 'i30': 1, 'i31': 0, 'i32': 1, 'i33': 0, 'lp0': 1, 'lp1': 0, 'lp2': 0, 'lp3': 1, 'lp4': 0, 'lp5': 1, 'lp6': 0, 'lp7': 1, 'lp8': 0, 'lp9': 1, 'lp10': 0, 'lp11': 0, 'lp12': 1, 'lp13': 0, 'lp14': 1, 'lp15': 1, 'lp16': 1, 'lp17': 1, 'lp18': 1, 'lp19': 1, 'lp20': 1})
open_gui(alu, init_sample=sample)
