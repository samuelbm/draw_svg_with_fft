import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationMaker:
    def __init__(self, route: np.ndarray):
        self.route = np.concatenate([route, route[::2]])
        self.x = np.real(self.route)
        self.y = np.imag(self.route)
        self.N = len(self.route)

        self.fig, self.ax = plt.subplots()

        self.line = self.ax.scatter([], [], s=3)

    def update(self, frame):
        self.line.set_offsets(np.c_[self.x[:frame], self.y[:frame]])
        return (self.line,)

    def play(self, time: float):
        interval = int(1000 * time / self.N)

        xmin, xmax = 1.1*np.min(self.x), 1.1*np.max(self.x)
        ymin, ymax = 1.1*np.min(self.y), 1.1*np.max(self.y)


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
    print("hello")
    duration = 3
    N = 3000
    r = 100
    t = np.linspace(0, 1, N, endpoint=True)
    route = r*np.exp(-1j*2*np.pi*t)

    animation_maker = AnimationMaker(route)
    animation_maker.play(duration)
    #TODO save the video




