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

        # Lengths
        lengths = [p.length() for p in paths]
        total_length = sum(lengths)

        # Cumulative lengths (important!)
        cumulative = np.cumsum([0] + lengths)

        # EXACT number of samples
        distances = np.linspace(0, total_length, n_samples, endpoint=False)

        points = []

        for d in distances:
            # Find which path this distance falls into
            i = np.searchsorted(cumulative, d, side="right") - 1

            # Local distance inside that path
            local_d = d - cumulative[i]

            path = paths[i]

            # Clamp for safety
            local_d = min(max(local_d, 0.0), lengths[i] - 1e-12)

            t = path.ilength(local_d)
            z = path.point(t)
            points.append(z)

        route = np.array(points, dtype=np.complex128)

        # Normalize
        route -= np.mean(route)
        route /= np.max(np.abs(route))

        # Flip Y axis
        route = np.conj(route)

        return route


if __name__ == "__main__":
    svg_path = "./files/music-note.svg"
    n_samples = 1024

    analyzer = SvgAnalyzer(svg_path)
    route = analyzer.compute_route(n_samples)


    plt.figure()
    plt.scatter(route.real, route.imag, s=2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Sampled SVG Path")
    plt.show()