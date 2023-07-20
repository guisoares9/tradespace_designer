#!/usr/bin/env python3
import json

# local imports
from tradespace import TradespaceDesigner
from uav import UAVModel

# Define your performance variables
designer = TradespaceDesigner()

# Add performance variables
# Add maximum flight distance
designer.add_performance_variable("max_flight_distance", 1, 20000, "m", 0.33)

# Add maximum speed
designer.add_performance_variable("max_speed", 5, 50, "m/s", 0.33)

# Add maximum payload
designer.add_performance_variable("max_payload", 0.1, 5, "kg", 0.33)

# # Instantiate the design variables by components


def add_frame(name, Df, nr, mass, price):

    # add frame to the tradespace designer
    designer.add_design_component({'name': name,
                                   'category': 'frame',
                                   'attributes': {'diagonal': {'value': Df, 'units': 'mm'},
                                                  'number_of_rotors': {'value': nr, 'units': 'int'},
                                                  'mass': {'value': mass, 'units': 'kg'},
                                                  'price': {'value': price, 'units': 'USD'}}})

    return


def add_propeller(name, Dp, Hp, Bp, mass, price):

    # add propeller to the tradespace designer
    designer.add_design_component({'name': name,
                                   'category': 'propeller',
                                   'attributes': {'diameter': {'value': Dp, 'units': 'in'},
                                                  'pitch': {'value': Hp, 'units': 'in'},
                                                  'num_blades': {'value': Bp, 'units': 'int'},
                                                  'mass': {'value': mass, 'units': 'kg'},
                                                  'price': {'value': price, 'units': 'USD'}}})
    return


def add_motor(name, Kv0, Um0, Im0, Rm, mass, price):

    # add motor to the tradespace designer
    designer.add_design_component({'name': name,
                                   'category': 'motor',
                                   'attributes': {'kv': {'value': Kv0, 'units': 'rpm/V'},
                                                  'no-load voltage': {'value': Um0, 'units': 'V'},
                                                  'no-load current': {'value': Im0, 'units': 'A'},
                                                  'resistance': {'value': Rm, 'units': 'ohm'},
                                                  'mass': {'value': mass, 'units': 'kg'},
                                                  'price': {'value': price, 'units': 'USD'}}})
    return


def add_esc(name, Re, mass, price):

    # add ESC to the tradespace designer
    designer.add_design_component({'name': name,
                                   'category': 'esc',
                                   'attributes': {'resistance': {'value': Re, 'units': 'ohm'},
                                                  'mass': {'value': mass, 'units': 'kg'},
                                                  'price': {'value': price, 'units': 'USD'}}})
    return


def add_battery(name, Ub, Cb, Cmin, Rb, mass, price):

    # add battery to the tradespace designer
    designer.add_design_component({'name': name,
                                   'category': 'battery',
                                   'attributes': {'voltage': {'value': Ub, 'units': 'V'},
                                                  'capacity': {'value': Cb, 'units': 'mAh'},
                                                  'min_capacity': {'value': Cmin, 'units': 'mAh'},
                                                  'resistance': {'value': Rb, 'units': 'ohm'},
                                                  'mass': {'value': mass, 'units': 'kg'},
                                                  'price': {'value': price, 'units': 'EUR'}}})
    return


# Add lipo battery with its attributes
# Add Zeee 2S LiPo Battery 7.4V 60C 1500mAh (Pack with 2 in parallel)
# https://amzn.eu/d/0v9NqXT
add_battery(name='zeee_1500_2_pack', Ub=7.4, Cb=3000, Cmin=600, Rb=0.2, mass=0.176, price=32.99)
# Add Tattu 2300mAh 11.1V 45C 3S1P
# https://amzn.eu/d/3qAMa69
add_battery(name='tatoo_2300', Ub=11.1, Cb=2300, Cmin=460, Rb=0.2, mass=0.1822, price=26.19)
# Add HRB 2 Pack 3S 11,1 V 5000 mAh LiPo-accu 50 C
# https://amzn.eu/d/bihiQ4N
add_battery(name='hrb_5000', Ub=11.1, Cb=5000, Cmin=1000, Rb=0.2, mass=0.376, price=45.99)
# Add Zeee 3S Lipo Battery 11.1V 100C 8000mAh
# https://amzn.eu/d/8p7C5QJ
add_battery(name='zeee_8000', Ub=11.1, Cb=8000, Cmin=1600, Rb=0.2, mass=0.493, price=79.99)
# Add Tattu Lipo 6S RC Battery 22.2V 1300mAh 120C
# https://amzn.eu/d/fp4bDz7
add_battery(name='tatoo_1300', Ub=22.2, Cb=1300, Cmin=260, Rb=0.2, mass=0.212, price=41.62)

# Add motor with its attributes
# Add TMOTOR Velox Victory V3008 1350kv
# https://shop.tmotor.com/products/cinematic-fpv-drone-motor-v3008
add_motor(name='motor_v3008', Kv0=1350, Um0=10, Im0=1.18, Rm=0.1, mass=0.07, price=28.39)
# Add TMOTOR VELOCE V2808 1950KV
# https://shop.tmotor.com/products/fpv-brushless-motor-v2808?variant=41118111367377
add_motor(name='motor_v2808', Kv0=1950, Um0=10, Im0=2.45, Rm=0.1, mass=0.061, price=24.83)

