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
    df = pd.read_csv('out.csv', usecols=["Vin", "Vout"])
    xs = df.loc[:, "Vin"]
    ys = df.loc[:, "Vout"]

    # Create matplotlib Figure and Axes
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Embellishments
    plt.grid(color='lightgray')
    plt.title('ECE295 M0 Line Regulation')

    # Plot the surface
    ax.scatter(xs, ys, zorder=99)

    ax.set_xlabel('Vin')
    ax.set_xticks(np.arange(min(xs), max(xs)+1, 2.5))
    ax.set_xlim(left=0.0)
    ax.set_ylabel('Vout')
    ax.set_yticks(np.arange(min(ys), max(ys)+1, 0.5))
    ax.set_ylim(bottom=0.0)

    plt.savefig('out.png', dpi=600)


if __name__ == "__main__":
    main()
