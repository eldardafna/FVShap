from Tree.AAGTree import AAGTree
import gui
import numpy as np
import matplotlib.pyplot as plt

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

def print_shap_chart(shap_scores, highlight_color='dodgerblue', color_positive='cornflowerblue', color_negative='violet'):
    # Sort the array
    sorted_shap_scores = sorted(shap_scores.items(), key=lambda x: abs(x[1]), reverse=True)

    # Extract names and values from the dictionary
    labels, values = zip(*sorted_shap_scores)
    labels = list(labels)
    values = np.array(values)

    # Calculate base value
    values_sum = np.sum(values)
    if values_sum>0:
        base_value = 1-values_sum
    else:
        base_value = -values_sum

    # Calculate cumulative sum
    cumulative = np.cumsum(values) + base_value

    # Define colors based on positive or negative values
    colors = [color_positive if val >= 0 else color_negative for val in values]

    # Start the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the base value as a horizontal line
    ax.barh([0], base_value, color='gray', left=0, height=0.4)

    # Plot each feature's contribution as a horizontal bar
    for i in range(len(values)):
        ax.barh(i + 1, values[i], left=(cumulative[i] - values[i]), color=colors[i])
        ax.text(cumulative[i] - values[i] / 2, i + 1, f'{values[i]:.2f}', va='center', ha='center', color='white',
                fontsize=10)

    # Plot the final output value
    ax.barh(len(values) + 1, cumulative[-1], color=highlight_color, left=0, height=0.6)
    ax.text(cumulative[-1] / 2, len(values) + 1, f'{cumulative[-1]:.2f}', va='center', ha='center', color='white',
            fontsize=10)

    # Set y-axis labels
    ax.set_yticks(range(len(values) + 2))
    ax.set_yticklabels(['Base'] + labels + ['Final Output'])

    # Remove spines and set grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Title and labels
    ax.set_xlabel('Value')
    ax.set_title('SHAP-like Horizontal Waterfall Chart')

    plt.show()

print_shap_chart({'x': 0.25, 'y': -0.5, 'z': -0.2})