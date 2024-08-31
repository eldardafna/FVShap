import tkinter as tk
from Tree.AAGTree import AAGTree

def on_submit(inputs_entries, output_vars, tree):
    inputs_sample = {}
    for input, entry in inputs_entries.items():
        value = entry.get()
        if value == '':
            value = 0
        else:
            assert value=='0' or value=='1'
            value = int(value)
        inputs_sample[input] = value

    outputs_to_check = []
    for output, var in output_vars.items():
        if var.get() == 1:
            outputs_to_check.append(output)

    print("Calculate Shap Values:")
    print("Input Sample: ", inputs_sample)
    print("Outputs: ", outputs_to_check)
    for output in outputs_to_check:
        res = tree.shap_scores(features=inputs_entries.keys(),
                               features_sample=inputs_sample,
                               output_to_check=output)
        print(output, ": ", res)
    print()

def open_gui(inputs, outputs, tree):
    # Initialize the main window
    root = tk.Tk()
    root.title("FVShap")

    # Input values section
    tk.Label(root, text="Enter input values:").grid(row=0, column=0, sticky=tk.W)

    input_entries = {}
    for i, label in enumerate(inputs, start=1):
        tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.W)
        entry = tk.Entry(root)
        entry.grid(row=i, column=1)
        input_entries[label] = entry

    # Output selection section
    tk.Label(root, text="Choose Outputs:").grid(row=len(inputs) + 1, column=0, sticky=tk.W)

    output_vars = {}
    for i, label in enumerate(outputs, start=len(inputs) + 2):
        var = tk.IntVar()
        tk.Checkbutton(root, text=label, variable=var).grid(row=i, column=0, sticky=tk.W)
        output_vars[label] = var

    # Calculate button
    tk.Button(root, text="Calculate", command=lambda: on_submit(input_entries, output_vars, tree)).grid(row=len(inputs) + len(outputs) + 2, column=0,
                                                              columnspan=2)

    # Start the GUI event loop
    root.mainloop()
