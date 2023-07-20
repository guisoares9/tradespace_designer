#!/usr/bin/env python3

import numpy as np
from numpy import pi, sqrt, cos, sin, tan, arctan, arccos, arctan2
from scipy.optimize import fsolve

# environment


def air_density(altitude, temp):
    '''
    Calculate the air density
    :param altitude: Altitude
    :param temp: Temperature
    :return: Air density
    '''

    p0 = 1.293  # kg/m^3

    pho = p0 * (1 - 0.0065 * altitude / (temp + 273.15)) ** 5.2561

    return pho

# Propellers


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
    Cd = Cfd + ((pi * A * K0 ** 2) / e) * (epsilon *
                                           arctan2(Hp, np.pi * Dp) - alpha0) ** 2 / (pi * A + K0) ** 2

    # torque coeff
    Cm = 1 / (8 * A) * pi ** 2 * Cd * zeta ** 2 * _lambda * Bp ** 2

    return Cm


def thrust_coefficient(Dp, Hp, Bp):
    '''
    Calculate the thrust coefficient of the propeller
    :param Dp: propeller diameter
    :param Hp: propeller pitch
    :param Bp: propeller blade number
    :return: Thrust coefficient
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

    # thrust coeff
    Ct = 0.25 * pi ** 3 * _lambda * zeta ** 2 * Bp * K0 
    Ct *= (epsilon * arctan2(Hp, pi * Dp) - alpha0) / (pi * A + K0)

    return Ct


def propeller_thrust(Dp, Hp, Bp, N, pho):
    '''
    Calculate the propeller thrust
    :param Dp: propeller diameter
    :param Hp: propeller pitch
    :param Bp: propeller blade number
    :param N: Motor speed (rpm)
    :param pho: air density (kg/m^3) default value is 1.168
    :return: Propeller thrust
    '''

    Ct = thrust_coefficient(Dp, Hp, Bp)

    T = pho * (Dp ** 4) * Ct * ((N / 60) ** 2)
    return T


def propeller_torque(Dp, Hp, Bp, N, pho):
    '''
    Calculate the motor torque
    :param Dp: propeller diameter
    :param Hp: propeller pitch
    :param Bp: propeller blade number
    :param N: Motor speed (rpm)
    :param pho: air density (kg/m^3)
    :return: Motor torque
    '''

    Cm = torque_coefficient(Dp, Hp, Bp)

    M = pho * (Dp ** 5) * Cm * ((N / 60) ** 2)
    return M


def propeller_speed(Dp, Hp, Bp, T, pho):
    '''
    Calculate the propeller speed
    :param Dp: propeller diameter
    :param Hp: propeller pitch
    :param Bp: propeller blade number
    :param T: Propeller thrust
    :param pho: air density (kg/m^3)
    :return: Propeller speed'''

    Ct = thrust_coefficient(Dp, Hp, Bp)

    N = 60 * sqrt(T / (pho * (Dp ** 4) * Ct))
    return N

# Motor


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

    Um = Rm * ((M * Kv0 * Um0) / (9.55 * (Um0 - Im0 * Rm)) + Im0) + \
        ((Um0 - Im0 * Rm) / (Kv0 * Um0)) * N
    return Um


def motor_current(Kv0, Um0, Im0, Rm, M):
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

# ESC


def duty_cycle(Re, Um, Im, Ub, limit=True):
    '''
    Calculate the duty cycle of the motor
    :param Re: Equivalent resistance of the motor
    :param Um: Motor voltage
    :param Im: Motor current
    :param Ub: Battery voltage
    :param limit: Limit duty cycle to 1, for the solver put limit = False
    :return: Duty cycle'''

    sigma = (Um + Im * Re) / Ub

    # necessary for the solver to work with limit = False
    if limit:
        if isinstance(sigma, int) or isinstance(sigma, float):
            if sigma > 1:
                sigma = 1
            if sigma < 0:
                sigma = 0
        else:
            if np.any(sigma > 1):
                print("Some necessary duty cycles are greater than 1. Limiting duty cycles to 1")
                sigma[sigma > 1] = 1
            if np.any(sigma < 0):
                print("Some necessary duty cycles are less than 0. Limiting duty cycles to 0")
                sigma[sigma < 0] = 0

    return sigma


def esc_voltage(Ub, Ib, Rb):
    '''
    Calculate the ESC voltage
    :param nr: Number of rotors
    :param Ub: Battery voltage
    :param Ib: Battery current
    :param Rb: Battery internal resistance
    :return: ESC input voltage
    '''

    Ue = Ub - Ib * Rb
    return Ue


def esc_current(duty_cycle, Im):
    '''
    Calculate the current of the ESC
    :param duty_cycle: Duty cycle
    :param Im: Motor current
    :return: ESC current
    '''

    Ie = duty_cycle * Im
    return Ie

# Battery


def battery_current(num_motors, Ie, Icontrol):
    '''
    Calculate the battery current
    :param num_motors: Number of motors
    :param Ie: ESC current
    :param Icontrol: Control current
    :return: Battery current
    '''

    Ib = num_motors * Ie + Icontrol
    return Ib


def battery_endurance(Ib, Cb, Cmin):
    '''
    Calculate the battery endurance
    :param Ib: Battery current
    :param Cb: Battery capacity
    :param Cmin: Minimum battery capacity
    :return: Battery endurance
    '''

    T = (60 / 1000) * (Cb - Cmin) / Ib
    return T

# System efficiency


def system_efficiency(num_motors, M, N, Ub, Ib):
    '''
    Calculate the system efficiency
    :param num_motors: Number of motors
    :param M: Motor torque
    :param N: Motor speed
    :param Ub: Battery voltage
    :param Ib: Battery current
    :return: System efficiency
    '''

    eta = (2 * pi / 60) * (num_motors * M * N) / (Ub * Ib)
    return eta


def speed_by_pitch(pitch, pho, G, S, C1, C2):

    # speed
    speed = np.sqrt(2 * G * np.tan(pitch) / (pho * S * (C1 *
                    (1 - np.cos(pitch) ** 3) + C2 * (1 - np.sin(pitch) ** 3))))

    return speed


def propeller_speed_by_pitch(pitch, pho, G, Ct, Dp, nr):

    # rpm
    N = 60 * sqrt(G / (pho * (Dp ** 4) * Ct * nr * np.cos(pitch)))

    return N


def propeller_torque_by_pitch(pitch, pho, G, Ct, Cm, Dp, nr):

    # torque
    M = (G * Cm * Dp) / (Ct * nr * np.cos(pitch))

    return M

# Problem solver


def calculate_hover_mode(pho, G, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, nr, Re, Ub, Cb, Cmin, Rb, Icontrol, verbose=False):
    '''
    Calculate the hover mode
    :param pho: Air density
    :param G: UAV mass
    :param Dp: Propeller diameter
    :param Hp: Propeller pitch
    :param Bp: Propeller blade number
    :param Kv0: Motor constant
    :param Um0: Motor voltage
    :param Im0: Motor current
    :param Rm: Motor resistance
    :param nr: Number of rotors
    :param Re: Equivalent resistance of the motor
    :param Ub: Battery voltage
    :param Cb: Battery capacity
    :param Cmin: Minimum battery capacity
    :param Rb: Battery internal resistance
    :param Icontrol: Control current

    :return:
    T (thrust),
    N (propeller speed),
    M (motor torque),
    Um (motor voltage),
    Im (motor current),
    sigma (duty cycle),
    Ue (ESC voltage),
    Ie (ESC current),
    Ib (battery current),
    t_hover (battery endurance
    '''

    if verbose:
        print("")
    if verbose:
        print("Calculating hover mode")

    # calculate necessary propeller thrust
    T = G / nr
    if verbose:
        print("Necessary thrust: ", T, " N")

    # calculate necessary propeller speed
    N = propeller_speed(Dp, Hp, Bp, T, pho)
    if verbose:
        print("Propeller speed: ", round(N, 3), " rpm")

    # calculate propeller torque
    M = propeller_torque(Dp, Hp, Bp, N, pho)
    if verbose:
        print("Propeller torque: ", round(M, 3), " Nm")

    # calculate motor voltage
    Um = motor_voltage(Kv0, Um0, Im0, Rm, M, N)
    if verbose:
        print("Motor voltage: ", round(Um, 3), " V")

    # calculate motor current
    Im = motor_current(Kv0, Um0, Im0, Rm, M)
    if verbose:
        print("Motor current: ", round(Im, 3), " A")

    # calculate duty cycle
    sigma = duty_cycle(Re, Um, Im, Ub)
    if verbose:
        print("Duty cycle: ", round(sigma, 3))

    # calculate esc current
    Ie = esc_current(sigma, Im)
    if verbose:
        print("ESC current: ", round(Ie, 3), " A")

    # calculate esc voltage
    Ue = esc_voltage(Ub, Ie, Rb)
    if verbose:
        print("ESC voltage: ", round(Ue, 3), " V")

    # calculate battery current
    Ib = battery_current(nr, Ie, Icontrol)
    if verbose:
        print("Battery current: ", round(Ib, 3), " A")

    # calculate battery endurance
    t_hover = battery_endurance(Ib, Cb, Cmin)
    if verbose:
        print("Battery endurance: ", round(t_hover, 3), " min")

    # additional calculations
    if verbose:
        print("")
    if verbose:
        print("Additional calculations")

    eta = system_efficiency(nr, M, N, Ub, Ib)
    if verbose:
        print("System efficiency: ", round(eta, 3))

    max_payload = None
    max_pitch = None
    return T, N, M, Um, Im, sigma, Ue, Ie, Ib, t_hover, eta, max_payload, max_pitch


def calculate_max_thrust_mode(pho, G, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, nr, Re, Ub, Cb, Cmin, Rb, Icontrol, verbose=False):

    if verbose:
        print("")
    if verbose:
        print("Calculating maximum thrust mode")

    # on maximum thrust, duty cycle is 1
    max_duty = 1

    def equations(x):

        duty = duty_cycle(Re, x[0], x[1], Ub, limit=False)
        Um = motor_voltage(Kv0, Um0, Im0, Rm, x[2], x[3])
        Im = motor_current(Kv0, Um0, Im0, Rm, x[2])
        M = propeller_torque(Dp, Hp, Bp, x[3], pho)

        return [duty - max_duty,
                x[2] - M,
                x[0] - Um,
                x[1] - Im]

    root, _, ier, mesg = fsolve(
        equations, (Um0, Im0, 1, Kv0 * Um0), full_output=True)

    # address variables
    Um = root[0]
    Im = root[1]
    M = root[2]
    N = root[3]

    if ier != 1:
        raise Exception(f"Solver: fsolve did not find a solution\n{mesg}")
    else:
        if verbose:
            print(
                f"Solver: fsolve found a solution with a error {np.round(equations(root), 5)}")

    if verbose:
        print('The solution on Maximum Thrust is:')
        print('Motor voltage: ', Um, ' V')
        print('Motor current: ', Im, ' A')
        print('Motor torque: ', M, ' Nm')
        print('Motor speed: ', N, ' rpm')

    # calculate esc current
    Ie = esc_current(max_duty, Im)
    if verbose:
        print('ESC current: ', round(Ie, 3), ' A')

    # calculate battery current
    Ib = battery_current(nr, Ie, Icontrol)
    if verbose:
        print('Battery current: ', round(Ib, 3), ' A')

    # calculate esc voltage
    Ue = esc_voltage(Ub, Ib, Rb)
    if verbose:
        print('ESC voltage: ', round(Ue, 3), ' V')

    # calculate efficiency
    eta = system_efficiency(nr, M, N, Ub, Ib)
    if verbose:
        print('System efficiency: ', round(eta, 3))

    # additional calculations
    if verbose:
        print("")
    if verbose:
        print("Additional calculations")

    # calculate propeller thrust
    T = propeller_thrust(Dp, Hp, Bp, N, pho)
    if verbose:
        print('Propeller thrust: ', round(T, 3), ' N')

    # calculate battery endurance
    t_hover = battery_endurance(Ib, Cb, Cmin)
    if verbose:
        print('Battery endurance: ', round(t_hover, 3), ' min')

    max_payload = None
    max_pitch = None
    return T, N, M, Um, Im, max_duty, Ue, Ie, Ib, t_hover, eta, max_payload, max_pitch


def calculate_max_payload_mode(pho, G, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, nr, Re, Ub, Cb, Cmin, Rb, Icontrol, safe_duty_cycle=0.8, verbose=False):

    if verbose:
        print("")
        print("Calculating maximum payload mode")

    # on max payload safe_duty_cycle
    target_duty = safe_duty_cycle

    def equations(x):

        duty = duty_cycle(Re, x[0], x[1], Ub, limit=False)
        Um = motor_voltage(Kv0, Um0, Im0, Rm, x[2], x[3])
        Im = motor_current(Kv0, Um0, Im0, Rm, x[2])
        M = propeller_torque(Dp, Hp, Bp, x[3], pho)

        return [duty - target_duty,
                x[2] - M,
                x[0] - Um,
                x[1] - Im]

    root, _, ier, mesg = fsolve(
        equations, (Um0, Im0, 1, Kv0 * Um0), full_output=True)

    # address variables
    Um = root[0]
    Im = root[1]
    M = root[2]
    N = root[3]

    if ier != 1:
        raise Exception(f"Solver: fsolve did not find a solution\n{mesg}")
    else:
        if verbose:
            print(
                f"Solver: fsolve found a solution with a error {np.round(equations(root), 5)}")

    if verbose:
        print('The solution on Maximum Payload is:')
        print('Motor voltage: ', round(Um, 3), ' V')
        print('Motor current: ', round(Im, 3), ' A')
        print('Motor torque: ', round(M, 3), ' Nm')
        print('Motor speed: ', round(N, 3), ' rpm')

    # calculate thrust
    T = propeller_thrust(Dp, Hp, Bp, N, pho)

    # calculate max payload
    max_payload = ((T * nr) - G) / 9.80665
    if max_payload < 0:
        max_payload = 0

    if verbose:
        print('Maximum payload: ', round(max_payload, 3), ' kg')

    # calculate max pitch
    cos_pitch = G / (T * nr)
    if cos_pitch > 1 or cos_pitch < -1:
        cos_pitch = 1
    max_pitch = arccos(cos_pitch)

    if verbose:
        print('Maximum pitch: ', round(max_pitch, 3), ' rad')

    # additional calculations
    if verbose:
        print("")
    if verbose:
        print("Additional calculations")

    # calculate esc current
    Ie = esc_current(target_duty, Im)
    if verbose:
        print('ESC current: ', round(Ie, 3), ' A')

    # calculate esc voltage
    Ue = esc_voltage(Ub, Ie, Rb)
    if verbose:
        print('ESC voltage: ', round(Ue, 3), ' V')

    # calculate battery current
    Ib = battery_current(nr, Ie, Icontrol)
    if verbose:
        print('Battery current: ', round(Ib, 3), ' A')

    # calculate battery endurance
    t_hover = battery_endurance(Ib, Cb, Cmin)
    if verbose:
        print('Battery endurance: ', round(t_hover, 3), ' min')

    # calculate efficiency
    eta = system_efficiency(nr, M, N, Ub, Ib)
    if verbose:
        print('System efficiency: ', round(eta, 3))

    return T, N, M, Um, Im, target_duty, Ue, Ie, Ib, t_hover, eta, max_payload, max_pitch


def calculate_vel_and_distance(max_pitch, pho, G, S, C1, C2, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, nr, Re, Ub, Cb, Cmin, Rb, Icontrol, verbose=False):

    if verbose:
        print("")
        print("Calculating maximum velocity and distance")

    if max_pitch is None or max_pitch <= 0 or np.isnan(max_pitch):
        max_distance = np.nan
        max_velocity = np.nan
        print("Error: Maximum pitch not valid")
        return max_distance, max_velocity

    pitch = np.linspace(0, max_pitch, 1000)

    # calculate speed
    speed_arr = speed_by_pitch(pitch, pho, G, S, C1, C2)

    # calculate rpm
    Ct = thrust_coefficient(Dp, Hp, Bp)
    rpm_arr = propeller_speed_by_pitch(pitch, pho, G, Ct, Dp, nr)

    # calculate torque
    Cm = torque_coefficient(Dp, Hp, Bp)
    torque_arr = propeller_torque_by_pitch(pitch, pho, G, Ct, Cm, Dp, nr)

    # calculate motor voltage
    Um_arr = motor_voltage(Kv0, Um0, Im0, Rm, torque_arr, rpm_arr)

    # calculate motor current
    Im_arr = motor_current(Kv0, Um0, Im0, Rm, torque_arr)

    # calculate duty cycle
    sigma_arr = duty_cycle(Re, Um_arr, Im_arr, Ub)

    # calculate esc current
    Ie_arr = esc_current(sigma_arr, Im_arr)

    # calculate battery current
    Ib_arr = battery_current(nr, Ie_arr, Icontrol)

    # calculate battery endurance
    t_arr = battery_endurance(Ib_arr, Cb, Cmin)

    # calculate max distance
    max_distance = np.max(60 * speed_arr * t_arr)
    if verbose:
        print("Maximum distance: ", round(max_distance, 3), " m")

    # calculate max velocity
    max_velocity = np.max(speed_arr)
    if verbose:
        print("Maximum velocity: ", round(max_velocity, 3), " m/s")

    return max_distance, max_velocity
