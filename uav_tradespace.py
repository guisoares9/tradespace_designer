from tradespace import TradespaceDesigner

class UAVTradespacer:
    def __init__(self):
        self.td = TradespaceDesigner()
        return

    def add_performance_variable(self, name, min_value, max_value, units, weight):
        # add performance variable to the tradespace designer
        self.td.add_performance_variable(name, min_value, max_value, units, weight)
        return

    def add_frame(self, name, Df, nr, mass, price):
        # add frame to the tradespace designer
        self.td.add_design_component({'name': name,
                                'category': 'frame',
                                'attributes': {'diagonal': {'value': Df, 'units': 'mm'},
                                                'number_of_rotors': {'value': nr, 'units': 'int'},
                                                'mass': {'value': mass, 'units': 'kg'},
                                                'price': {'value': price, 'units': 'USD'}}})
        return

    def add_propeller(self, name, Dp, Hp, Bp, mass, price):
        # add propeller to the tradespace designer
        self.td.add_design_component({'name': name,
                                'category': 'propeller',
                                'attributes': {'diameter': {'value': Dp, 'units': 'in'},
                                                'pitch': {'value': Hp, 'units': 'in'},
                                                'num_blades': {'value': Bp, 'units': 'int'},
                                                'mass': {'value': mass, 'units': 'kg'},
                                                'price': {'value': price, 'units': 'USD'}}})
        return

    def add_motor(self, name, Kv0, Um0, Im0, Rm, mass, price):
        # add motor to the tradespace designer
        self.td.add_design_component({'name': name,
                                'category': 'motor',
                                'attributes': {'kv': {'value': Kv0, 'units': 'rpm/V'},
                                                'no-load voltage': {'value': Um0, 'units': 'V'},
                                                'no-load current': {'value': Im0, 'units': 'A'},
                                                'resistance': {'value': Rm, 'units': 'ohm'},
                                                'mass': {'value': mass, 'units': 'kg'},
                                                'price': {'value': price, 'units': 'USD'}}})
        return

    def add_esc(self, name, Re, mass, price):
        # add ESC to the tradespace designer
        self.td.add_design_component({'name': name,
                                'category': 'esc',
                                'attributes': {'resistance': {'value': Re, 'units': 'ohm'},
                                                'mass': {'value': mass, 'units': 'kg'},
                                                'price': {'value': price, 'units': 'USD'}}})
        return

    def add_battery(self, name, Ub, Cb, Cmin, Rb, mass, price):
        # add battery to the tradespace designer
        self.td.add_design_component({'name': name,
                                'category': 'battery',
                                'attributes': {'voltage': {'value': Ub, 'units': 'V'},
                                                'capacity': {'value': Cb, 'units': 'mAh'},
                                                'min_capacity': {'value': Cmin, 'units': 'mAh'},
                                                'resistance': {'value': Rb, 'units': 'ohm'},
                                                'mass': {'value': mass, 'units': 'kg'},
                                                'price': {'value': price, 'units': 'EUR'}}})
        return

    def add_onboard_computer(self, name, Icontrol, mass, price):
        # add onboard computer to the tradespace designer
        self.td.add_design_component({'name': name,
                                'category': 'onboard_computer',
                                'attributes': {'control_current': {'value': Icontrol, 'units': 'A'},
                                                'mass': {'value': mass, 'units': 'kg'},
                                                'price': {'value': price, 'units': 'USD'}}})
        return
