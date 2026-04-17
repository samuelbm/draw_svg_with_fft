import numpy as np
from matplotlib import pyplot as plt

from svg_analyzer import SvgAnalyzer
from fft_plotter import FftPlotter
from animation_maker import AnimationMaker

if __name__ == "__main__":
    svg_path = "./files/music-note.svg"
    n_samples = 1024
    duration = 3
    n_circle = 11
    svg_analyzer = SvgAnalyzer(svg_path)
    route = svg_analyzer.compute_route(n_samples)

    fft_plotter = FftPlotter(route, n_circle)

    routes = fft_plotter.circle_centers
    radii = fft_plotter.circle_radii

    test = fft_plotter.route_approx
    plt.plot(test.real, test.imag)
    plt.show()

    # animation_maker = AnimationMaker(routes, radii)
    # animation_maker.play(duration)
