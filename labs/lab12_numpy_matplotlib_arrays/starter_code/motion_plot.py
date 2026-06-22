import numpy as np
import matplotlib.pyplot as plt

def position(t, x0, v0, a):
    return x0 + v0 *t + 0.5*a*t**2

def velocity(t, v0, a):
    return v0 + a*t

def main():
    v0 = 50.0 # initial velocity in m/s
    angle = 30.0 # launch angle in degrees
    ay = -9.805 # acceleration due to gravity
    ax = 0.0    # ignore air resistance
    x0 = 0.0
    y0 = 0.0
    v0x = v0 * np.cos(angle*np.pi/180.0)
    v0y = v0 * np.sin(angle*np.pi/180.0)

    # TODO: create time array using np.linspace
    tmax = -2.0*v0y/ay
    time = np.linspace(0, tmax, 1000)
    # TODO: compute position and velocity arrays

    xpos = position(time,x0,v0x,ax)
    ypos = position(time,y0,v0y,ay)
    velxpos = velocity(time,v0,ax)
    velypos = velocity(time,v0,ay)

    # TODO: make and save plots
    figure, axes = plt.subplots(2,2)

    axes[0][0].plot(time, xpos, label="x position")
    axes[0][0].set_title("X position")
    axes[0][0].set_xlabel("time (s)")
    axes[0][0].set_ylabel("x (m)")

    axes[0][1].plot(time, ypos, label="y position")
    axes[0][1].set_title("Y position")
    axes[0][1].set_xlabel("time (s)")
    axes[0][1].set_ylabel("y (m)")

    axes[1][0].plot(time, velxpos, label="x velocity")
    axes[1][0].set_title("X Velocity")
    axes[1][0].set_xlabel("time (s)")
    axes[1][0].set_ylabel("vx (m/s)")

    axes[1][1].plot(time, velypos, label="y velocity")
    axes[1][1].set_title("Y velocity")
    axes[1][1].set_xlabel("time (s)")
    axes[1][1].set_ylabel("vy (m/s)")

    plt.tight_layout(pad=2.0, w_pad=1.5, h_pad=1.5)
    plt.show()

main()
