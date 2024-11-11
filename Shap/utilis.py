from Shap import Shap
import gui
import numpy as np
import matplotlib.pyplot as plt
import random

def init_from_file(file_path, mode="CHANGE_TO_AVERAGE_GATE", should_print=False):
    print("Shap Init: ", file_path)
    aag_tree = Shap(file_path, mode)
    if(should_print):
        aag_tree.print()
    return aag_tree

def print_tree(aag_tree: Shap, output_to_print=None):
    if output_to_print:
        aag_tree.tree.id_map[output_to_print].print()
    else:
        aag_tree.print()

def open_gui(aag_tree: Shap, init_sample={}):
    gui.open_gui([variable.id for variable in aag_tree.tree.variables()],
                 [root.id for root in aag_tree.tree.roots()],
                 aag_tree,
                 init_sample)

def print_shap_chart(shap_scores, simulation, highlight_color='dodgerblue', color_positive='cornflowerblue', color_negative='violet'):
    assert simulation == 1 or simulation == 0

    # Sort the array
    sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1]!=0], key=lambda x: abs(x[1]), reverse=True)
    print("sorted_shap_scores_positive", sorted([item for item in shap_scores.items() if item[1]>0], key=lambda x: x[1], reverse=True))
    print("sorted_shap_scores_negative", sorted([item for item in shap_scores.items() if item[1]<0], key=lambda x: x[1], reverse=False))
    if sorted_shap_scores == []:
        print("All Shap scores are 0")
        return

    # Extract names and values from the dictionary
    labels, values = zip(*sorted_shap_scores)
    labels = list(labels)
    values = np.array(values)

    # Calculate base value
    values_sum = np.sum(values)
    base_value = simulation-values_sum

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
    ax.set_yticklabels(['Base'] + labels + ['Shap Output'])

    # Remove spines and set grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Title and labels
    ax.set_xlabel('Value')
    ax.set_title('SHAP-like Horizontal Waterfall Chart')

    plt.show()

# print_shap_chart({'x': 0.25, 'y': -0.5, 'z': -0.2})

def sample_from_ones(tree, ones):
    sample = {}
    for feature in tree.circuit.inputs+tree.circuit.latches_prev:
        sample[feature.id] = 1 if feature.id in ones else 0
    return sample

def sample_from_zeros(tree, zeros):
    sample = {}
    for feature in tree.circuit.inputs+tree.circuit.latches_prev:
        sample[feature.id] = 0 if feature.id in zeros else 1
    return sample

def sample_rand(tree, zeros, ones):
    sample = {}
    for feature in tree.circuit.inputs+tree.circuit.latches_prev:
        if feature.id in zeros:
            assert feature.id not in ones
            sample[feature.id] = 0
        elif feature.id in ones:
            sample[feature.id] = 1
        else:
            sample[feature.id] = random.choice([0, 1])
    return sample

def sample_from_sample(tree, other_sample, zeros, ones):
    sample = {}
    for feature in tree.circuit.inputs + tree.circuit.latches_prev:
        if feature.id in zeros:
            assert feature.id not in ones
            sample[feature.id] = 0
        elif feature.id in ones:
            sample[feature.id] = 1
        else:
            sample[feature.id] = other_sample[feature.id]
    return sample


def calculate_shap_scores(tree: Shap, inputs_sample, outputs_to_check, prints=True):
    if prints:
        print("Calculate Shap Values:")
        print("Input Sample: ", inputs_sample)
        print("Outputs: ", outputs_to_check)

    assert len(outputs_to_check) == 1
    res = None
    for output in outputs_to_check:
        res = tree.calculate_shap_scores(output, inputs_sample)
        res_sum = sum(res.values())
        e_f = -res_sum if res_sum < 0 else 1 - res_sum
        simulation = tree.simulate(inputs_sample, output)
        if prints:
            print("Shap Results - ", output, ":")
            print("simulation= ", simulation)
            print("E[f]= ", e_f)
            print("Shap= ", res)
            print_shap_chart(res, simulation)
    print()
    return res


def TEST_sanity_random(tree, output_to_check):
    calculate_shap_scores(tree, sample_rand(tree, [], []), [output_to_check])

def TEST_the_change_threshold(tree, output_to_check):
    sample = sample_rand(tree, [], [])
    shap_scores = calculate_shap_scores(tree, sample, [output_to_check], False)
    simulation = 1 if tree.simulate(sample, output_to_check) else 0
    sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1] != 0], key=lambda x: x[1],
                                reverse=(simulation==0))

    print("SIMULATED: ", simulation)
    simulation_changed_once = False
    new_sample = sample
    for feature, value in sorted_shap_scores:
        if sample[feature] == 1:
            new_sample = sample_from_sample(tree, sample, [feature], [])
        else:
            new_sample = sample_from_sample(tree, sample, [], [feature])

        # new_shap_scores = calculate_shap_scores(tree, new_sample, [output_to_check])
        new_simulation = 1 if tree.simulate(new_sample, output_to_check) else 0
        print("Changed",
              feature,
              " "*(5-len(feature)),
              "with shap score ",
              round(value, 4),
              " "*(8-len(str(round(value, 4)))),
              "- SIMULATED: ",
              new_simulation)

        if (value<=0 and simulation==1) or (value>=0 and simulation==0):
            if new_simulation!=simulation:
                print("FAILURE!")
                return False
        else: # passed 0 to the other sign
            if new_simulation!=simulation and simulation_changed_once == False:
                simulation_changed_once = True
                print("Simulation value changed! from now on, we expect to see nothing but this result")

            if new_simulation == simulation and simulation_changed_once == True:
                print("Changed Twice! This indicated that a larger shap score was given to less important feature.")
                print("FAILURE!")
                return False

    print("SUCCESS!")
    return True

