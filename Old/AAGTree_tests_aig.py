from AAGTree import AAGTree
from shap import plots

# aag = AAGTree('../aag/bad_state.aag')
# aag.circuit.print()

# aag = AAGTree('../aag/coverted_aig/miim.aag')
aag = AAGTree('../aag/coverted_aig/h_TreeArb.aag')
# aag.circuit.print()
sample = {feature.id: 0 for feature in aag.circuit.inputs+aag.circuit.latches_prev}
output_to_check = aag.circuit.bad_states[0].id

shap = aag.shap_scores(features=[input.id for input in aag.circuit.inputs+aag.circuit.latches_prev],
                        features_sample=sample,
                        output_to_check=output_to_check)

print({input: round(value, 4) for input, value in shap.items() if value!=0})

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Example data
data = {
    'Category': [key for key in shap.keys() if shap[key]!=0],
    'Value': [value for value in shap.values() if value!=0],
}

df = pd.DataFrame(data)
df['Cumulative'] = df['Value'].cumsum()
df['Start'] = df['Cumulative'].shift(1).fillna(0)

# Plotting the horizontal waterfall chart
fig, ax = plt.subplots(figsize=(10, 6))

for i in range(len(df)):
    ax.barh(df['Category'][i], df['Value'][i], left=df['Start'][i],
            color='cyan' if df['Value'][i] >= 0 else 'pink')

ax.set_xlabel('Value')
ax.set_ylabel('Category')
ax.set_title('Horizontal Waterfall Chart')

plt.show()



