import numpy as np
from svgpathtools import svg2paths
import matplotlib.pyplot as plt


class SvgAnalyzer:
    def __init__(self, svg_path: str):
        self.svg_path = svg_path

    def compute_route(self, n_samples: int) -> np.ndarray:
        paths, _ = svg2paths(self.svg_path)

        if len(paths) == 0:
            raise ValueError("No paths found in SVG")

        # Compute total length
        lengths = [p.length() for p in paths]
        total_length = sum(lengths)

        points = []

        for path, length in zip(paths, lengths):
            if length == 0:
                continue

            # Allocate samples proportionally
            n = max(2, int(n_samples * (length / total_length)))

            # IMPORTANT: avoid hitting exactly `length`
            distances = np.linspace(0, length, n, endpoint=False)

            for d in distances:
                # Extra safety clamp
                d = min(max(d, 0.0), length - 1e-12)

                t = path.ilength(d)
                z = path.point(t)
                points.append(z)

        route = np.array(points, dtype=np.complex128)

        # Optional: center and normalize (VERY useful for FFT later)
        route -= np.mean(route)
        route /= np.max(np.abs(route))

        # SVG Y axis goes down → flip it
        route = np.conj(route)

        return route


if __name__ == "__main__":
    svg_path = "./files/music-note.svg"
    n_samples = 1000

    analyzer = SvgAnalyzer(svg_path)
    route = analyzer.compute_route(n_samples)


    plt.figure()
    plt.scatter(route.real, route.imag, s=2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Sampled SVG Path")
    plt.show()