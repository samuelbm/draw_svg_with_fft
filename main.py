from svg_analyzer import SvgAnalyzer
from fft_plotter import FftPlotter
from animation_maker import AnimationMaker

if __name__ == "__main__":
    svg_path = "./files/music-note.svg"
    n_samples = 1000
    duration = 3
    svg_analyzer = SvgAnalyzer(svg_path)
    route = svg_analyzer.compute_route(n_samples)

    animation_maker = AnimationMaker(route)
    animation_maker.play(duration)