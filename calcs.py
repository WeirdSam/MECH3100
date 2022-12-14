"""
Created on Thu May  5 16:29:29 2022

Author: Samantha Nowland
MECH3600
The University of Queensland


Calculation tool for system/motor requirements of motor for MECH3100 
tractor design

Constants Input:
    Friction Coefficient of Sled: mu_sled
    Mass of Sled (estimate): mass_est_sled
    Gravity: gravity
    Rolling Resistance Coefficient of System Tire: c_tire_conc
    Estimated System Mass (including added weights): tractor_mass
    Maximum Time for Run Required = max_time
    Distance of Run: dist
    Coefficient between tire and concrete for system: mu_tractor
"""
#Imports
from math import cos 
from math import radians
from math import sin
from math import log
from math import pi
import numpy as np

#Functions
def normal(mass_est_sled, tractor_mass, gravity, theta):
    #Normal Force of Sled
    normal_sled = mass_est_sled * gravity * cos(radians(theta)) #N
    #Normal Force of System
    normal_tractor = tractor_mass * gravity * cos(radians(theta)) #N
    return normal_sled, normal_tractor


def friction(normal_sled, normal_tractor, mu_sled, c_tire_conc):
    #Friction force Due to Sled
    force_fric_sled = mu_sled * normal_sled #N
    
    #Rolling Resistance
    roll_res = c_tire_conc * normal_tractor #N
    
    #Resistance due to Gravity 
    grav_tract = tractor_mass * gravity * sin(radians(theta)) #N
    grav_sled = mass_est_sled * gravity * sin(radians(theta)) #N
    
    #Total Frictional Forces
    tractorfrict = roll_res + grav_tract #N
    winchfrict = force_fric_sled + grav_sled #N
    totalfrict = winchfrict + tractorfrict
    
    return tractorfrict, winchfrict, totalfrict


def traction(friction, normal_tractor, mu_tractor):
    #Traction Force
    tract_force = mu_tractor * normal_tractor
    if tract_force > friction:
        return 'traction force satisfactory', tract_force
    if tract_force < friction:
        return 'traction force UNSATISFACTORY', tract_force


def power(dist, time, totalfrict):  
    #Required Average Velocity
    minvel = dist/time #m/s 
    #Required Min Power
    p_req_min = totalfrict * minvel/nu
    #power is const through gear train
    return minvel, p_req_min   


def winchpower(dist, time, winchfrict):  
    #Required Average Velocity
    minvel = dist/time #m/s 
    #Required Min Power
    p_req_min = winchfrict * minvel/nu
    #power is const through gear train
    return minvel, p_req_min    


def iterate(dist, max_time, winchfrict, tractorfrict):
    tol = 0.05
    w_time = max_time/2
    w_v, P = winchpower(dist, w_time, winchfrict)
    t_v = P/tractorfrict
    t_time = dist/t_v
    time = t_time + w_time
    while abs(time - max_time) > tol:
            if max_time > time:
                w_time += 0.05
                w_v, P = winchpower(dist, w_time, winchfrict)
                t_v = P/tractorfrict
                t_time = dist/t_v
                time = t_time + w_time
            elif time > max_time:
                w_time -= 0.05
                w_v, P = winchpower(dist, w_time, winchfrict)
                t_v = P/tractorfrict
                t_time = dist/t_v
                time = t_time + w_time
            else:
                print('error')
    print(time, t_time, w_time, P, w_v, t_v)
    return P, w_v, t_v, w_time, t_time
    

def gearwinchsys(P, v_winch, v_tractor, t_winch, t_tractor, r_winch,  r_tractor, w_motor): 
    #angular velocity of tire(output)  
    w_winch = v_winch / r_winch
    w_tractor = v_tractor / r_tractor
    
    #torque output
    T_winch = P/w_winch
    T_tractor = P/w_tractor
    
    #required winch gear ratio
    GR_winch = w_motor/w_winch
    GR_tractor = w_motor/w_tractor
    return GR_winch, GR_tractor, T_winch, T_tractor, w_tractor, w_winch

    
#Values
mu_s_sled = 0.58 #static coefficient of friction used
mass_est_sled = 100 #kg - 85kg max ingot weight, plus equivalent sled weight
gravity = 9.81 #m/s**2 
theta = 5 #degrees
c_tire_conc = 0.002
tractor_mass = 60 #kg - assuming weight of tractor is 10kg so 50kg ballast is added
max_time = 1.5*60 #s - FOS of 1.33 - must complete pull under 2 minutes
dist = 7 #m
mu_tractor = 0.9 #(dry), 0.6 wet
nu = 0.8 #est gear efficiency

#gear vals
r_tractor = 0.1 #m
r_winch = 0.1 #m
Kv = 300 #rpm/V
V = 7.2 #V
w_motor = (Kv*V) * 2 * pi /60 #rad/s - 3000 is RPM
p_motor = 80 #W



#Calling Functions
normal_sled, normal_tractor = normal(mass_est_sled, tractor_mass, gravity, theta)
tractorfrict, winchfrict, totalfrict = friction(normal_sled, normal_tractor, mu_s_sled, c_tire_conc)
test, tract_force = traction(tractorfrict, normal_tractor, mu_tractor)
P, v_winch, v_tractor, t_winch, t_tractor = iterate(dist, max_time, winchfrict, tractorfrict)
min_vel, power = power(dist, max_time, totalfrict)
GR_winch, GR_tractor, T_winch, T_tractor, w_tractor, w_winch = gearwinchsys(p_motor, v_winch, v_tractor, t_winch, t_tractor, r_winch,  r_tractor, w_motor)



#Print
print("-"*50)
print('IMPORTANT MOTOR VALUES\n')

print(f'total friction force at max is: \n{tractorfrict, winchfrict} N\n')

print(f'traction force of system is: \n{tract_force} N\n')
   
print(f'min req power of motor for max friction and for winch velocity of {v_winch}m/s and  tractor velocity of {v_tractor}m/s is: \n{P} W\n')

print(f'power required for system without winch is {power} W, with minimum velocity of {min_vel}')

print(GR_winch, GR_tractor, T_winch, T_tractor, w_tractor, w_winch)