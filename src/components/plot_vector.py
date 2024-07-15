import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from leap import datatypes as dt

def plot_vector(vec: dt.Vector):
    v = np.array([vec.x, vec.y, vec.z])

    # define empty figure
    fig = plt.figure()

    ax = plt.axes(projection="3d")
    ax.quiver(0, 0, 0, v[0], v[1], v[2], color="r")

    # set bounds
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # set title
    plt.title("Palm Vector Plot")

    plt.ion()
    plt.draw()
    plt.pause(0.5)

