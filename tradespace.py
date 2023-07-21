#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import itertools
import json


class TradespaceDesigner:
    def __init__(self):

        # performance items dict that will be added by the user
        self.performance_items = {}

        # design components dict that will be added by the user
        self.design_components = {}

        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):

        # add performance variable to the dict
        self.performance_items[name] = {'min_value': min_value,
                                        'max_value': max_value,
                                        'units': units,
                                        'weight': weight}
        return

    def add_design_component(self, component_dict):

        # append the name and attributes to the design components dict on the category key
        name = component_dict['name']
        category = component_dict['category']
        attributes_dict = component_dict['attributes']

        # Check if the name already exists in the design components dictionary
        if name in self.design_components:
            print(
                f"Warning: {name} already exists in the design components dictionary and will be overwritten")
            self.design_components[name] = {
                'category': category, 'attributes': attributes_dict}
        else:
            # If the name does not exist, add the category and attributes to it
            self.design_components[name] = {
                'category': category, 'attributes': attributes_dict}

        return

    def get_attr_by_name(self, name, attribute):
        if self.design_components is None:
            raise Exception("Warning: No design components have been added. Please add design components before calling this function")

        if name not in self.design_components:
            raise Exception(f"Warning: {name} not found in the design components dictionary")

        if attribute not in self.design_components[name]['attributes']:
            raise Exception(f"Warning: {attribute} not found in the attributes dictionary for {name}")

        return self.design_components[name]['attributes'][attribute]['value']

    def sum_attributes_by_category(self, category: str, attribute: str):
        if self.design_components is None:
            raise Exception("Warning: No design components have been added. Please add design components before calling this function")

        # get categories
        categories = list(dict.fromkeys(
            [self.design_components[option]['category'] for option in self.design_components]))

        if category not in categories:
            raise Exception(f"Warning: {category} not found in the categories dictionary")

        # get attribute keys
        attributes = list(dict.fromkeys(
            [self.design_components[option]['attributes'][attribute] for option in self.design_components if self.design_components[option]['category'] == category]))

        if attribute not in attributes:
            raise Exception(f"Warning: {attribute} not found in the attributes dictionary for {category}")

        # get the sum of the attributes
        return sum([self.get_attr_by_name(option, attribute) for option in self.design_components if self.design_components[option]['category'] == category])

    def sum_attributes_by_names(self, names: list, attribute: str):

        # get attribute keys
        attributes = list(dict.fromkeys(
            [self.design_components[option]['attributes'][attribute] for option in self.design_components if option in names]))

        if attribute not in attributes:
            raise Exception(f"Warning: {attribute} not found in the attributes dictionary for {names}")

        # get the sum of the attributes
        return sum([self.get_attr_by_name(option, attribute) for option in self.design_components if option in names])

    def generate_tradespace(self):

        # Get the unique categories with the same order as the design variables
        categories = list(dict.fromkeys(
            [self.design_components[option]['category'] for option in self.design_components]))

        # Generate the unique combinations of the design variable options
        components_by_category = [
            [option for option in self.design_components if self.design_components[option]['category'] == category] for category in categories]
        tradespace_data = list(itertools.product(*components_by_category))

        # Create a pandas DataFrame from the tradespace data
        self.tradespace_df = pd.DataFrame(tradespace_data, columns=categories)

        return

    def save_components_to_json(self, filename):

        if self.design_components is None:
            raise Exception("Warning: No design components have been added. Please add design components before calling this function")

        with open(filename, 'w') as f:
            json.dump(self.design_components, f, indent=4)

        return


    def calculate_sau(self):

        # iterate over the performance variables
        for name, item in self.performance_items.items():

            # calculate the SAU with a linear function
            self.tradespace_df['SAU_' + name] = (self.tradespace_df[name] - item['min_value']) / (
                item['max_value'] - item['min_value'])

    def calculate_mau(self):

        self.tradespace_df['MAU'] = 0
        for name, item in self.performance_items.items():
            self.tradespace_df['MAU'] += item['weight'] * \
                self.tradespace_df['SAU_' + name]

    def save_tradespace(self, filename):

        if self.tradespace_df is None:
            raise Exception("Warning: No tradespace has been generated. Please generate a tradespace before calling this function")
        self.tradespace_df.to_csv(filename, index=True)

        return

    def plot_tradespace(self, x_name, y_name, block=True, labels=False, hexbin=True):

        # Plot the Maximum Payload vs MAU
        fig, ax = plt.subplots()
        ax.scatter(
            self.tradespace_df[x_name], self.tradespace_df[y_name], s=50, c='b', marker="s", label=y_name)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)

        # # Add labels for each point
        if labels:
            for i, row in self.tradespace_df.iterrows():
                ax.annotate(f"ID: {i}", (row[x_name], row[y_name]), textcoords="offset points", xytext=(
                    0, 10), ha='center')

        # Show the legend and plot the figure
        ax.legend()

        if hexbin:
            ax.hexbin(
                self.tradespace_df[x_name], self.tradespace_df[y_name], gridsize=20, cmap='Blues')

        plt.show(block=block)

    def plot_tradespace_plotly(self, x_name, y_name):

        # Create the scatter plot
        pareto_fig = go.Figure(data=go.Scatter(
            x=self.tradespace_df[x_name],
            y=self.tradespace_df[y_name],
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
        pareto_fig.update_layout(
            xaxis=dict(title=x_name),
            yaxis=dict(title=y_name),
            showlegend=False
        )

        df = self.tradespace_df

        # Create a Plotly Table figure
        csv_fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
            cells=dict(values=[df[col] for col in df.columns], fill_color='lavender', align='left'))
        ])

        # Set the layout of the subplots
        csv_fig.update_layout(title='Drone Designer')

        # Show the figure
        # csv_fig.show()
        pareto_fig.show()
