import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#We define the initializing parameters

H = 35                 # cells row
W = 35                 # cells columns
N = H * W              # total cells

K = 2.5                # accoplament force
dt = 0.04              # step time
steps = 600             # steps

#We generate a randomizer using 4 as the seed 

rng = np.random.default_rng(4)

# We proceed to generate each cell frequency (we get a matrix of frequencys)
omega = rng.normal(
    loc=1.0,
    scale=0.15,
    size=(H, W)
)

# We proceed to generate a random phase for each cell between 0 and 2pi (this is a matrix as well)
theta = rng.uniform(
    0,
    2 * np.pi,
    size=(H, W)
)

#To save the evolution
theta_history = []
R_history = []

#We proceed with the simulation
for step in range(steps):
    #We roll the matrix to right, left , up and down
    right = np.roll(theta, -1, axis=1)
    left = np.roll(theta, 1, axis=1)
    down = np.roll(theta, -1, axis=0)
    up = np.roll(theta, 1, axis=0)

    #To neutralize the non-end borders

    right[:, -1] = theta[:, -1]
    left[:, 0] = theta[:, 0]
    down[-1, :] = theta[-1, :]
    up[0, :] = theta[0, :]

   #Now we subtract the previous rolled matrixes from the original phase one, 
   # so we get a number that represents the difference between the phase 
   # of for example a11 from its "neighbours" such as a12 or b11
    coupling = (
        np.sin(right - theta)
        + np.sin(left - theta)
        + np.sin(up - theta)
        + np.sin(down - theta)
    )

    #We proceed to apply kuramotos equation
    # dθ/dt = ω + K * interaction

    theta = theta + dt * (
        omega + K * coupling / 4
    )

    #We save the state 
    theta_history.append(theta.copy())

    #We proceed to calculate the order parameter R, we use the phases of each cell
    #to represent each phase as a vector using Euler's formula.
    #if all the cells point in the same direction, the vectors reinforce each other
    #and R will be close to 1. If the cells point in different directions,
    #the vectors cancel each other and R will be close to 0.

    R = np.abs(
        np.mean(
            np.exp(1j * theta)
        )
    )

    R_history.append(R)


theta_history = np.array(theta_history)
R_history = np.array(R_history)

#We proceed to code the visualization
fig = plt.figure(figsize=(10, 7))

#We create the main area where we will visualize the cells
ax = fig.add_axes([0.05, 0.15, 0.62, 0.75])

#We create a second area where we will visualize the synchronization parameter R over time
ax_graph = fig.add_axes([0.72, 0.20, 0.25, 0.65])


#We create a grid of coordinates for each cell
x, y = np.meshgrid(
    np.arange(W),
    np.arange(H)
)

#We define the initial size of each cell
initial_size = 30

#We create a scatter plot where each point represents one cell
#the position of each cell is given by x and y
#the color of each cell represents its phase theta
scatter = ax.scatter(
    x.flatten(),
    y.flatten(),
    s=initial_size,
    c=theta_history[0].flatten(),
    cmap="hsv",
    vmin=0,
    vmax=2 * np.pi
)

#We define the limits of the visualization
ax.set_xlim(-1, W)
ax.set_ylim(-1, H)

#We make sure that the cells have the same scale in both axes
ax.set_aspect("equal")

#We remove the numbers from the x and y axes
ax.set_xticks([])
ax.set_yticks([])

#We add a title to the visualization
ax.set_title(
    "Kuramoto Model\n"
    "From independent oscillators to synchronization",
    fontsize=10
)


# We create a text element that will show the current synchronization value
phase_text = ax.text(
    0.02,
    0.97,
    "",
    transform=ax.transAxes,
    fontsize=11,
    verticalalignment="top"
)


#We define the limits of the synchronization graph
#the x axis represents time and the y axis represents the synchronization R
ax_graph.set_xlim(
    0,
    steps * dt
)

ax_graph.set_ylim(
    0,
    1.05
)

#We add labels to both axes
ax_graph.set_xlabel("Time")
ax_graph.set_ylabel("R")

#We add a title to the synchronization graph
ax_graph.set_title(
    "Synchronization"
)

#We add a light grid to make the graph easier to read
ax_graph.grid(
    alpha=0.2
)

#We create an empty line that will represent the evolution of R over time
line_R, = ax_graph.plot(
    [],
    [],
    linewidth=2
)

#We create a vertical line that will indicate the current moment of the simulation
current_time = ax_graph.axvline(
    0,
    linestyle="--",
    linewidth=1
)


#We create the function that will update the visualization at each frame
def update(frame):

    #We obtain the phase of every cell at the current frame
    current_theta = theta_history[frame]

    #We use the phase of each cell to determine its color
    scatter.set_array(
        current_theta.flatten()
    )

    #We create a pulsating effect for the cells using their current phase
    #cells change their size according to sin(theta)
    pulse = (
        1
        + 0.8 * (
            (np.sin(current_theta) + 1) / 2
        )
    )

    #We calculate the size of each cell according to its current phase
    sizes = initial_size * pulse.flatten()

    #We update the size of every cell
    scatter.set_sizes(
        sizes
    )

    #We obtain the synchronization value R at the current frame
    R = R_history[frame]

    #We display the current synchronization value on the visualization
    phase_text.set_text(
        f"Synchronization R = {R:.2f}"
    )

    #We create the time values corresponding to the frames
    times = np.arange(frame + 1) * dt

    #We update the synchronization graph with all the R values calculated so far
    line_R.set_data(
        times,
        R_history[:frame + 1]
    )

    #We move the vertical line to the current time of the simulation
    current_time.set_xdata(
        [frame * dt, frame * dt]
    )

    #We return the elements that have been updated
    return (
        scatter,
        phase_text,
        line_R,
        current_time
    )

#Now we generate the animation
animation = FuncAnimation(
    fig,
    update,
    frames=steps,
    interval=30,
    blit=True
)

plt.show()

#We save as .gif
import os

animation.save(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "kuramoto.gif"
    ),
    writer="pillow",
    fps=30
)