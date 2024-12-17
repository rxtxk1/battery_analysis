import plotly.express as px

# Plot Re vs Cycle Number
def plot_re_vs_cycle(data):
    fig = px.scatter(data, x="Cycle_Number", y="Re", title="Re vs Cycle Number", labels={"Cycle_Number": "Cycle Number", "Re": "Estimated Electrolyte Resistance (Ohms)"})
    fig.show()

# Plot Rct vs Cycle Number
def plot_rct_vs_cycle(data):
    fig = px.scatter(data, x="Cycle_Number", y="Rct", title="Rct vs Cycle Number", labels={"Cycle_Number": "Cycle Number", "Rct": "Estimated Charge Transfer Resistance (Ohms)"})
    fig.show()
