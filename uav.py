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

def duty_cycle(Re, Um, Im, Ub):
    '''
    Calculate the duty cycle of the motor
    :param Re: Equivalent resistance of the motor
    :param Um: Motor voltage
    :param Im: Motor current
    :param Ub: Battery voltage
    :return: Duty cycle'''

    sigma = (Um + Im * Re) / Ub
    return sigma

def torque_coefficient(Dp, Hp, Bp):
    '''
    Calculate the torque coefficient of the propeller
    :param Dp: propeller diameter
    :param Hp: propeller pitch
    :param Bp: propeller blade number
    :return: Torque coefficient
    '''
    # Constants used in the paper
    A = 5  # 5 ~ 8
    epsilon = 0.85  # 0.85 ~ 0.95
    _lambda = 0.75  # 0.8 ~ 0.9
    zeta = 0.5  # 0.4 ~0.7
    e = 0.83  # 0.7 ~ 0.9
    Cfd = 0.015
    alpha0 = 0  # -pi/36 ~ 0
    K0 = 6.11

    # drag coeff
    Cd = Cfd + ((pi * A * K0 ** 2) / e) * (epsilon * atan2(Hp, pi * Dp) - alpha0) ** 2 / (pi * A + K0) ** 2

    # torque coeff
    Cm = 1 / (8 * A) * pi ** 2 * Cd * zeta ** 2 * _lambda + Bp ** 2

    return Cm

def motor_torque(Dp, Hp, Bp, N, pho=1.168):
    '''
    Calculate the motor torque
    :param Dp: propeller diameter 
    :param Hp: propeller pitch
    :param Bp: propeller blade number
    :param N: Motor speed (rpm)
    :param pho: air density (kg/m^3) default value is 1.168
    :return: Motor torque
    '''

    Cm = torque_coefficient(Dp, Hp, Bp)
    M = pho * (Dp ** 5) * Cm * ((N / 60) ** 2)
    return M

def motor_voltage(Kv0, Um0, Im0, Rm, M, N):
    '''
    Calculate the motor voltage
    :param Kv0: Motor constant
    :param Um0: Motor voltage
    :param Im0: Motor current
    :param Rm: Motor resistance
    :param M: Motor torque
    :param N: Motor speed
    :return: Motor voltage
    '''

    Um = Rm * ((M * Kv0 * Um0) / (9.55 * (Um0 - Im0 * Rm)) + Im0) + ((Um0 - Im0 * Rm) / (Kv0 * Um0)) * N
    return Um

def motor_current(Kv0, Um0, Im0, Rm, M, N):
    '''
    Calculate the motor current
    :param Kv0: Motor constant
    :param Um0: Motor voltage
    :param Im0: Motor current
    :param Rm: Motor resistance
    :param M: Motor torque
    :param N: Motor speed
    :return: Motor current
    '''

    Im = (M * Kv0 * Um0) / (9.55 * (Um0 - Im0 * Rm)) + Im0
    return Im

def calculate_max_payload(Re, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, Ub):

    def equations(x):

        duty = duty_cycle(Re, x[0], x[1], Ub)
        Um = motor_voltage(Kv0, Um0, Im0, Rm, x[2], x[3])
        Im = motor_current(Kv0, Um0, Im0, Rm, x[2], x[3])
        M = motor_torque(Dp, Hp, Bp, x[3])

        # print("duty: ", duty)
        # print("Um: ", x[0])
        # print("Im: ", x[1])
        # print("M: ", x[2])
        # print("N: ", x[3])

        return [duty - 1,
                x[2] - M,
                x[0] - Um,
                x[1] - Im]

    root, _, ier, mesg = fsolve(equations, (Um0, Im0, 1, Kv0 * Um0), full_output=True)

    if ier != 1:
        print("fsolve did not find a solution")
        print(mesg)
    else:
        print("fsolve found a solution")

    print(root)
    print(equations(root))


Re = 0.008
Dp = 10 * 0.0254
Hp = 4.5 * 0.0254
Bp = 2
Kv0 = 820
Um0 = 10
Im0 = 0.5
Rm = 0.101
Ub = 12

calculate_max_payload(Re, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, Ub)

M = motor_torque(Dp, Hp, Bp, 890)