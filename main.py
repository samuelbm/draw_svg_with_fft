import numpy as np
from matplotlib import pyplot as plt

from svg_analyzer import SvgAnalyzer
from fft_plotter import FftPlotter
from animation_maker import AnimationMaker

if __name__ == "__main__":
    svg_path = "./files/music-note.svg"
    n_samples = 4096
    duration = 3
    n_circle = 4001
    svg_analyzer = SvgAnalyzer(svg_path)
    route = svg_analyzer.compute_route(n_samples)

    fft_plotter = FftPlotter(route, n_circle)

    route_approx = fft_plotter.route_approx
    route = fft_plotter.route

    animation_maker = AnimationMaker(route_approx)
    animation_maker.play(duration)

    # plt.scatter(route.real, route.imag)
    # plt.scatter(route_approx.real, route_approx.imag)
    # plt.show()

