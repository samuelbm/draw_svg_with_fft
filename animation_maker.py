import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationMaker:
    def __init__(self, circle_routes: np.ndarray, circle_radii: np.ndarray, save_path: str):
        self.save_path = save_path
        self.circle_routes = circle_routes
        self.circle_radii = circle_radii
        self.n_circles, self.N = self.circle_routes.shape
        self.curve = self.circle_routes[-1]

        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor("black")
        self.ax.set_facecolor("black")

        # IMPORTANT: unpack Line2D
        self.route, = self.ax.plot([], [], color="orange", linewidth=1)

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
            self.ax.add_patch(circle)

            line = plt.Line2D(
                [0],
                [0],
                color="white",
                alpha=0.8,
                linewidth=1
            )
            self.lines.append(line)
            self.ax.add_line(line)

    def update(self, frame):
        frame = frame % self.N
        # draw curve progressively
        self.route.set_data(
            self.curve[:frame].real,
            self.curve[:frame].imag
        )

        for i in range(self.n_circles):

            if i == 0:
                center = (0, 0)
            else:
                center = (
                    self.circle_routes[i-1, frame].real,
                    self.circle_routes[i-1, frame].imag
                )

            self.circles[i].center = center

            if i == 0:
                self.lines[i].set_data(
                    [0, self.circle_routes[i, frame].real],
                    [0, self.circle_routes[i, frame].imag]
                )
            else:
                self.lines[i].set_data(
                    [
                        self.circle_routes[i - 1, frame].real,
                        self.circle_routes[i, frame].real
                    ],
                    [
                        self.circle_routes[i - 1, frame].imag,
                        self.circle_routes[i, frame].imag
                    ]
                )

        return (self.route, *self.circles, *self.lines)

    def play(self, time: float):
        interval = np.max([int(1000 * time / self.N), 1])

        # compute bounds
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
        minimum = np.min([xmin, ymin])
        maximum = np.max([xmax, ymax])

        self.ax.set_aspect("equal")
        self.ax.set_xlim(minimum, maximum)
        self.ax.set_ylim(minimum, maximum)
        self.ax.axis("off")

        self.anim = FuncAnimation(
            self.fig,
            self.update,
            frames=5*self.N,
            interval=interval,
            blit=False
        )

        if self.save_path is not None:
            self.anim.save(
                self.save_path,
                writer="ffmpeg",
                fps=100,
                dpi=300
            )
            print("Done!")
        else:
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
