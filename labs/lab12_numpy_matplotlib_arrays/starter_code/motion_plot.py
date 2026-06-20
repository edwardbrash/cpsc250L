import numpy as np
import matplotlib.pyplot as plt

def position(t, x0, v0, a):
    return x0 + v0 *t + 0.5*a*t**2

def velocity(t, v0, a):
    return v0 + a*t

def main():
    # TODO: create time array using np.linspace
    time = np.linspace(0, 10, 1000)
    # TODO: compute position and velocity arrays
    v0 = 50.0 # initial velocity in m/s
    angle = 45.0 # launch angle in degrees
    ay = -9.805 # acceleration due to gravity
    ax = 0.0    # ignore air resistance

    v0x = v0 * np.cos(angle*np.pi/180.0)
    v0y = v0 * np.sin(angle*np.pi/180.0)

    x0 = 0.0
    y0 = 0.0

    xpos = []
    ypos = []
    timepos = []
    velxpos = []
    velypos = []


    for t in time:
        x = position(t, x0, v0x, ax)
        y = position(t, y0, v0y, ay)
        vx = velocity(t, v0x, ax)
        vy = velocity(t, v0y, ay)
        xpos.append(x)
        ypos.append(y)
        timepos.append(t)
        velxpos.append(vx)
        velypos.append(vy)

    # TODO: make and save plots
    figure = plt.figure()
    fig, axes = plt.subplots(2,2)
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