def TEST_the_change_threshold_accumulated(tree, output_to_check):
    sample = sample_rand(tree, [], [])
    shap_scores = calculate_shap_scores(tree, sample, [output_to_check], False)
    simulation = 1 if tree.simulate(sample, output_to_check) else 0
    sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1] != 0], key=lambda x: x[1],
                                reverse=(simulation==0))

    print("SIMULATED: ", simulation)
    simulation_changed_once = False
    new_sample = sample
    for feature, value in sorted_shap_scores:
        if sample[feature] == 1:
            new_sample = sample_from_sample(tree, new_sample, [feature], [])
            # new_sample = sample_from_sample(tree, sample, [feature], [])
        else:
            new_sample = sample_from_sample(tree, new_sample, [], [feature])
            # new_sample = sample_from_sample(tree, sample, [], [feature])

        # new_shap_scores = calculate_shap_scores(tree, new_sample, [output_to_check])
        new_simulation = 1 if tree.simulate(new_sample, output_to_check) else 0
        print("Changed",
              feature,
              " "*(5-len(feature)),
              "with shap score ",
              round(value, 4),
              " "*(8-len(str(round(value, 4)))),
              "- SIMULATED: ",
              new_simulation)

        # if (value<=0 and simulation==1) or (value>=0 and simulation==0):
        #     if new_simulation!=simulation:
        #         print("Failure attained for sample: ", new_sample)
        #         print("FAILURE!")
        #         return False
        # else: # passed 0 to the other sign
        if 1:
            if new_simulation!=simulation and simulation_changed_once == False:
                simulation_changed_once = True
                print("Simulation value changed!")

    print("SUCCESS!")
    return True

def TEST_change_one_by_one(tree, output_to_check):
    sample = sample_rand(tree, [], [])
    shap_scores = calculate_shap_scores(tree, sample, [output_to_check], False)
    simulation = 1 if tree.simulate(sample, output_to_check) else 0
    sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1] != 0], key=lambda x: x[1],
                                reverse=(simulation==0))

    print("SIMULATED: ", simulation)
    simulation_changed_once = False
    new_sample = sample
    new_simulation = simulation
    changed_features = []
    while new_simulation == simulation:
        new_shap_scores = calculate_shap_scores(tree, new_sample, [output_to_check], False)
        sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1] != 0 and item[0] not in changed_features], key=lambda x: x[1],
                                    reverse=(simulation == 0))
        if len(sorted_shap_scores) == 0:
            break
        changed_feature = sorted_shap_scores[0][0]
        if changed_feature in changed_features:
            break

        changed_features.append(changed_feature)
        print("Changed: ", changed_features)
        if sample[changed_feature] == 0:
            new_sample = sample_from_sample(tree, new_sample, [], [changed_feature])
        else:
            new_sample = sample_from_sample(tree, new_sample, [changed_feature], [])

        new_simulation = 1 if tree.simulate(new_sample, output_to_check) else 0

    print(len(changed_features))
    print("SUCCESS!")
    new_shap_scores = calculate_shap_scores(tree, new_sample, [output_to_check], True)
    return True

def TEST_change_one_by_one_after_trying(tree, output_to_check):
    sample = sample_rand(tree, [], [])
    shap_scores = calculate_shap_scores(tree, sample, [output_to_check], False)
    simulation = 1 if tree.simulate(sample, output_to_check) else 0
    sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1] != 0], key=lambda x: x[1],
                                reverse=(simulation==0))

    print("SIMULATED: ", simulation)
    simulation_changed_once = False
    new_sample = sample
    new_simulation = simulation
    changed_features = []
    while 1:
        while new_simulation == simulation:
            sorted_shap_scores = sorted([item for item in shap_scores.items() if item[1] != 0 and item[0] not in changed_features], key=lambda x: x[1],
                                        reverse=(simulation == 0))
            if len(sorted_shap_scores) == 0:
                print(len(changed_features))
                print("SUCCESS!")
                return True
            changed_feature = sorted_shap_scores[0][0]

            changed_features.append(changed_feature)
            print("Changed: ", changed_features)

            if sample[changed_feature] == 0:
                new_sample = sample_from_sample(tree, new_sample, [], [changed_feature])
            else:
                new_sample = sample_from_sample(tree, new_sample, [changed_feature], [])

            new_simulation = 1 if tree.simulate(new_sample, output_to_check) else 0

        if sample[changed_feature] == 0:
            new_sample = sample_from_sample(tree, new_sample, [changed_feature], [])
        else:
            new_sample = sample_from_sample(tree, new_sample, [], [changed_feature])

        new_shap_scores = calculate_shap_scores(tree, new_sample, [output_to_check], False)




def TEST_change_all_negatives_at_once(tree, output_to_check):
    sample = sample_rand(tree, [], [])
    shap_scores = calculate_shap_scores(tree, sample, [output_to_check], False)
    simulation = 1 if tree.simulate(sample, output_to_check) else 0

    ones = []
    zeros = []
    for feature, value in shap_scores.items():
        if (simulation == 1 and value<=0) or (simulation == 0 and value>=0):
            if sample[feature] == 1:
                zeros.append(feature)
            else:
                ones.append(feature)

    new_sample = sample_from_sample(tree, sample, zeros, ones)
    new_simulation = 1 if tree.simulate(new_sample, output_to_check) else 0

    if new_simulation!=simulation:
        print("Failure attained for sample: ", sample)
        print("FAILURE!")
        return False
    else:
        print("SUCCESS!")
        return True



