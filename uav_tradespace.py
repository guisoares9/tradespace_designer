import numpy as np
from tradespace import TradespaceDesigner
from uav import UAVModel
# make a subplot for each category
from plotly.subplots import make_subplots
import itertools

class UAVTradespacer:
    def __init__(self):
        # start tradespace designer
        self.td = TradespaceDesigner()

        # init uav list
        self.uav_list = []

        self.desire_price_range = []

        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):
        # add performance variable to the tradespace designer
        self.td.add_performance_variable(name, min_value, max_value, units, weight)
        return

    def set_desired_price_range(self, min_price, max_price):

        # assert that its int float or None
        if not isinstance(min_price, (int, float, type(None))):
            raise TypeError("The minimum price must be an integer or a float.")
        if not isinstance(max_price, (int, float, type(None))):
            raise TypeError("The maximum price must be an integer or a float.")

        # check if the price range is valid
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("The minimum price cannot be higher than the maximum price.")

        self.desire_price_range = [min_price, max_price]
        return

    def add_frame(self, name, Df, nr, mass, price):
        # add frame to the tradespace designer
        self.td.add_design_component(
            {
                "name": name,
                "category": "frame",
                "attributes": {
                    "diagonal": {"value": Df, "units": "mm"},
                    "number_of_rotors": {"value": nr, "units": "int"},
                    "mass": {"value": mass, "units": "kg"},
                    "price": {"value": price, "units": "USD"},
                },
            }
        )
        return

    def add_propeller(self, name, Dp, Hp, Bp, mass, price):
        # add propeller to the tradespace designer
        self.td.add_design_component(
            {
                "name": name,
                "category": "propeller",
                "attributes": {
                    "diameter": {"value": Dp, "units": "in"},
                    "pitch": {"value": Hp, "units": "in"},
                    "num_blades": {"value": Bp, "units": "int"},
                    "mass": {"value": mass, "units": "kg"},
                    "price": {"value": price, "units": "USD"},
                },
            }
        )
        return

    def add_motor(self, name, Kv0, Um0, Im0, Rm, mass, price):
        # add motor to the tradespace designer
        self.td.add_design_component(
            {
                "name": name,
                "category": "motor",
                "attributes": {
                    "kv": {"value": Kv0, "units": "rpm/V"},
                    "no-load voltage": {"value": Um0, "units": "V"},
                    "no-load current": {"value": Im0, "units": "A"},
                    "resistance": {"value": Rm, "units": "ohm"},
                    "mass": {"value": mass, "units": "kg"},
                    "price": {"value": price, "units": "USD"},
                },
            }
        )
        return

    def add_esc(self, name, Re, mass, price):
        # add ESC to the tradespace designer
        self.td.add_design_component(
            {
                "name": name,
                "category": "esc",
                "attributes": {
                    "resistance": {"value": Re, "units": "ohm"},
                    "mass": {"value": mass, "units": "kg"},
                    "price": {"value": price, "units": "USD"},
                },
            }
        )
        return

    def add_battery(self, name, Ub, Cb, Cmin, Rb, mass, price):
        # add battery to the tradespace designer
        self.td.add_design_component(
            {
                "name": name,
                "category": "battery",
                "attributes": {
                    "voltage": {"value": Ub, "units": "V"},
                    "capacity": {"value": Cb, "units": "mAh"},
                    "min_capacity": {"value": Cmin, "units": "mAh"},
                    "resistance": {"value": Rb, "units": "ohm"},
                    "mass": {"value": mass, "units": "kg"},
                    "price": {"value": price, "units": "EUR"},
                },
            }
        )
        return

    def add_onboard_computer(self, name, Icontrol, mass, price):
        # add onboard computer to the tradespace designer
        self.td.add_design_component(
            {
                "name": name,
                "category": "onboard_computer",
                "attributes": {
                    "control_current": {"value": Icontrol, "units": "A"},
                    "mass": {"value": mass, "units": "kg"},
                    "price": {"value": price, "units": "USD"},
                },
            }
        )
        return

    def generate_tradespace(self, sensitive_analysis=True):
        # generate tradespace with the all possible combinations of design components
        self.td.generate_design_tradespace()

        td = self.td

        self.uav_list = []
        # calculate performance
        for index, row in td.tradespace_df.iterrows():
            uav = UAVModel()

            temp = 25
            h = 60
            safe_duty_cycle = 0.7

            Icontrol = td.get_attr_by_name(row["onboard_computer"], "control_current")

            mass = (
                td.get_attr_by_name(row["frame"], "mass")
                + td.get_attr_by_name(row["propeller"], "mass")
                * td.get_attr_by_name(row["frame"], "number_of_rotors")
                + td.get_attr_by_name(row["motor"], "mass")
                * td.get_attr_by_name(row["frame"], "number_of_rotors")
                + td.get_attr_by_name(row["esc"], "mass")
                * td.get_attr_by_name(row["frame"], "number_of_rotors")
                + td.get_attr_by_name(row["battery"], "mass")
                + td.get_attr_by_name(row["onboard_computer"], "mass")
            )

            nr = td.get_attr_by_name(row["frame"], "number_of_rotors")

            Dp = td.get_attr_by_name(row["propeller"], "diameter")
            Hp = td.get_attr_by_name(row["propeller"], "pitch")
            Bp = td.get_attr_by_name(row["propeller"], "num_blades")

            Kv0 = td.get_attr_by_name(row["motor"], "kv")
            Um0 = td.get_attr_by_name(row["motor"], "no-load voltage")
            Im0 = td.get_attr_by_name(row["motor"], "no-load current")
            Rm = td.get_attr_by_name(row["motor"], "resistance")

            Re = td.get_attr_by_name(row["esc"], "resistance")

            Ub = td.get_attr_by_name(row["battery"], "voltage")
            Cb = td.get_attr_by_name(row["battery"], "capacity")
            Cmin = td.get_attr_by_name(row["battery"], "min_capacity")
            Rb = td.get_attr_by_name(row["battery"], "resistance")

            # price
            price = (
                td.get_attr_by_name(row["frame"], "price")
                + td.get_attr_by_name(row["propeller"], "price")
                * td.get_attr_by_name(row["frame"], "number_of_rotors")
                + td.get_attr_by_name(row["motor"], "price")
                * td.get_attr_by_name(row["frame"], "number_of_rotors")
                + td.get_attr_by_name(row["esc"], "price")
                * td.get_attr_by_name(row["frame"], "number_of_rotors")
                + td.get_attr_by_name(row["battery"], "price")
                + td.get_attr_by_name(row["onboard_computer"], "price")
            )

            uav.setAll(
                temp,
                h,
                mass,
                nr,
                Dp,
                Hp,
                Bp,
                Kv0,
                Um0,
                Im0,
                Rm,
                Re,
                Ub,
                Cb,
                Cmin,
                Rb,
                Icontrol,
                safe_duty_cycle,
            )

            # calculate performance
            uav.calculate_performance()

            # add design variables to the tradespace
            td.tradespace_df.loc[index, "mass"] = uav.G / uav.g
            td.tradespace_df.loc[index, "number_of_rotors"] = uav.nr
            td.tradespace_df.loc[index, "prop_diameter"] = uav.Dp
            td.tradespace_df.loc[index, "prop_pitch"] = uav.Hp
            td.tradespace_df.loc[index, "prop_blades"] = uav.Bp
            td.tradespace_df.loc[index, "motor_resistance"] = uav.Rm
            td.tradespace_df.loc[index, "kv"] = uav.Kv0
            td.tradespace_df.loc[index, "esc_resistance"] = uav.Re
            td.tradespace_df.loc[index, "voltage"] = uav.Ub
            td.tradespace_df.loc[index, "capacity"] = uav.Cb
            td.tradespace_df.loc[index, "battery_resistance"] = uav.Rb
            td.tradespace_df.loc[index, "battery_min_capacity"] = uav.Cmin
            td.tradespace_df.loc[index, "onboard_computer_current"] = uav.Icontrol

            # add price to the tradespace
            td.tradespace_df.loc[index, "price"] = price

            # add performance to the tradespace
            td.tradespace_df.loc[index, "max_flight_distance"] = uav.max_distance

            td.tradespace_df.loc[index, "max_speed"] = uav.max_speed

            td.tradespace_df.loc[index, "max_payload"] = uav.max_payload / 9.81

            td.tradespace_df.loc[index, "max_flight_time"] = uav.t_hover

            # append uav to the list
            self.uav_list.append(uav)

        if sensitive_analysis:

            # store the original datafrane
            original_tradespace_df = td.tradespace_df.copy()

            # store the original performance items
            original_performance_items = td.performance_items.copy()

            # iterate 100 times to change the values of design and performance variables to see how the performance changes
            near_pareto_unique_ids_dict = {}
            min_max_maus = {}

            range_percent = 0.5
            weights_list = []
            for value in td.performance_items.values():
                weights_list.append(value["weight"])
            weights_list = np.array(weights_list)

            # generate combinations of coefficients for each performance attribute, guaranteeing that the sum of all coefficients is 1
            coeff_combinations = np.array(list(itertools.product(np.array([1-range_percent, 1.0, 1+range_percent]), repeat=len(td.performance_items))))

            coeff_combinations = np.multiply(coeff_combinations, weights_list)

            # make the sum of each row equal to 1
            coeff_combinations = coeff_combinations / np.sum(coeff_combinations, axis=1)[:, None]

            for i in range(len(coeff_combinations)):
                # print(i)
                # change design variables
                # for index, row in td.tradespace_df.iterrows():
                #     for attribute in td.design_components:
                #         continue
                #         td.tradespace_df.loc[index, attribute] = row[attribute] * coeff

                # change performance items weights
                for perf_idx, name in enumerate(self.td.performance_items.keys()):
                    self.td.performance_items[name]['weight'] = coeff_combinations[i][perf_idx]
                    # print(self.td.performance_items)

                # check if the sum is 1
                sum = np.sum([value['weight'] for value in self.td.performance_items.values()])
                assert np.isclose(sum, 1.0), "The sum of the weights must be 1.0, but it is {}.".format(sum)

                # calculate performance
                self.td.generate_performance_tradespace()

                # store the designs that are in the pareto front with each id
                pareto_ids = self.td.tradespace_df[self.td.tradespace_df["pareto"] == True]
                maus = self.td.tradespace_df["mau"]

                # dict to save the id
                for index, pareto_id in enumerate(pareto_ids.index):
                    if not (pareto_id in near_pareto_unique_ids_dict):
                        near_pareto_unique_ids_dict[pareto_id] = {}

                # add min max mau for all designs
                for index, row in self.td.tradespace_df.iterrows():
                    if not (index in min_max_maus):
                        min_max_maus[index] = {"max": maus.iloc[index], "min": maus.iloc[index]}
                    elif maus.iloc[index] > min_max_maus[index]["max"]:
                        min_max_maus[index]["max"] = maus.iloc[index]
                    elif maus.iloc[index] < min_max_maus[index]["min"]:
                        min_max_maus[index]["min"] = maus.iloc[index]

            # reset the values of design and performance variables
            self.td.tradespace_df = original_tradespace_df.copy()

            # restore the original performance items
            self.td.performance_items = original_performance_items.copy()

            self.td.generate_performance_tradespace()

            # add possible pareto ids to the tradespace
            for index, row in self.td.tradespace_df.iterrows():
                if index in near_pareto_unique_ids_dict:
                    self.td.tradespace_df.loc[index, "near_pareto"] = True
                else:
                    self.td.tradespace_df.loc[index, "near_pareto"] = False

            # add the max and min MAU to the tradespace
            for index, row in self.td.tradespace_df.iterrows():
                if index in min_max_maus:
                    self.td.tradespace_df.loc[index, "max_mau"] = min_max_maus[index]["max"]
                    self.td.tradespace_df.loc[index, "min_mau"] = min_max_maus[index]["min"]
                else:
                    self.td.tradespace_df.loc[index, "max_mau"] = None
                    self.td.tradespace_df.loc[index, "min_mau"] = None

        else:
            self.td.generate_performance_tradespace()

        # save the tradespace to a csv file
        self.td.save_tradespace('tradespace.csv')

        return

    def plot_all_attributes(self, x_name, y_name):
        # categories
        # categories = list(dict.fromkeys([self.td.design_components[option]['category'] for option in self.td.design_components]))
        categories = [
            "mass",
            "number_of_rotors",
            "prop_diameter",
            "prop_pitch",
            "kv",
            "voltage",
            "capacity",
            "max_flight_distance",
            "max_speed",
            "max_payload",
            "max_flight_time",
        ]

        categories_to_title = {
            "mass": "Mass [kg]",
            "number_of_rotors": "Number of rotors",
            "prop_diameter": "Propeller diameter [in]",
            "prop_pitch": "Propeller pitch [in]",
            "kv": "Motor kv [rpm/V]",
            "voltage": "Battery voltage [V]",
            "capacity": "Battery capacity [mAh]",
            "max_flight_distance": "Max flight distance [m]",
            "max_speed": "Max speed [m/s]",
            "max_payload": "Max payload [kg]",
            "max_flight_time": "Max flight time [m]",
        }

        if x_name is None:
            x_is_category = True
        else:
            x_is_category = False

        fig = make_subplots(len(categories), 1, subplot_titles=list(categories_to_title.values()))

        pixels_per_plot = 350
        total_pixels = pixels_per_plot * len(categories)

        # get figures
        color_len = 200 / total_pixels
        color_y = (pixels_per_plot * len(categories)) / total_pixels - color_len / 2
        for index, category in enumerate(categories):

            if x_is_category:
                x_name = category

            designs_trace, pareto_trace, near_pareto_trace = self.td.plot_tradespace_plotly(
                x_name, y_name, color_by_attribute=True, attribute_name=category, block=False, cbar_y=color_y, cbar_len=color_len, showlegend=False
            )
            fig.add_trace(pareto_trace, row=index+1, col=1)
            fig.add_trace(near_pareto_trace, row=index+1, col=1)
            fig.add_trace(designs_trace, row=index+1, col=1)
            color_y -= 1.041 * pixels_per_plot / total_pixels

            # add yaxis name
            fig.update_yaxes(title_text=y_name, row=index+1, col=1)
            fig.update_xaxes(title_text=x_name, row=index+1, col=1)

        # add price range
        fig = self.td.add_price_region(fig, self.desire_price_range)

        fig.update_layout(height=pixels_per_plot*len(categories), width=1080, title_text="MAU per attribute", showlegend=False)
        fig.show()

    def plot_price_vs_mau(self):
        self.td.plot_price_vs_mau(desired_price_range=self.desire_price_range)
        return

    def plot_price_vs_performances(self):
        categories = list(self.td.performance_items.keys())

        # remove _, capitalize and add unit
        categories_to_title = [
            category.replace("_", " ").capitalize() + " [" + self.td.performance_items[category]["units"] + "]" for category in categories
        ]

        fig = make_subplots(len(categories), 1, subplot_titles=categories_to_title)

        for index, category in enumerate(categories):
            designs_trace, pareto_trace, near_pareto_trace = self.td.plot_tradespace_plotly(
                "price", category, block=False, showlegend=False
            )
            fig.add_trace(designs_trace, row=index+1, col=1)
            fig.add_trace(near_pareto_trace, row=index+1, col=1)
            fig.add_trace(pareto_trace, row=index+1, col=1)

            # add horizontal line to show the desired min and max performance
            fig.add_hline(
                y=self.td.performance_items[category]["min_value"],
                line_dash="dash",
                row=index+1,
                col=1,
                annotation_text="min",
                annotation_position="bottom right",
            )
            fig.add_hline(
                y=self.td.performance_items[category]["max_value"],
                line_dash="dash",
                row=index+1,
                col=1,
                annotation_text="max",
                annotation_position="top right",
            )

            title = categories_to_title[index]
            fig.update_yaxes(title_text=title, row=index+1, col=1)
            fig.update_xaxes(title_text="price", row=index+1, col=1)

        # add price range
        fig = self.td.add_price_region(fig, self.desire_price_range)

        pixels_per_plot = 400
        fig.update_layout(height=pixels_per_plot*len(categories), width=1080, title_text="Performance per Price", showlegend=False)
        fig.show()
        return

    def save_components_to_json(self, filename):
        self.td.save_components_to_json(filename)
        return
