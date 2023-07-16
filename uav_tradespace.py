#!/usr/bin/env python3

import numpy as np
from math import pi, sqrt, atan2
from scipy.optimize import fsolve

# local imports
from tradespace import TradespaceDesigner

# Define your performance variables
designer = TradespaceDesigner()

# Add performance variables
# Add maximum flight distance
designer.add_performance_variable("max_flight_distance", 1, 100, "km", 0.33)

# Add maximum speed
designer.add_performance_variable("max_speed", 10, 250, "m/s", 0.33)

# Add maximum payload
designer.add_performance_variable("max_payload", 0.4, 5, "kg", 0.33)

# # Instantiate the design variables by components

# # Add lipo battery with its attributes
# # Add Tattu 10000mAh 3.7V 1C 2S1P Lipo Battery Pack with XT60 plug
# designer.add_component({'component_name': 'tatoo_10000',
#                         'component_type': 'battery',
#                         'component_attributes': {'capacity': {'value': 10000, 'units': 'mAh'},
#                                                  'voltage': {'value': 7.4, 'units': 'V'},
#                                                  'mass': {'value': 0.2, 'units': 'kg'}}})

# # Add Tattu 5200mAh 3.7V 1C 2S1P Lipo Battery Pack with XT60 plug
# designer.add_component({'component_name': 'tatoo_5200',
#                         'component_type': 'battery',
#                         'component_attributes': {'capacity': {'value': 5200, 'units': 'mAh'},
#                                                  'voltage': {'value': 7.4, 'units': 'V'},
#                                                  'mass': {'value': 0.2, 'units': 'kg'}}})

# # Add motor with its attributes
# # Add T-Motor AT2310 2200KV Brushless Motor
# designer.add_component({'component_name': 'motor_tmotor',
#                         'component_type': 'motor',
#                         'component_attributes': {'kv': {'value': 2200, 'units': 'rpm/V'},
#                                                  'mass': {'value': 0.05, 'units': 'kg'}}})

# # Add 820KV Brushless Motor
# designer.add_component({'component_name': 'motor_820',
#                         'component_type': 'motor',
#                         'component_attributes': {'kv': {'value': 820, 'units': 'rpm/V'},
#                                                  'mass': {'value': 0.05, 'units': 'kg'}}})

# # Add propeller with its attributes
# # Add 10x4.5 propeller
# designer.add_component({'component_name': 'propeller_10x45',
#                         'component_type': 'propeller',
#                         'component_attributes': {'diameter': {'value': 10, 'units': 'in'},
#                                                  'pitch': {'value': 4.5, 'units': 'in'},
#                                                  'mass': {'value': 0.01, 'units': 'kg'}}})

# # Add 8x4.5 propeller
# designer.add_component({'component_name': 'propeller_8x45',
#                         'component_type': 'propeller',
#                         'component_attributes': {'diameter': {'value': 8, 'units': 'in'},
#                                                  'pitch': {'value': 4.5, 'units': 'in'},
#                                                  'mass': {'value': 0.01, 'units': 'kg'}}})

# # Add ESC with its attributes
# # Add 30A ESC
# designer.add_component({'component_name': 'esc_30',
#                         'component_type': 'esc',
#                         'component_attributes': {'max_current': {'value': 30, 'units': 'A'},
#                                                  'mass': {'value': 0.01, 'units': 'kg'}}})

# # Add 20A ESC
# designer.add_component({'component_name': 'esc_20',
#                         'component_type': 'esc',
#                         'component_attributes': {'max_current': {'value': 20, 'units': 'A'},
#                                                  'mass': {'value': 0.01, 'units': 'kg'}}})

# # Add frame with its attributes
# # Add 450mm frame
# designer.add_component({'component_name': 'frame_450',
#                         'component_type': 'frame',
#                         'component_attributes': {'diagonal': {'value': 450, 'units': 'mm'},
#                                                  'mass': {'value': 0.2, 'units': 'kg'}}})

# # Add 250mm frame
# designer.add_component({'component_name': 'frame_250',
#                         'component_type': 'frame',
#                         'component_attributes': {'diagonal': {'value': 250, 'units': 'mm'},
#                                                  'mass': {'value': 0.2, 'units': 'kg'}}})

# # Add constant components
# # Add other components mass
# designer.add_component({'component_name': 'other_components',
#                         'component_type': 'constant',
#                         'component_attributes': {'mass': {'value': 0.5, 'units': 'kg'}}})

# Define the relationship between the design variables and the performance variables

# environment
temp = 25  # C
h = 10  # m

# propeller
Dp = 10 * 0.0254  # m
Hp = 4.5 * 0.0254  # m
Bp = 2  # units

# motor
Kv0 = 890  # rpm/V
Um0 = 10  # V
Im0 = 0.5  # A
Rm = 0.101  # Ohm
nr = 4  # units

# esc
Re = 0.008

# battery
Ub = 12
Cb = 5000
Cmin = 0.2 * Cb
Rb = 0.01

# weight
G = 14.7

# # Validating model
# print("Validating model")
# sigma = duty_cycle(Re, 10, Im0 + 5, Ub)
# print("sigma: ", sigma)

# M = motor_torque(Dp, Hp, Bp, 10000)
# print("M: ", M)

# Um = motor_voltage(Kv0, Um0, Im0, Rm, M, 890)
# print("Um: ", Um)

# Im = motor_current(Kv0, Um0, Im0, Rm, M, 890)
# print("Im: ", Im)
# print("")

# Calculate max payload
# calculate_max_payload(Dp, Hp, Bp, Kv0, Um0, Im0, Rm, Re, Ub)

# Calculate on hover mode
calculate_hover_mode(temp, h, G, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, nr, Re, Ub, Cb, Cmin, Rb)

# Calculate on maximum thrust
# calculate_max_thrust_mode(Dp, Hp, Bp, Kv0, Um0, Im0, Rm, nr, Re, Ub, Rb)
