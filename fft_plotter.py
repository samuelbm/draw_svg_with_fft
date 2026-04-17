import matplotlib.pyplot as plt
import numpy as np
from utils import sample_square

class FftPlotter:
    def __init__(self, route: np.ndarray, n_circles: int) -> None:
        self.route = route
        self.n_circles = n_circles
        self.N = len(route)
        self.c = np.fft.fftshift(np.fft.fft(route)) / self.N
        self.f = np.fft.fftshift(np.fft.fftfreq(self.N))

        n_half = int(self.N/2)
        m = int((n_circles-1)/2)
        self.c_approx = self.c[n_half - m: n_half + m + 1]
        self.f_approx = self.f[n_half - m: n_half + m + 1]

        idx = np.argsort(np.abs(self.c_approx))[::-1]
        self.c_ordered = self.c_approx[idx]
        self.f_ordered = self.f_approx[idx]

        n = np.arange(self.N)
        self.circle_centers = np.cumsum(
            self.c_ordered[:, None] *
            np.exp(1j * 2 * np.pi * self.f_ordered[:, None] * n[None, :]),
            axis=0
        )

        self.route_approx = self.circle_centers[-1, :]
        self.circle_radii = np.abs(self.c_ordered)


if __name__ == "__main__":
    N = 4096
    n_circles = 13
    route = sample_square(N)
    fft_plotter = FftPlotter(route, n_circles)
    route_approx = fft_plotter.route_approx
    circle_radii = fft_plotter.circle_radii
    circle_centers = fft_plotter.circle_centers

    fig, ax = plt.subplots()
    point_index = 234
    for n_circle in range(n_circles):

        radius = circle_radii[n_circle]
        if n_circle == 0:
            circle = plt.Circle((0, 0), radius, fill=False)
        elif n_circle < n_circles:
            center =(circle_centers[n_circle, point_index].real, circle_centers[n_circle, point_index].imag)
            circle = plt.Circle(center, radius, fill=False)
        ax.add_patch(circle)

        if n_circle == 0:
            line = plt.Line2D([0, circle_centers[n_circle, point_index].real], [0, circle_centers[n_circle, point_index].imag])
        else:
            line = plt.Line2D([circle_centers[n_circle-1, point_index].real, circle_centers[n_circle, point_index].real], [circle_centers[n_circle-1, point_index].imag, circle_centers[n_circle, point_index].imag])
        ax.add_line(line)

    ax.set_aspect('equal')
    plt.plot(route_approx.real, route_approx.imag)
    plt.show()