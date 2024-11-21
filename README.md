# Shap API

The `Shap` class provides functionality for calculating SHAP (Shapley Additive Explanations) scores for boolean functions represented as AAG\AIG\CNF files. It implements the algorithm in the following article: https://arxiv.org/pdf/2007.14045 
It supports various modes to use the algorithm with a composable ciruit. 

## Features
- Supports input files in AAG, AIG, and CNF formats.
- Parses AAG files into a tree structure for easier manipulation and score calculation.
- Provides two modes for handling decomposability:
  - **VARIABLE_INSTANCES_AS_PLAYERS**: Treats each variable instance as a different player.
  - **CHANGE_TO_AVERAGE_GATE**: Interprets composable AND gates as AVERAGE gates for polynomial time computation. An AVERAGE gate is similar to the AND gate - it gets two inputs and outputs 0 if both inputs are false, 1 if both are true, and 0.5 if only one input is true.
- Computes SHAP scores for boolean functions.

## External Tools
- AIG-to-AAG conversion tool (`aigtoaig`\'aiger')

### File Formats

- **AAG (And-Inverter Graph)**: A standard format for representing boolean functions. The input file should be in AAG format.
- **AIG (And-Inverter Graph)**: An alternative format to AAG. The tool will automatically convert AIG files to AAG format. Used in HWMCC.
- **CNF (Conjunctive Normal Form)**: Another representation of boolean functions, which can also be converted to AAG format.

## Usage

### Initialization
To initialize the `Shap` object, provide the path to an AAG, AIG, or CNF file. You should also specify the mode for handling decomposability.

Example initialization:

```python
shap_instance = Shap(path="path_to_file.aag", mode="VARIABLE_INSTANCES_AS_PLAYERS")
```

## Modes
There are two modes available for handling decomposability:
1. **VARIABLE_INSTANCES_AS_PLAYERS**: Treats each variable instance as a distinct player when calculating SHAP scores.
2. **CHANGE_TO_AVERAGE_GATE**: Interprets composable AND gates as average gates, simplifying calculations.

You can specify the mode when initializing the `Shap` class. The default is `"VARIABLE_INSTANCES_AS_PLAYERS"`.

### Methods

#### `print(root_to_print=None)`
Prints the tree structure. You can optionally specify a root to print. Default prints the whole circuit, which is not recommended for big circuits.

##### Variable Naming Convention
When printing the tree structure, the variables are named using a specific template: **[letter][number]**. The **letter** represents the variable type, and the **number** is the variable's identifier.

##### Variable Types:
- **i**: Input
- **o**: Output
- **lp**: Latch (previous state)
- **ln**: Latch (next state)
- **b**: Bad state

For example:
- `i1`: Input variable with ID 1
- `o0`: Output variable with ID 0
- `lp3`: Latch previous state variable with ID 3
- `ln2`: Latch next state variable with ID 2
- `b5`: Bad state variable with ID 5

#### `simulate(variables_assignment, root_to_simulate=None)`
Simulates an output with the provided variable assignments. Returns 0 (False) or 1 (True).

#### `get_sample(default_value=0, ones=[], zeros=[], dict={})`
Generates a sample of variable assignments, in order to preserve the format of the assignment. You can specify:
- `ones`: Variables that should be assigned a value of 1.
- `zeros`: Variables that should be assigned a value of 0.
- `dict`: A dictionary of custom variable assignments.
- `default value`: the rest of the model's inputs which weren't specified in 'ones', 'zeros' or 'dict' would be assigned with this value. Default is 0.

#### `calculate_shap_scores(root_to_shap, variables_assignment)`
Calculates SHAP scores for a specific output (`root_to_shap`) and a specifit variable_assignment. The variable assignments must be provided as a dictionary, where the keys are variable IDs and the values are either 0 or 1. You should use 'get_sample' method to get this assignment.


### Example

Example usage of the Shap API:

```python
# Initialize the Shap instance with a sample AAG file
shap_instance = Shap(path="path_to_file.aag", mode="CHANGE_TO_AVERAGE_GATE")

# Print the tree structure
shap_instance.print()

# Generate a sample of variable assignments
sample = shap_instance.get_sample(default_value=0, ones=['i1', 'i2'])
print(sample)

# Simulate with the sample assignments
shap_instance.simulate(sample)

# Calculate SHAP scores for a specific output node
shap_scores = shap_instance.calculate_shap_scores('b0', sample)
print(shap_scores)
```

