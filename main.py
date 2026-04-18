import numpy as np
from matplotlib import pyplot as plt

from svg_analyzer import SvgAnalyzer
from fft_plotter import FftPlotter
from animation_maker import AnimationMaker

if __name__ == "__main__":
    save_path = "./files/rose.mp4"
    svg_path = "./files/rose.svg"
    save_path = None

    n_samples = 1024
    duration = 1
    n_circle = 401
    svg_analyzer = SvgAnalyzer(svg_path)
    route = svg_analyzer.compute_route(n_samples)

    fft_plotter = FftPlotter(route, n_circle)

    routes = fft_plotter.circle_centers
    radii = fft_plotter.circle_radii

    animation_maker = AnimationMaker(routes, radii, save_path)
    animation_maker.play(duration)
