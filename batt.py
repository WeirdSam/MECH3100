# -*- coding: utf-8 -*-
"""
Created on Sun May 22 15:11:23 2022

Author: Samantha Nowland
"""
from math import pi
from math import log
from math import trunc

r_est = 0.1 #m
w_motor = 4500 * 2 * pi /60 #rad/s - 3000 is RPM
p_motor = 50 #W
dist = 7 #m
time = 1.5*60 #s

min_vel = dist/time

def gear(min_vel, r_est, p_req_min, w_motor): 
    #angular velocity of tire(output)  
    w_tire = min_vel / r_est
    T_est_tire = p_req_min/w_tire
    #required gear ratio
    GR = w_motor/w_tire
    
    #for planetary gear config x is number of stages requires
    x = log(GR, 3)
    y = trunc(x)
    pla_GR = 3**y
    spur_GR = GR / pla_GR
    spur_pin = 16
    spur_gear = round(spur_pin * spur_GR,0)
    return GR, y, T_est_tire, spur_gear, pla_GR, spur_pin, spur_GR
GR, x, T_est, spur_gear, pla_GR, spur_pin, spur_GR = gear(min_vel, r_est, p_motor, w_motor)


print(f'required gear ratio is {GR} and number of gear levels for design is {x}')
print(f'this will acheive a gear ratio of {pla_GR}, and therefore spur gears will be also required')
print(f'required spur gear ratio is {spur_GR}, and can be acheived with a pinion gear with {spur_pin} teeth, and a driven gear with {spur_gear} teeth')
print(f'the overall gear ratio will be {pla_GR*(spur_gear/spur_pin)} which is acceptable')


#battery requirements
volt = 7.2 #V, other volatges may be used
des_time = 15/60 #hrs, must be able to do 5*2minute passes - 10 minutes, FOS of 1.5, therefore 20 minute battery operation time required
eff = 0.85 #85% efficiency to account for circuit board power draw and not purely efficient system
#power draw from motor (2 motors each at 50W power)
power_draw = p_motor * 2

#battery amp-hr required
amp = power_draw * des_time / (volt * eff)
print(f'required Amp-hours with {volt}V battery is {amp}')



