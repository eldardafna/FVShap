from Tree.AAGTree import AAGTree
import gui

def init_aag(aag_path, should_print=False):
    print("AAG Init: ", aag_path)
    aag_tree = AAGTree(aag_path)
    if(should_print):
        aag_tree.circuit.print()
    return aag_tree

def print_tree(aag_tree: AAGTree):
    aag_tree.print()
def open_gui(aag_tree: AAGTree):
    gui.open_gui([leave.id for leave in aag_tree.circuit.inputs+aag_tree.circuit.latches_prev],
                 [root.id for root in aag_tree.circuit.outputs+aag_tree.circuit.latches_next+aag_tree.circuit.bad_states],
                 aag_tree)

