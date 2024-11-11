import matplotlib.pyplot as plt
import numpy as np


def shap_waterfall(data, base_value=0, highlight_color='dodgerblue', color_positive='green', color_negative='red'):
    # Extract names and values from the dictionary
    names = list(data.keys())
    values = np.array(list(data.values()))

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
    ax.set_yticklabels(['Base'] + names + ['Shap Output'])

    # Remove spines and set grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Title and labels
    ax.set_xlabel('Value')
    ax.set_title('SHAP-like Horizontal Waterfall Chart')

    plt.show()


# Example data dictionary
data = {
    'Feature 1': 100,
    'Feature 2': -30,
    'Feature 3': 20,
    'Feature 4': -10,
    'Feature 5': 50,
    'Feature 6': -20
}

shap_waterfall(data, base_value=50)
