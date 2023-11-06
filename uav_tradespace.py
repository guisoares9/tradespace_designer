from tradespace import TradespaceDesigner
from uav import UAVModel


class UAVTradespacer:
    def __init__(self):
        # start tradespace designer
        self.td = TradespaceDesigner()

        # init uav list
        self.uav_list = []

        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):
        # add performance variable to the tradespace designer
        self.td.add_performance_variable(name, min_value, max_value, units, weight)
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

    def generate_tradespace(self):
        # generate tradespace with the all possible combinations of design components
        self.td.generate_tradespace()

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
            td.tradespace_df.loc[index, "kv"] = uav.Kv0
            td.tradespace_df.loc[index, "voltage"] = uav.Ub
            td.tradespace_df.loc[index, "capacity"] = uav.Cb

            # add price to the tradespace
            td.tradespace_df.loc[index, "price"] = price

            # add performance to the tradespace
            td.tradespace_df.loc[index, "max_flight_distance"] = uav.max_distance

            td.tradespace_df.loc[index, "max_speed"] = uav.max_speed

            td.tradespace_df.loc[index, "max_payload"] = uav.max_payload / 9.81

            td.tradespace_df.loc[index, "max_flight_time"] = uav.t_hover

            # append uav to the list
            self.uav_list.append(uav)

        return

    def plot_all_attributes(self, x_name, y_name):
        # categories
        # categories = list(dict.fromkeys([self.td.design_components[option]['category'] for option in self.td.design_components]))
        categories = [
            "mass",
            # "number_of_rotors",/
            "kv",
            "voltage",
            "capacity",
            "price",
            "max_flight_distance",
            "max_speed",
            "max_payload",
            "max_flight_time",
        ]

        # make a subplot for each category
        from plotly.subplots import make_subplots

        fig = make_subplots(len(categories), 1, subplot_titles=categories)

        # get figures
        for category in categories:
            trace = self.td.plot_tradespace_plotly(
                x_name, y_name, color_by_attribute=True, attribute_name=category, block=False
            )
            fig.add_trace(trace, row=categories.index(category) + 1, col=1)

        fig.update_layout(height=3000, width=1080, title_text="Stacked Subplots")
        fig.show()

    def save_components_to_json(self, filename):
        self.td.save_components_to_json(filename)
        return
