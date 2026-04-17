import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationMaker:
    def __init__(self, circle_routes: np.ndarray, circle_radii: np.ndarray):
        self.circle_routes = circle_routes
        self.circle_radii = circle_radii
        self.n_circles, self.N = self.circle_routes.shape
        self.curve = self.circle_routes[-1]

        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor("black")
        self.ax.set_facecolor("black")
        self.route = self.ax.scatter([], [], s=0.5, color="orange")
        self.circles = []
        self.lines = []

        for circle_index in range(self.n_circles):

            circle = plt.Circle(
                (0, 0),
                self.circle_radii[circle_index],
                color="yellow",
                alpha=0.2,
                fill=False,
                linewidth=1
            )
            self.circles.append(circle)
            self.ax.add_patch(self.circles[circle_index])

            line = plt.Line2D(
                [0],
                [0],
                color="white",
                alpha=0.8,
                linewidth=1
            )
            self.lines.append(line)
            self.ax.add_line(self.lines[circle_index])


    def update(self, frame):
        self.route.set_offsets(np.c_[self.curve[:frame].real, self.curve[:frame].imag])

        for circle_index in range(self.n_circles):
            if circle_index == 0:
                self.circles[circle_index].center = (0, 0)
            elif circle_index < self.n_circles:
                center = (self.circle_routes[circle_index-1, frame].real,
                          self.circle_routes[circle_index-1, frame].imag
                          )
                self.circles[circle_index].center = center

            self.lines[circle_index].set_data([0, 1], [0, 1])
            if circle_index == 0:
                self.lines[circle_index].set_data(
                    [0, self.circle_routes[circle_index, frame].real],
                    [0, self.circle_routes[circle_index, frame].imag]
                )
            elif circle_index < self.n_circles:
                self.lines[circle_index].set_data(
                    [
                        self.circle_routes[circle_index - 1, frame].real,
                        self.circle_routes[circle_index, frame].real
                    ],
                    [
                        self.circle_routes[circle_index - 1, frame].imag,
                        self.circle_routes[circle_index, frame].imag
                    ]
                )

        return self.route, *self.circles, *self.lines

    def play(self, time: float):
        interval = int(1000 * time / self.N)

        all_real = np.concatenate([
            self.curve.real,
            np.real(self.circle_routes).ravel()
        ])

        all_imag = np.concatenate([
            self.curve.imag,
            np.imag(self.circle_routes).ravel()
        ])

        xmin, xmax = 1.1 * np.min(all_real), 1.1 * np.max(all_real)
        ymin, ymax = 1.1 * np.min(all_imag), 1.1 * np.max(all_imag)

        self.ax.set_facecolor("black")
        self.ax.set_aspect("equal")
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.ax.axis("off")

        ani = FuncAnimation(
            self.fig,
            self.update,
            frames=self.N,
            interval=interval,
            blit=True
        )

        plt.show()

if __name__ == "__main__":
    N = 1024
    n_circles = 13
    duration = 3
    radii = np.linspace(10, 20, n_circles, endpoint=True)
    t = np.linspace(0, 2, N, endpoint=True)
    k = np.linspace(0, 2, n_circles, endpoint=True)
    routes = np.cumsum(t[None, :] + 0.2 * np.exp(1j * (np.pi * t[None, :] + k[:, None])), axis=1)

    animation_maker = AnimationMaker(routes, radii)
    animation_maker.play(duration)
    # #TODO save the video
