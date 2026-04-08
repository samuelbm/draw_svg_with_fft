import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------------------
# CONFIGURATION
# ---------------------------
NUM_CIRCLES = 6
RADII = np.linspace(1.5, 0.2, NUM_CIRCLES)  # big → small
SPEEDS = np.linspace(1, 5, NUM_CIRCLES)     # angular speeds

# Function that defines motion (you can modify this)
def f(t, i):
    return SPEEDS[i] * t

# ---------------------------
# SETUP FIGURE
# ---------------------------
fig, ax = plt.subplots()
ax.set_facecolor("black")
ax.set_aspect("equal")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.axis("off")

# Circles and lines storage
circles = []
line, = ax.plot([], [], color="blue", lw=2)

# Create circle patches
for r in RADII:
    circle = plt.Circle((0, 0), r, fill=False, edgecolor="red", alpha=0.5, lw=1.5)
    ax.add_patch(circle)
    circles.append(circle)

# ---------------------------
# ANIMATION FUNCTION
# ---------------------------
def update(frame):
    t = frame * 0.05

    centers_x = []
    centers_y = []

    x, y = 0, 0

    # Compute chained circle centers
    for i in range(NUM_CIRCLES):
        angle = f(t, i)

        x += RADII[i] * np.cos(angle)
        y += RADII[i] * np.sin(angle)

        centers_x.append(x)
        centers_y.append(y)

        circles[i].center = (x, y)

    # Update connecting line
    line.set_data(centers_x, centers_y)

    return circles + [line]

# ---------------------------
# RUN ANIMATION
# ---------------------------
ani = FuncAnimation(fig, update, frames=1000, interval=30, blit=True)

plt.show()