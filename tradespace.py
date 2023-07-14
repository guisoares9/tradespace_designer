import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

class TradespaceDesigner:
    def __init__(self):

        # performance items dict that will be added by the user
        self.performance_items = {}

        # design variables dict that will be added by the user
        self.design_variables = {}

        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):

        # add performance variable to the dict
        self.performance_items[name] = {'min_value': min_value,
                                        'max_value': max_value,
                                        'units': units,
                                        'weight': weight}
        return

    def add_design_variable(self, name, units, options):

        # add design variable to the dict
        self.design_variables[name] = {'units': units, 'options': options}
        return

    def generate_tradespace(self):

        # Get the names and options of the design variables
        design_variable_names = list(self.design_variables.keys())
        design_variable_options = [self.design_variables[name]['options'] for name in design_variable_names]

        # Generate the unique combinations of the design variable options
        tradespace_data = list(itertools.product(*design_variable_options))

        # Create a pandas DataFrame from the tradespace data
        self.tradespace_df = pd.DataFrame(tradespace_data, columns=design_variable_names)

        return

    def calculate_sau(self):

        # iterate over the performance variables
        for name, item in self.performance_items.items():

            # calculate the SAU with a linear function
            self.tradespace_df[name + '_SAU'] = (self.tradespace_df[name] - item['min_value']) / (item['max_value'] - item['min_value'])

    def calculate_mau(self):

        self.tradespace_df['MAU'] = 0
        for name, item in self.performance_items.items():
            self.tradespace_df['MAU'] += item['weight'] * self.tradespace_df[name + '_SAU']

    def plot_tradespace(self, x_name, y_name, block=True, labels=False, hexbin=True):

        # Plot the Maximum Payload vs MAU
        fig, ax = plt.subplots()
        ax.scatter(designer.tradespace_df[x_name], designer.tradespace_df[y_name], s=50, c='b', marker="s", label=y_name)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)

        # # Add labels for each point
        if labels:
            for i, row in designer.tradespace_df.iterrows():
                ax.annotate(f"ID: {i}", (row[x_name], row[y_name]), textcoords="offset points", xytext=(0, 10), ha='center')

        # Show the legend and plot the figure
        ax.legend()

        if hexbin:
            ax.hexbin(designer.tradespace_df[x_name], designer.tradespace_df[y_name], gridsize=20, cmap='Blues')

        plt.show(block=block)
    
    def plot_tradespace_plotly(self, x_name, y_name):
        import plotly.graph_objects as go

        # Create the scatter plot
        fig = go.Figure(data=go.Scatter(
            x=designer.tradespace_df[x_name],
            y=designer.tradespace_df[y_name],
            mode='markers',
            marker=dict(
                size=10,
                color='blue',
                symbol='square'
            ),
            text=[f'ID: {i}' for i in range(len(self.tradespace_df))],
            hovertemplate='<b>%{text}</b><br><br>%{xaxis.title.text}: %{x}<br>%{yaxis.title.text}: %{y}<extra></extra>'
        ))

        # Update the layout
        fig.update_layout(
            xaxis=dict(title=x_name),
            yaxis=dict(title=y_name),
            showlegend=False
        )

        # Show the plot
        fig.show()

# Define your performance variables
designer = TradespaceDesigner()

# Add performance variables
# Add maximum flight distance
designer.add_performance_variable("Maximum Flight Distance", 1, 100, "km", 0.33)

# Add maximum speed
designer.add_performance_variable("Maximum Speed", 10, 250, "m/s", 0.33)

# Add maximum payload
designer.add_performance_variable("Maximum Payload", 0.4, 5, "kg", 0.33)

# Add design variables
# Add battery capacity
designer.add_design_variable("Battery Capacity", "mAh", [2500, 3000, 3500, 4000, 4500])

# Add battery voltage
designer.add_design_variable("Battery Voltage", "V", [11.1, 14.8, 18.5, 22.2])

# Add number of battery
designer.add_design_variable("Number of Batteries", "unit", [1, 2, 3])

# Add number of motors
designer.add_design_variable("Number of Motors", "unit", [4, 6, 8])

# Add motor thrust
designer.add_design_variable("Motor Thrust", "N", [3, 4, 5, 6, 7])

# Generate the tradespace
df = designer.generate_tradespace()

# Define the performance formulas
designer.tradespace_df["Maximum Flight Distance"] = 20
designer.tradespace_df["Maximum Payload"] = designer.tradespace_df['Number of Motors'] * designer.tradespace_df['Motor Thrust'] / (9.81 * 1) - designer.tradespace_df['Number of Batteries'] * 0.5
designer.tradespace_df["Maximum Speed"] = 50

# calculate cost
designer.tradespace_df["Cost"] = designer.tradespace_df['Number of Motors'] * 10 + designer.tradespace_df['Number of Batteries'] * 20 + designer.tradespace_df['Battery Capacity'] * designer.tradespace_df['Battery Voltage'] / 1000

# Calculate the SAU
designer.calculate_sau()

# Calculate the MAU
designer.calculate_mau()

# Save the tradespace to a CSV file
designer.tradespace_df.to_csv('tradespace.csv', index=True)

# designer.plot_tradespace('Cost', 'MAU')

designer.plot_tradespace_plotly('Cost', 'MAU')
