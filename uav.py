#!/usr/bin/env python3

import numpy as np

import uav_model as model


class UAVModel:

    g = 9.80665  # gravitational acceleration (m/s^2)

    def __init__(self) -> None:

        # environment
        self.temp = None  # temperature (°C)
        self.h = None  # altitude (m)
        self.pho = None  # air density (kg/m^3)

        # general
        self.G = None  # weight of the uav (N)

        # aerodynamics and geometry of the uav
        self.S = 0.5 * 0.45 ** 2  # surface area of the uav (m^2)
        self.C1 = 3  # C1 coefficient of the uav (unit)
        self.C2 = 1.5  # C2 coefficient of the uav (unit)

        # propeller
        self.Dp = None  # propeller diameter (m)
        self.Hp = None  # propeller pitch (m)
        self.Bp = None

        self.Ct = None
        self.Cm = None

        # motor
        self.Kv0 = None
        self.Um0 = None
        self.Im0 = None
        self.Rm = None
        self.nr = None

        # esc
        self.Re = None

        # battery
        self.Ub = None
        self.Cb = None
        self.Cmin = None
        self.Rb = None

        # control
        self.Icontrol = None

        # safety factor
        self.safe_duty_cycle = None

        # calculated parameters
        self.T_hover = None
        self.N_hover = None
        self.M_hover = None
        self.Um_hover = None
        self.Im_hover = None
        self.sigma_hover = None
        self.Ue_hover = None
        self.Ie_hover = None
        self.Ib_hover = None
        self.t_hover = None
        self.eta = None

        self.T_max = None
        self.N_max = None
        self.M_max = None
        self.Um_max = None
        self.Im_max = None
        self.sigma_max = None
        self.Ue_max = None
        self.Ie_max = None
        self.Ib_max = None
        self.t_max = None
        self.eta = None

        self.T_payload = None
        self.N_payload = None
        self.M_payload = None
        self.Um_payload = None
        self.Im_payload = None
        self.sigma_payload = None
        self.Ue_payload = None
        self.Ie_payload = None
        self.Ib_payload = None
        self.t_payload = None
        self.eta = None
        self.max_payload = None
        self.max_pitch = None

        self.max_speed = None
        self.max_distance = None

        return None

    def setAll(self, temp, h, mass, nr, Dp, Hp, Bp, Kv0, Um0, Im0, Rm, Re, Ub, Cb, Cmin, Rb, Icontrol, safe_duty_cycle):
        '''
        Set all the parameters
        :param temp: Temperature (°C)
        :param h: Altitude (m)
        :param mass: Mass of the UAV (Kg)
        :param Dp: propeller diameter (in)
        :param Hp: propeller pitch (in)
        :param Bp: propeller blade number (unit)
        :param Kv0: Motor constant (rpm/V)
        :param Um0: Motor no-load voltage (V)
        :param Im0: Motor no-load current (A)
        :param Rm: Motor resistance (Ohm)
        :param nr: Number of rotors (unit)
        :param Re: Equivalent resistance of the esc (Ohm)
        :param Ub: Battery voltage (V)
        :param Cb: Battery capacity (mAh)
        :param Cmin: Minimum battery capacity (mAh)
        :param Rb: Battery internal resistance (Ohm)
        :param Icontrol: Control current (A)
        :param safe_duty_cycle: Safety factor for maximum payload mode (%)
        :return: None
        '''

        # set environment
        self.setEnvironment(temp, h)

        # set mass
        self.setMass(mass)

        # set number of rotors
        self.setNumberOfRotors(nr)

        # set propeller
        self.setPropeller(Dp, Hp, Bp)

        # set motor
        self.setMotor(Kv0, Um0, Im0, Rm)

        # set esc
        self.setESC(Re)

        # set battery
        self.setBattery(Ub, Cb, Cmin, Rb)

        # set control
        self.setControl(Icontrol)

        # set safety factor
        self.setSafetyFactor(safe_duty_cycle)

    def setEnvironment(self, temp, h):
        '''
        Set the environment
        :param temp: Temperature (°C)
        :param h: Altitude (m)
        :return: None
        '''

        self.temp = temp
        self.h = h

        # calculate air density
        self.pho = model.air_density(h, temp)

    def setMass(self, mass):
        '''
        Set the mass of the UAV
        :param G: weight of the uav (N)
        :return: None
        '''
        self.G = mass * self.g
    
    def setNumberOfRotors(self, nr):
        '''
        Set the number of rotors
        :param nr: Number of rotors (unit)
        :return: None
        '''
        self.nr = nr

    def setPropeller(self, Dp, Hp, Bp):
        '''
        Set the propeller parameters
        :param Dp: propeller diameter (in)
        :param Hp: propeller pitch (in)
        :param Bp: propeller blade number (unit)
        :return: None
        '''
        self.Dp = Dp * 0.0254
        self.Hp = Hp * 0.0254
        self.Bp = Bp

        # calculate propeller constants
        self.Ct = model.thrust_coefficient(Dp, Hp, Bp)
        self.Cm = model.torque_coefficient(Dp, Hp, Bp)

    def setMotor(self, Kv0, Um0, Im0, Rm):
        '''
        Set the motor parameters
        :param Kv0: Motor constant (rpm/V)
        :param Um0: Motor voltage at no-load (V)
        :param Im0: Motor current at no-load (A)
        :param Rm: Motor resistance (Ohm)
        :return: None
        '''
        self.Kv0 = Kv0
        self.Um0 = Um0
        self.Im0 = Im0
        self.Rm = Rm

    def setESC(self, Re):
        '''
        Set the ESC parameters
        :param Re: Equivalent resistance of the esc (Ohm)
        :return: None
        '''

        self.Re = Re

    def setBattery(self, Ub, Cb, Cmin, Rb):
        '''
        Set the battery parameters
        :param Ub: Battery voltage (V)
        :param Cb: Battery capacity (mAh)
        :param Cmin: Minimum battery capacity (mAh)
        :param Rb: Battery internal resistance (Ohm)
        :return: None
        '''

        self.Ub = Ub
        self.Cb = Cb
        self.Cmin = Cmin
        self.Rb = Rb

    def setControl(self, Icontrol):
        '''
        Set the control current
        :param Icontrol: Control current (A)
        :return: None
        '''

        self.Icontrol = Icontrol

    def setSafetyFactor(self, safe_duty_cycle):
        '''
        Set the safety factor
        :param safe_duty_cycle: Safety factor for maximum payload mode (%)
        :return: None
        '''

        self.safe_duty_cycle = safe_duty_cycle

    def show_config(self):

        # print the configuration

        print(f"{'-'*40}")
        print(f"{'UAV Model Configuration':^40}")
        print(f"{'-'*40}")
        print(f"{'-'*40}")
        print(f"{'Input parameters':^40}")
        print(f"{'-'*40}")
        print(f"{'Environment':^40}")
        print(f"{'Temperature:':<30}{self.temp:>10.3f} °C")
        print(f"{'Altitude:':<30}{self.h:>10.3f} m")
        print("")
        print(f"{'General':^40}")
        print(f"{'Mass:':<30}{self.G / self.g:>10.3f} Kg")
        print("")
        print(f"{'Propeller':^40}")
        print(f"{'Diameter:':<30}{self.Dp:>10.3f} m")
        print(f"{'Pitch:':<30}{self.Hp:>10.3f} m")
        print(f"{'Blade number:':<30}{self.Bp:>10.3f} units")
        print("")
        print(f"{'Motor':^40}")
        print(f"{'Motor constant:':<30}{self.Kv0:>10.3f} rpm/V")
        print(f"{'Motor no-load voltage:':<30}{self.Um0:>10.3f} V")
        print(f"{'Motor no-load current:':<30}{self.Im0:>10.3f} A")
        print(f"{'Motor resistance:':<30}{self.Rm:>10.3f} Ohm")
        print(f"{'Number of rotors:':<30}{self.nr:>10.3f} units")
        print("")
        print(f"{'ESC':^40}")
        print(f"{'Equivalent resistance:':<30}{self.Re:>10.3f} Ohm")
        print("")
        print(f"{'Battery':^40}")
        print(f"{'Battery voltage:':<30}{self.Ub:>10.3f} V")
        print(f"{'Battery capacity:':<30}{self.Cb:>10.3f} mAh")
        print(f"{'Minimum battery capacity:':<30}{self.Cmin:>10.3f} mAh")
        print(f"{'Battery internal resistance:':<30}{self.Rb:>10.3f} Ohm")
        print("")
        print(f"{'Others':^40}")
        print(f"{'Control current:':<30}{self.Icontrol:>10.3f} A")
        print(f"{'Max duty for max payload:':<30}{self.safe_duty_cycle:>10.3f} %")
        print("")
        print(f"{'-'*40}")
        print(f"{'Calculated parameters':^40}")
        print(f"{'-'*40}")
        print(f"{'Environment':^40}")
        print(f"{'Air density:':<30}{self.pho:>10.3f} kg/m^3")
        print("")
        print(f"{'Propeller':^40}")
        print(f"{'Thrust coefficient:':<30}{self.Ct:>10.3f}")
        print(f"{'Torque coefficient:':<30}{self.Cm:>10.3f}")
        print(f"{'-'*40}")
        print("")

    def calculate_performance(self, verbose=False):
        '''
        Calculate the performance of the UAV
        :return: None
        '''

        # calculate hover mode
        result = model.calculate_hover_mode(self.pho,
                                            self.G,
                                            self.Dp,
                                            self.Hp,
                                            self.Bp,
                                            self.Kv0,
                                            self.Um0,
                                            self.Im0,
                                            self.Rm,
                                            self.nr,
                                            self.Re,
                                            self.Ub,
                                            self.Cb,
                                            self.Cmin,
                                            self.Rb,
                                            self.Icontrol,
                                            verbose=verbose)

        self.T_hover = result[0]
        self.N_hover = result[1]
        self.M_hover = result[2]
        self.Um_hover = result[3]
        self.Im_hover = result[4]
        self.sigma_hover = result[5]
        self.Ue_hover = result[6]
        self.Ie_hover = result[7]
        self.Ib_hover = result[8]
        self.t_hover = result[9]
        self.eta = result[10]

        # # calculate maximum thrust mode
        result = model.calculate_max_thrust_mode(self.pho,
                                                 self.G,
                                                 self.Dp,
                                                 self.Hp,
                                                 self.Bp,
                                                 self.Kv0,
                                                 self.Um0,
                                                 self.Im0,
                                                 self.Rm,
                                                 self.nr,
                                                 self.Re,
                                                 self.Ub,
                                                 self.Cb,
                                                 self.Cmin,
                                                 self.Rb,
                                                 self.Icontrol,
                                                 verbose=verbose)

        self.T_max = result[0]
        self.N_max = result[1]
        self.M_max = result[2]
        self.Um_max = result[3]
        self.Im_max = result[4]
        self.sigma_max = result[5]
        self.Ue_max = result[6]
        self.Ie_max = result[7]
        self.Ib_max = result[8]
        self.t_max = result[9]
        self.eta = result[10]

        # # calculate maximum payload mode
        result = model.calculate_max_payload_mode(self.pho,
                                                  self.G,
                                                  self.Dp,
                                                  self.Hp,
                                                  self.Bp,
                                                  self.Kv0,
                                                  self.Um0,
                                                  self.Im0,
                                                  self.Rm,
                                                  self.nr,
                                                  self.Re,
                                                  self.Ub,
                                                  self.Cb,
                                                  self.Cmin,
                                                  self.Rb,
                                                  self.Icontrol,
                                                  self.safe_duty_cycle,
                                                  verbose=verbose)

        self.T_payload = result[0]
        self.N_payload = result[1]
        self.M_payload = result[2]
        self.Um_payload = result[3]
        self.Im_payload = result[4]
        self.sigma_payload = result[5]
        self.Ue_payload = result[6]
        self.Ie_payload = result[7]
        self.Ib_payload = result[8]
        self.t_payload = result[9]
        self.eta = result[10]
        self.max_payload = result[11]
        self.max_pitch = result[12]

        result = model.calculate_vel_and_distance(self.max_pitch,
                                                  self.pho,
                                                  self.G,
                                                  self.S,
                                                  self.C1,
                                                  self.C2,
                                                  self.Dp,
                                                  self.Hp,
                                                  self.Bp,
                                                  self.Kv0,
                                                  self.Um0,
                                                  self.Im0,
                                                  self.Rm,
                                                  self.nr,
                                                  self.Re,
                                                  self.Ub,
                                                  self.Cb,
                                                  self.Cmin,
                                                  self.Rb,
                                                  self.Icontrol,
                                                  verbose=verbose)

        self.max_distance = result[0]
        self.max_speed = result[1]

    def show_performance(self):
        print(f"{'-'*40}")
        print(f"{'UAV Performance':^40}")
        print(f"{'-'*40}")
        print(f"{'Hover mode':^40}")
        print(f"{'-'*40}")
        print(f"{'Thrust:':<30}{self.T_hover*self.nr:>10.3f} N")
        print(f"{'Thrust/motor:':<30}{self.T_hover:>10.3f} N")
        print(f"{'Motor speed:':<30}{self.N_hover:>10.3f} rpm")
        print(f"{'Motor torque:':<30}{self.M_hover:>10.3f} Nm")
        print(f"{'Motor voltage:':<30}{self.Um_hover:>10.3f} V")
        print(f"{'Motor current:':<30}{self.Im_hover:>10.3f} A")
        print(f"{'Duty cycle:':<30}{self.sigma_hover:>10.3f} %")
        print(f"{'ESC voltage:':<30}{self.Ue_hover:>10.3f} V")
        print(f"{'ESC current:':<30}{self.Ie_hover:>10.3f} A")
        print(f"{'Battery current:':<30}{self.Ib_hover:>10.3f} A")
        print(f"{'Flight time:':<30}{self.t_hover:>10.3f} min")
        print(f"{'Efficiency:':<30}{self.eta:>10.3f}")
        print("")
        print(f"{'Maximum thrust mode':^40}")
        print(f"{'-'*40}")
        print(f"{'Thrust:':<30}{self.T_max*self.nr:>10.3f} N")
        print(f"{'Thrust/motor:':<30}{self.T_max:>10.3f} N")
        print(f"{'Motor speed:':<30}{self.N_max:>10.3f} rpm")
        print(f"{'Motor torque:':<30}{self.M_max:>10.3f} Nm")
        print(f"{'Motor voltage:':<30}{self.Um_max:>10.3f} V")
        print(f"{'Motor current:':<30}{self.Im_max:>10.3f} A")
        print(f"{'Duty cycle:':<30}{self.sigma_max:>10.3f} %")
        print(f"{'ESC voltage:':<30}{self.Ue_max:>10.3f} V")
        print(f"{'ESC current:':<30}{self.Ie_max:>10.3f} A")
        print(f"{'Battery current:':<30}{self.Ib_max:>10.3f} A")
        print(f"{'Flight time:':<30}{self.t_max:>10.3f} min")
        print(f"{'Efficiency:':<30}{self.eta:>10.3f}")
        print("")
        print(f"{'Maximum payload mode':^40}")
        print(f"{'-'*40}")
        print(f"{'Thrust:':<30}{self.T_payload*self.nr:>10.3f} N")
        print(f"{'Thrust/motor:':<30}{self.T_payload:>10.3f} N")
        print(f"{'Motor speed:':<30}{self.N_payload:>10.3f} rpm")
        print(f"{'Motor torque:':<30}{self.M_payload:>10.3f} Nm")
        print(f"{'Motor voltage:':<30}{self.Um_payload:>10.3f} V")
        print(f"{'Motor current:':<30}{self.Im_payload:>10.3f} A")
        print(f"{'Duty cycle:':<30}{self.sigma_payload:>10.3f} %")
        print(f"{'ESC voltage:':<30}{self.Ue_payload:>10.3f} V")
        print(f"{'ESC current:':<30}{self.Ie_payload:>10.3f} A")
        print(f"{'Battery current:':<30}{self.Ib_payload:>10.3f} A")
        print(f"{'Flight time:':<30}{self.t_payload:>10.3f} min")
        print(f"{'Efficiency:':<30}{self.eta:>10.3f}")
        print(f"{'Maximum payload:':<30}{self.max_payload / self.g:>10.3f} Kg")
        print(f"{'Maximum pitch:':<30}{np.rad2deg(self.max_pitch):>10.3f} deg")
        print("")
        print(f"{'Reachability':^40}")
        print(f"{'-'*40}")
        print(f"{'Maximum distance:':<30}{self.max_distance:>10.3f} m")
        print(f"{'Maximum speed:':<30}{self.max_speed:>10.3f} m/s")
        print(f"{'-'*40}")
        print("")
    
    def show_all(self):
        self.show_config()
        self.show_performance()


