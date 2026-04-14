import numpy as np
from matplotlib import pyplot as plt

from svg_analyzer import SvgAnalyzer
from fft_plotter import FftPlotter
from animation_maker import AnimationMaker

if __name__ == "__main__":
    svg_path = "./files/music-note.svg"
    n_samples = 1000
    duration = 3
    n_circle = 980
    svg_analyzer = SvgAnalyzer(svg_path)
    route = svg_analyzer.compute_route(n_samples)

    fft_plotter = FftPlotter(route, n_circle)

    route_approx = fft_plotter.X_approx

    N =len(fft_plotter.route)
    t = np.linspace(0, N, N, False)
    x = fft_plotter.route
    y = fft_plotter.X_approx

    plt.plot(t, np.abs(x))
    plt.plot(t, np.abs(y))
    plt.show()

    # animation_maker = AnimationMaker(route_approx)
    # animation_maker.play(duration)