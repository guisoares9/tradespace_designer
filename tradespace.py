import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

class TradespaceDesigner:
    def __init__(self):

        # performance itens dict that will be added by the user
        self.performance_itens = {}

        # design variables dict that will be added by the user
        self.design_variables = {}

        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):

        # add performance variable to the dict
        self.performance_itens[name] = {'min_value': min_value,
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

        return self.tradespace_df

    def add_performance_formula(self, name: str, formula: callable):

        # check if the performance variable is already in the dict
        if name not in self.performance_itens.keys():
            raise Exception('The performance variable {} is not in the tradespace. Please add it first.'.format(name))

        # add performance variable to the dict
        self.performance_itens[name] = {'formula': formula}

        return
    
    # def calculate_performance(self):

    #     # iterate over the performance variables
    #     for name, item in self.performance_itens.items():

    #         # if the item has not a formula
    #         if not ('formula' in item.keys()):
    #             raise Exception('The performance variable {} has no formula'.format(name))
            
    #         # get the formula
    #         formula = item['formula']

    #         # iterate over the tradespace combinations
    #         for index, row in self.tradespace_df.iterrows():

    #             # call the formula with the design variables values
    #             result = formula(**row)

    #             # add the result to the tradespace dataframe
    #             self.tradespace_df.loc[index, name] = result

    def calculate_sau(self):

        for name, item in self.performance_itens.items():

            pass

# Define your performance variables
designer = TradespaceDesigner()

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
designer.add_design_variable("Motor Thrust", "N", [300, 400, 500, 600, 700])

df = designer.generate_tradespace()

# Define the performance formulas
designer.tradespace_df["Maximum Flight Distance"] = 20
designer.tradespace_df["Maximum Payload"] = designer.tradespace_df['Number of Motors'] * designer.tradespace_df['Motor Thrust'] / 9.81 - designer.tradespace_df['Number of Batteries'] * 0.5
designer.tradespace_df["Maximum Speed"] = 50




print(designer.tradespace_df.head())