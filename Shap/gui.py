import tkinter as tk

import utilis

def on_submit(inputs_entries, output_vars, tree):
    inputs_sample = {}
    for input, entry in inputs_entries.items():
        value = entry.get()
        if value == '':
            value = 0
        else:
            assert value == '0' or value == '1'
            value = int(value)
        inputs_sample[input] = value

    outputs_to_check = []
    for output, var in output_vars.items():
        if var.get() == 1:
            outputs_to_check.append(output)

    utilis.calculate_shap_scores(tree, inputs_sample, outputs_to_check)

def open_gui(inputs, outputs, tree, init_sample={}):
    # Initialize the main window
    root = tk.Tk()
    root.title("FVShap")

    # Create a Canvas widget
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a Scrollbar widget linked to the Canvas
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a Frame to hold the content inside the Canvas
    content_frame = tk.Frame(canvas)
    content_frame2 = tk.Frame(canvas)

    # Create a window inside the Canvas to place the Frame
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    # Configure the scrollbar to update the Canvas view
    canvas.configure(yscrollcommand=scrollbar.set)

    # Update the scroll region of the Canvas to fit the content
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", on_frame_configure)


    # Output selection section
    tk.Label(content_frame, text="Choose Outputs:").grid(row=0, column=0, sticky=tk.W)

    output_vars = {}
    for i, label in enumerate(outputs, start=1):
        var = tk.IntVar()
        tk.Checkbutton(content_frame, text=label, variable=var).grid(row=i, column=0, sticky=tk.W)
        output_vars[label] = var

    # Calculate button
    tk.Button(content_frame, text="Calculate", command=lambda: on_submit(input_entries, output_vars, tree)).grid(row= len(outputs) + 1, column=0,
                                                              columnspan=2)


    # Input values section
    tk.Label(content_frame, text="Enter input values:").grid(row=len(outputs) + 2, column=0, sticky=tk.W)

    input_entries = {}
    for i, label in enumerate(inputs, start=len(inputs) + 3):
        tk.Label(content_frame, text=label).grid(row=i, column=0, sticky=tk.W)
        entry = tk.Entry(content_frame)
        entry.grid(row=i, column=1)
        input_entries[label] = entry
        if label in init_sample.keys():
            entry.insert(0, str(init_sample[label]))

    # Start the GUI event loop
    root.mainloop()