if __name__ == '__main__':

    # Model Validation
    # Validation of Table 2, 3, 4, 5
    uav = UAVModel()
    uav.setAll(temp=25, h=10, mass=14.7 / uav.g, nr=4, Dp=10, Hp=4.5, Bp=2, Kv0=890, Um0=10, Im0=0.5,
               Rm=0.101, Re=0.008, Ub=12, Cb=5000, Cmin=5000 * 0.2, Rb=0.01, Icontrol=1, safe_duty_cycle=0.8)
    uav.show_config()
    uav.calculate_performance()
    uav.show_performance()

    # Validation of Table 6
    uav1 = UAVModel()
    uav1.setAll(temp=25, h=10, mass=14.7 / uav.g, nr=4, Dp=10, Hp=4.5, Bp=2, Kv0=890, Um0=10, Im0=0.5,
                Rm=0.101, Re=0.008, Ub=11.1, Cb=5000, Cmin=5000 * 0.2, Rb=0.0078, Icontrol=1, safe_duty_cycle=0.8)
    uav2 = UAVModel()
    uav2.setAll(temp=25, h=10, mass=28.763 / uav.g, nr=4, Dp=13, Hp=4.5, Bp=2, Kv0=415, Um0=10, Im0=0.3,
                Rm=0.2425, Re=0.008, Ub=22.2, Cb=5500, Cmin=5000 * 0.2, Rb=0.0114, Icontrol=1, safe_duty_cycle=0.8)
    uav3 = UAVModel()
    uav3.setAll(temp=25, h=10, mass=29.4 / uav.g, nr=4, Dp=12, Hp=5.5, Bp=2, Kv0=480, Um0=10, Im0=0.4,
                Rm=0.178, Re=0.006, Ub=22.2, Cb=5000, Cmin=5000 * 0.2, Rb=0.0168, Icontrol=1, safe_duty_cycle=0.8)
    
    uav1.calculate_performance()
    uav2.calculate_performance()
    uav3.calculate_performance()

    print("UAV1")
    uav1.show_performance()
    print("UAV2")
    uav2.show_performance()
    print("UAV3")
    uav3.show_performance()

    # Validation with DJI Inspire
    dji = UAVModel()
    dji.setAll(temp=25, h=10, mass=28.73 / uav.g, nr=4, Dp=13, Hp=4.5, Bp=2, Kv0=350, Um0=10, Im0=0.3,
               Rm=0.21, Re=0.02, Ub=24, Cb=5700, Cmin=5000 * 0.15, Rb=0.12, Icontrol=1, safe_duty_cycle=0.7)
    print("DJI Inspire")
    dji.show_config()
    dji.calculate_performance()
    dji.show_performance()
