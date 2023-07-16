#!/usr/bin/env python3

import numpy as np

import uav_model as model


class UAVModel:

    g = 9.81  # m/s^2

    def __init__(self) -> None:
        return None

    def setEnvironment(self, temp, h):
        '''
        Set the environment
        :param temp: Temperature
        :param h: Altitude
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

    def setPropeller(self, Dp, Hp, Bp):
        '''
        Set the propeller parameters
        :param Dp: propeller diameter
        :param Hp: propeller pitch
        :param Bp: propeller blade number
        :return: None
        '''
        self.Dp = Dp
        self.Hp = Hp
        self.Bp = Bp

        # calculate propeller constants
        self.Ct = model.thrust_coefficient(Dp, Hp, Bp)
        self.Cm = model.torque_coefficient(Dp, Hp, Bp)

    def setMotor(self, Kv0, Um0, Im0, Rm, nr):
        '''
        Set the motor parameters
        :param Kv0: Motor constant
        :param Um0: Motor voltage
        :param Im0: Motor current
        :param Rm: Motor resistance
        :param nr: Number of rotors
        :return: None
        '''
        self.Kv0 = Kv0
        self.Um0 = Um0
        self.Im0 = Im0
        self.Rm = Rm
        self.nr = nr

    def setESC(self, Re):
        '''
        Set the ESC parameters
        :param Re: Equivalent resistance of the esc
        :return: None
        '''

        self.Re = Re

    def setBattery(self, Ub, Cb, Cmin, Rb):
        '''
        Set the battery parameters
        :param Ub: Battery voltage
        :param Cb: Battery capacity
        :param Cmin: Minimum battery capacity
        :param Rb: Battery internal resistance
        :return: None
        '''

        self.Ub = Ub
        self.Cb = Cb
        self.Cmin = Cmin
        self.Rb = Rb

    def setControl(self, Icontrol):
        '''
        Set the control current
        :param Icontrol: Control current
        :return: None
        '''

        self.Icontrol = Icontrol

    def setSafetyFactor(self, safe_duty_cycle):
        '''
        Set the safety factor
        :param safe_duty_cycle: Safety factor for maximum payload mode
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

    def calculate_performance(self):
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
                                            self.Icontrol)

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
                                                 self.Icontrol)

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
                                                  self.Icontrol)

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
        print(f"{'-'*40}")


if __name__ == '__main__':

    # initialize UAVModel
    uav = UAVModel()

    # set environment
    uav.setEnvironment(temp=25, h=10)

    # set mass
    uav.setMass(mass=1.47)

    # set propeller
    uav.setPropeller(Dp=10 * 0.0254, Hp=4.5 * 0.0254, Bp=2)

    # set motor
    uav.setMotor(Kv0=890, Um0=10, Im0=0.5, Rm=0.101, nr=4)

    # set esc
    uav.setESC(Re=0.008)

    # set battery
    uav.setBattery(Ub=12, Cb=5000, Cmin=0.2 * 5000, Rb=0.01)

    # set control
    uav.setControl(Icontrol=1)

    # set safety factor
    uav.setSafetyFactor(safe_duty_cycle=0.8)

    # show configuration
    uav.show_config()

    # calculate performance
    uav.calculate_performance()

    # show performance
    uav.show_performance()