# Add propeller with its attributes
# Add 10x4.5 propeller
add_propeller(name='propeller_10x45', Dp=10, Hp=4.5, Bp=2, mass=0.01, price=5)
# # Add 8x4.5 propeller
add_propeller(name='propeller_8x45', Dp=8, Hp=4.5, Bp=2, mass=0.01, price=5)

# Add ESC with its attributes
# Add 30A ESC
add_esc(name='esc_30', Re=0.01, mass=0.01, price=10)
# # Add 20A ESC
# add_esc('esc_20', 0.01, 0.01, 10)

# # Add frame with its attributes
# # Add 450mm frame
add_frame(name='frame_450', Df=450, nr=4, mass=0.4, price=20)
# # Add 250mm frame
add_frame(name='frame_250', Df=250, nr=4, mass=0.2, price=15)

# dict to json
with open('design_components.json', 'w') as fp:
    json.dump(designer.design_components, fp, indent=4)
designer.generate_tradespace()

# see the tradespace
print(designer.tradespace_df.head())

uav_list = []
# calculate performance
for index, row in designer.tradespace_df.iterrows():
    uav = UAVModel()

    temp = 25
    h = 10
    Icontrol = 1
    safe_duty_cycle = 0.7

    mass = designer.design_components[row['frame']]['attributes']['mass']['value'] + \
        designer.design_components[row['propeller']]['attributes']['mass']['value'] + \
        designer.design_components[row['motor']]['attributes']['mass']['value'] + \
        designer.design_components[row['esc']]['attributes']['mass']['value'] + \
        designer.design_components[row['battery']
                                   ]['attributes']['mass']['value']

    nr = designer.design_components[row['frame']
                                    ]['attributes']['number_of_rotors']['value']

    Dp = designer.design_components[row['propeller']
                                    ]['attributes']['diameter']['value']
    Hp = designer.design_components[row['propeller']
                                    ]['attributes']['pitch']['value']
    Bp = designer.design_components[row['propeller']
                                    ]['attributes']['num_blades']['value']

    Kv0 = designer.design_components[row['motor']]['attributes']['kv']['value']
    Um0 = designer.design_components[row['motor']
                                     ]['attributes']['no-load voltage']['value']
    Im0 = designer.design_components[row['motor']
                                     ]['attributes']['no-load current']['value']
    Rm = designer.design_components[row['motor']
                                    ]['attributes']['resistance']['value']

    Re = designer.design_components[row['esc']
                                    ]['attributes']['resistance']['value']

    Ub = designer.design_components[row['battery']
                                    ]['attributes']['voltage']['value']
    Cb = designer.design_components[row['battery']
                                    ]['attributes']['capacity']['value']
    Cmin = designer.design_components[row['battery']
                                      ]['attributes']['min_capacity']['value']
    Rb = designer.design_components[row['battery']
                                    ]['attributes']['resistance']['value']

    # price
    price = designer.design_components[row['frame']]['attributes']['price']['value'] + \
        designer.design_components[row['propeller']]['attributes']['price']['value'] + \
        designer.design_components[row['motor']]['attributes']['price']['value'] + \
        designer.design_components[row['esc']]['attributes']['price']['value'] + \
        designer.design_components[row['battery']
                                   ]['attributes']['price']['value']

    uav.setAll(temp, h, mass, nr, Dp, Hp, Bp, Kv0, Um0, Im0, Rm,
               Re, Ub, Cb, Cmin, Rb, Icontrol, safe_duty_cycle)

    # calculate performance
    uav.calculate_performance()

    # add design variables to the tradespace
    designer.tradespace_df.loc[index, 'mass'] = uav.G / uav.g
    designer.tradespace_df.loc[index, 'number_of_rotors'] = uav.nr
    designer.tradespace_df.loc[index, 'kv'] = uav.Kv0
    designer.tradespace_df.loc[index, 'voltage'] = uav.Ub
    designer.tradespace_df.loc[index, 'capacity'] = uav.Cb

    # add price to the tradespace
    designer.tradespace_df.loc[index, 'price'] = price

    # add performance to the tradespace
    designer.tradespace_df.loc[index, 'max_flight_distance'] = uav.max_distance

    designer.tradespace_df.loc[index, 'max_speed'] = uav.max_speed

    designer.tradespace_df.loc[index, 'max_payload'] = uav.max_payload

    designer.tradespace_df.loc[index, 'max_flight_time'] = uav.t_hover

    # append uav to the list
    uav_list.append(uav)

# calculate the sau
designer.calculate_sau()

# calculate the mau
designer.calculate_mau()

# see the tradespace
designer.plot_tradespace_plotly('price', 'MAU')

# save the tradespace to a csv file
designer.tradespace_df.to_csv('tradespace.csv', index=True)

# uav_list[12].show_config()
# uav_list[12].show_performance()

# uav_list[12].calculate_performance()