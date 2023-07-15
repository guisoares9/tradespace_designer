#!/usr/bin/env python3

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

    # def add_design_variable(self, name, units, options):

    #     # add design variable to the dict
    #     self.design_variables[name] = {'units': units, 'options': options}
    #     return

    def generate_tradespace(self):

        # Get the names and options of the design variables
        design_variable_names = list(self.design_variables.keys())
        design_variable_options = [
            self.design_variables[name]['options'] for name in design_variable_names]

        # Generate the unique combinations of the design variable options
        tradespace_data = list(itertools.product(*design_variable_options))

        # Create a pandas DataFrame from the tradespace data
        self.tradespace_df = pd.DataFrame(
            tradespace_data, columns=design_variable_names)

        return

    def calculate_sau(self):

        # iterate over the performance variables
        for name, item in self.performance_items.items():

            # calculate the SAU with a linear function
            self.tradespace_df[name + '_SAU'] = (self.tradespace_df[name] - item['min_value']) / (
                item['max_value'] - item['min_value'])

    def calculate_mau(self):

        self.tradespace_df['MAU'] = 0
        for name, item in self.performance_items.items():
            self.tradespace_df['MAU'] += item['weight'] * \
                self.tradespace_df[name + '_SAU']

    def plot_tradespace(self, x_name, y_name, block=True, labels=False, hexbin=True):

        # Plot the Maximum Payload vs MAU
        fig, ax = plt.subplots()
        ax.scatter(
            designer.tradespace_df[x_name], designer.tradespace_df[y_name], s=50, c='b', marker="s", label=y_name)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)

        # # Add labels for each point
        if labels:
            for i, row in designer.tradespace_df.iterrows():
                ax.annotate(f"ID: {i}", (row[x_name], row[y_name]), textcoords="offset points", xytext=(
                    0, 10), ha='center')

        # Show the legend and plot the figure
        ax.legend()

        if hexbin:
            ax.hexbin(
                designer.tradespace_df[x_name], designer.tradespace_df[y_name], gridsize=20, cmap='Blues')

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
