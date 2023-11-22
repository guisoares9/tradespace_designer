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

        # initialize tradespace dataframe
        self.tradespace_df = pd.DataFrame()

        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):
        # check if the name already exists in the performance items dictionary
        if name in self.performance_items:
            print(
                f"Warning: {name} already exists in the performance items dictionary and will be overwritten"
            )

        # check if max value is greater than min value
        if max_value < min_value:
            raise Exception(
                f"Warning: {name} has a max value that is less than the min value. Please change the values to calculate the SAU"
            )

        # check if the weight is between 0 and 1
        if weight < 0 or weight > 1:
            raise Exception(
                f"Warning: {name} has a weight that is not between 0 and 1. Please change the values to calculate the MAU"
            )

        # check if the sum of the weights is higher than 1
        if sum([item["weight"] for item in self.performance_items.values()]) + weight > 1:
            raise Exception(
                f"Warning: {name} has a weight that is too high. Please change the values to calculate the MAU"
            )

        # add performance variable to the dict
        self.performance_items[name] = {
            "min_value": min_value,
            "max_value": max_value,
            "units": units,
            "weight": weight,
        }
        return

    def add_design_component(self, component_dict):
        # append the name and attributes to the design components dict on the category key
        name = component_dict["name"]
        category = component_dict["category"]
        attributes_dict = component_dict["attributes"]

        # Check if the name already exists in the design components dictionary
        if name in self.design_components:
            print(
                f"Warning: {name} already exists in the design components dictionary and will be overwritten"
            )
            self.design_components[name] = {
                "category": category,
                "attributes": attributes_dict,
            }
        else:
            # If the name does not exist, add the category and attributes to it
            self.design_components[name] = {
                "category": category,
                "attributes": attributes_dict,
            }

        return

    def get_attr_by_name(self, name, attribute):
        if self.design_components is None:
            raise Exception(
                "Warning: No design components have been added. Please add design components before calling this function"
            )

        if name not in self.design_components:
            raise Exception(
                f"Warning: {name} not found in the design components dictionary"
            )

        if attribute not in self.design_components[name]["attributes"]:
            raise Exception(
                f"Warning: {attribute} not found in the attributes dictionary for {name}"
            )

        return self.design_components[name]["attributes"][attribute]["value"]

    def sum_attributes_by_category(self, category: str, attribute: str):
        if self.design_components is None:
            raise Exception(
                "Warning: No design components have been added. Please add design components before calling this function"
            )

        # get categories
        categories = list(
            dict.fromkeys(
                [
                    self.design_components[option]["category"]
                    for option in self.design_components
                ]
            )
        )

        if category not in categories:
            raise Exception(
                f"Warning: {category} not found in the categories dictionary"
            )

        # get attribute keys
        attributes = list(
            dict.fromkeys(
                [
                    self.design_components[option]["attributes"][attribute]
                    for option in self.design_components
                    if self.design_components[option]["category"] == category
                ]
            )
        )

        if attribute not in attributes:
            raise Exception(
                f"Warning: {attribute} not found in the attributes dictionary for {category}"
            )

        # get the sum of the attributes
        return sum(
            [
                self.get_attr_by_name(option, attribute)
                for option in self.design_components
                if self.design_components[option]["category"] == category
            ]
        )

    def sum_attributes_by_names(self, names: list, attribute: str):
        # get attribute keys
        attributes = list(
            dict.fromkeys(
                [
                    self.design_components[option]["attributes"][attribute]
                    for option in self.design_components
                    if option in names
                ]
            )
        )

        if attribute not in attributes:
            raise Exception(
                f"Warning: {attribute} not found in the attributes dictionary for {names}"
            )

        # get the sum of the attributes
        return sum(
            [
                self.get_attr_by_name(option, attribute)
                for option in self.design_components
                if option in names
            ]
        )

    def generate_design_tradespace(self):
        # Get the unique categories with the same order as the design variables
        categories = list(
            dict.fromkeys(
                [
                    self.design_components[option]["category"]
                    for option in self.design_components
                ]
            )
        )

        # Generate the unique combinations of the design variable options
        components_by_category = [
            [
                option
                for option in self.design_components
                if self.design_components[option]["category"] == category
            ]
            for category in categories
        ]
        tradespace_data = list(itertools.product(*components_by_category))

        # Create a pandas DataFrame from the tradespace data
        self.tradespace_df = pd.DataFrame(tradespace_data, columns=categories)

        return

    def save_components_to_json(self, filename):
        if self.design_components is None:
            raise Exception(
                "Warning: No design components have been added. Please add design components before calling this function"
            )

        with open(filename, "w") as f:
            json.dump(self.design_components, f, indent=4)

        return

    def calculate_sau(self, clip_max=True, clip_min=True):
        # iterate over the performance variables
        for name, item in self.performance_items.items():

            # check if the max value is greater than the max value in the tradespace
            if self.tradespace_df[name].max() > item["max_value"] and not clip_max:
                raise Exception(
                    f"Warning: {name} has a max value that is less than the max value in the tradespace. Please change the values to calculate the SAU or set clip_max to True"
                )
            elif self.tradespace_df[name].max() > item["max_value"] and clip_max:
                # set 1 to only where the max value is greater than the max value in the tradespace
                self.tradespace_df.loc[self.tradespace_df[name] > item["max_value"], "sau_" + name] = 1.0

            # check if the min value is less than the min value in the tradespace
            if self.tradespace_df[name].min() < item["min_value"] and not clip_min:
                raise Exception(
                    f"Warning: {name} has a min value that is greater than the min value in the tradespace. Please change the values to calculate the SAU or set clip_min to True"
                )
            elif self.tradespace_df[name].min() < item["min_value"] and clip_min:
                # set 0 to only where the min value is less than the min value in the tradespace
                self.tradespace_df.loc[self.tradespace_df[name] < item["min_value"], "sau_" + name] = 0.0
            
            good_values = (self.tradespace_df[name] <= item["max_value"]) & (self.tradespace_df[name] >= item["min_value"])
            # calculate the SAU with a linear function
            self.tradespace_df.loc[good_values, "sau_" + name] = (
                self.tradespace_df[name] - item["min_value"]
            ) / (item["max_value"] - item["min_value"])

    def calculate_mau(self, restrictive=True):
        self.tradespace_df["mau"] = 0
        for name, item in self.performance_items.items():
            
            # check if the SAU is zero and zero out the MAU
            if restrictive:
                self.tradespace_df.loc[self.tradespace_df["sau_" + name] == 0, "mau"] = 0.0
            
            self.tradespace_df["mau"] += (
                item["weight"] * self.tradespace_df["sau_" + name]
            )

    def generate_performance_tradespace(self, clip_max=True, clip_min=True, restrictive=True):
        # check if the tradespace has been generated
        if self.tradespace_df is None:
            raise Exception(
                "Warning: No tradespace has been generated. Please generate a tradespace before calling this function"
            )

        # calculate the SAU
        self.calculate_sau(clip_max=clip_max, clip_min=clip_min)

        # calculate the MAU
        self.calculate_mau(restrictive=restrictive)

        # calculate the pareto front
        self.detect_pareto()

        return

    def save_tradespace(self, filename):
        if self.tradespace_df is None:
            raise Exception(
                "Warning: No tradespace has been generated. Please generate a tradespace before calling this function"
            )
        self.tradespace_df.to_csv(filename, index=True)

        return

    def detect_pareto(self, x_name='price', y_name='mau'):

        for index, row in self.tradespace_df.iterrows():

            # get the x axis of the pareto search space
            x = row[x_name]
            y = row[y_name]

            # check if y is zero
            if y == 0:
                row['pareto'] = False
                continue

            # check if the point is dominated by any other point
            if any((self.tradespace_df[x_name] <= x) & (self.tradespace_df[y_name] > y)):
                row['pareto'] = False
            else:
                row['pareto'] = True

            # update the row
            self.tradespace_df.loc[index, 'pareto'] = row['pareto']
        return

    def plot_tradespace(self, x_name='price', y_name='mau', block=True, labels=False, hexbin=True):
        # Plot the Maximum Payload vs MAU
        fig, ax = plt.subplots()
        ax.scatter(
            self.tradespace_df[x_name],
            self.tradespace_df[y_name],
            s=50,
            c="b",
            marker="s",
            label=y_name,
        )
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)

        # # Add labels for each point
        if labels:
            for i, row in self.tradespace_df.iterrows():
                ax.annotate(
                    f"ID: {i}",
                    (row[x_name], row[y_name]),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                )

        # Show the legend and plot the figure
        ax.legend()

        if hexbin:
            ax.hexbin(
                self.tradespace_df[x_name],
                self.tradespace_df[y_name],
                gridsize=20,
                cmap="Blues",
            )

        plt.show(block=block)

    def add_price_region(self, fig, desired_price_range):
        if len(desired_price_range) != 2:
            raise Exception(
                "Warning: desired_price_range must have 2 values"
            )

        # check if the desired price is None
        if desired_price_range[0] is None:
            # set minimum price of all items to the minimum price
            desired_price_range[0] = self.tradespace_df['price'].min()

        if desired_price_range[1] is None:
            # set maximum price of all items to the maximum price
            desired_price_range[1] = self.tradespace_df['price'].max()

        if desired_price_range[0] > desired_price_range[1]:
            raise Exception(
                "Warning: desired_price_range must have the first value less than the second value"
            )

        fig.add_vrect(
            x0=desired_price_range[0],
            x1=desired_price_range[1],
            fillcolor="blue",
            opacity=0.10,
            line_width=0,
            annotation_text=f"Desired Price Range",
            annotation_position="top left",
            annotation_font_size=14,
        )
        return fig

    def plot_tradespace_plotly(
        self,
        x_name,
        y_name,
        color_by_attribute=False,
        attribute_name="",
        block=True,
        cbar_y=0.05,
        cbar_len= 0.9,
        pareto=True,
        desired_price_range=[],
        showlegend=True,
    ):
        trace_list = []
        # check if the color value is string
        if color_by_attribute:
            if type(self.tradespace_df[attribute_name][0]) is str:
                # assign a color value to each unique attribute
                color_value = [
                    i for i in range(len(self.tradespace_df[attribute_name].unique()))
                ]
            else:
                color_value = self.tradespace_df[attribute_name]

        if color_by_attribute:
            designs_scatter = go.Scatter(
                x=self.tradespace_df[x_name],
                y=self.tradespace_df[y_name],
                mode="markers",
                marker=dict(
                    size=10,
                    color=color_value,
                    colorscale='Plotly3',
                    showscale=True,
                    colorbar=dict(len=cbar_len, y=cbar_y),
                ),
                text=[f"ID: {i}" for i in range(len(self.tradespace_df))],
                hovertemplate="<b>%{text}</b><br>%{yaxis.title.text}: %{y}<br>%{xaxis.title.text}: %{x}<extra></extra>",
                name=attribute_name,
            )
            trace_list.append(designs_scatter)

        else:
            # Create the scatter plot
            designs_scatter = go.Scatter(
                x=self.tradespace_df[x_name],
                y=self.tradespace_df[y_name],
                mode="markers",
                marker=dict(
                    size=10,
                    color="gray",
                ),
                text=[f"ID: {i}" for i in range(len(self.tradespace_df))],
                hovertemplate="<b>%{text}</b><br>%{yaxis.title.text}: %{y}<br>%{xaxis.title.text}: %{x}<extra></extra>",
                name='All Designs',
            )
            trace_list.append(designs_scatter)

        if pareto:
            # add pareto points to the figure
            pareto_ids = self.tradespace_df['pareto'] == True
            x = self.tradespace_df[pareto_ids][x_name]
            y = self.tradespace_df[pareto_ids][y_name]
            
            # try to get min and max values
            try:
                y_min = self.tradespace_df[pareto_ids]['min_' + y_name].values
                y_max = self.tradespace_df[pareto_ids]['max_' + y_name].values
            except KeyError:
                y_min = np.zeros(len(x))
                y_max = np.zeros(len(x))
                print(f"Warning: min and max values not found for {y_name}")

            ids = self.tradespace_df[pareto_ids].index
            pareto_front_scatter = go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker=dict(
                    size=14,
                    color="darkblue",
                ),
                error_y=dict(
                    type='data', # value of error bar given in data coordinates
                    symmetric=False,
                    array=y_max-y,
                    arrayminus=y-y_min,
                    visible=True),
                text=[f"ID: {i}" for i in ids],
                hovertemplate="<b>%{text}</b><br><br>%{xaxis.title.text}: %{x}<br>%{yaxis.title.text}: %{y}<extra></extra>",
                name='Pareto Front',
            )
            trace_list.append(pareto_front_scatter)

            near_but_not_pareto_ids = (self.tradespace_df['near_pareto'] == True) & (self.tradespace_df['pareto'] == False)

            # add near pareto points to the plot
            x = self.tradespace_df[near_but_not_pareto_ids][x_name]
            y = self.tradespace_df[near_but_not_pareto_ids][y_name]
            ids = self.tradespace_df[near_but_not_pareto_ids].index

            # try to get min and max values
            try:
                y_min = self.tradespace_df[near_but_not_pareto_ids]['min_' + y_name].values
                y_max = self.tradespace_df[near_but_not_pareto_ids]['max_' + y_name].values
            except KeyError:
                y_min = np.zeros(len(x))
                y_max = np.zeros(len(x))
                print(f"Warning: min and max values not found for {y_name}")

            near_pareto_front_scatter = go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker=dict(
                    size=14,
                    color="blue",
                    # opacity=0.50,
                ),
                error_y=dict(
                    type='data', # value of error bar given in data coordinates
                    symmetric=False,
                    array=y_max-y,
                    arrayminus=y-y_min,
                    visible=True),
                text=[f"ID: {i}" for i in ids],
                hovertemplate="<b>%{text}</b><br><br>%{xaxis.title.text}: %{x}<br>%{yaxis.title.text}: %{y}<extra></extra>",
                name='Near Pareto Front',
            )
            trace_list.append(near_pareto_front_scatter)

        pareto_fig = go.Figure(data=trace_list)

        if desired_price_range:
            pareto_fig = self.add_price_region(pareto_fig, desired_price_range)

        # Update the layout
        pareto_fig.update_layout(
            xaxis=dict(title=x_name), yaxis=dict(title=y_name), showlegend=showlegend
        )

        # Show the figure
        if block:
            pareto_fig.show()

        return designs_scatter, pareto_front_scatter, near_pareto_front_scatter

    def plot_price_vs_mau(self, desired_price_range=[], block=True):

        # generate scatter plot
        designs_scatter, pareto_front_scatter, near_pareto_front_scatter = self.plot_tradespace_plotly('price', 'mau', block=False)

        # create a figure with the scatter plot
        fig = go.Figure(data=[designs_scatter, near_pareto_front_scatter, pareto_front_scatter])

        # change y axis limits to 0 to 1
        fig.update_yaxes(range=[-0.05, 1])

        if desired_price_range:
            fig = self.add_price_region(fig, desired_price_range)

        # update the layout
        fig.update_layout(
            xaxis=dict(title='Price (USD)'), yaxis=dict(title='MAU'), showlegend=True
        )

        # show the figure
        if block:
            fig.show()

        return fig

    # def plot_price_vs_performances(self, desired_price_range=desire_price_range):
    #     pass

    def csv_plotly(self, block=True):

        # Get the tradespace dataframe
        df = self.tradespace_df

        # Create a Plotly Table figure
        csv_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(df.columns),
                        fill_color="paleturquoise",
                        align="left",
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )

        # Set the layout of the subplots
        csv_fig.update_layout(title="Drone Designer")
        if block:
            csv_fig.show()

        return csv_fig