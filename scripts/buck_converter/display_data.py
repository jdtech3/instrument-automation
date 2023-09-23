import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create x, y coords
# nx, ny = 17, 5      # x: voltage, y: current
# cellsize = 1.
# x = np.arange(0., float(nx), 1.) * cellsize
# y = np.arange(0., float(ny), 1.) * cellsize
# X, Y = np.meshgrid(x, y)

def main():
    # data
    df = pd.read_csv('out.csv', usecols=["Vin", "Iout", "Efficiency"])
    xs = df.loc[:, "Vin"]
    ys = df.loc[:, "Iout"]
    zs = df.loc[:, "Efficiency"]

    # Create matplotlib Figure and Axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    ax.scatter(xs, ys, zs)

    ax.set_xlabel('Vin')
    ax.set_ylabel('Iout')
    ax.set_zlabel('Efficiency')

    plt.show()


if __name__ == "__main__":
    main()
