import matplotlib.pyplot as plt
import numpy as np

class FftPlotter:
    def __init__(self, route: np.ndarray, n_circles):
        print(f"route shape = {route.shape}")
        self.route = route
        N = len(route)

        # 1. FULL FFT (no truncation yet)
        X = np.fft.fft(route) / N
        freqs = np.fft.fftfreq(N)

        #2. shift (optional, but keep consistent)
        X = np.fft.fftshift(X)
        freqs = np.fft.fftshift(freqs)

        # 3. sort by magnitude (global ranking)
        idx = np.argsort(np.abs(X))[::-1]

        X = X[idx]
        freqs = freqs[idx]

        # 4. NOW truncate
        X = X[:n_circles]
        freqs = freqs[:n_circles]

        self.coefficients = X
        self.freqs = freqs

        c = np.array(self.coefficients)
        k = np.arange(N)
        n = np.arange(N)

        self.X_approx = np.sum(
            c[:, None] * np.exp(1j * 2 * np.pi * k[:, None] * n[None, :] / N),
            axis=0
        )


def sample_square(N):
    t = np.linspace(0, 4, N, endpoint=False)  # 4 sides
    points = np.zeros(N, dtype=complex)

    for i, ti in enumerate(t):
        if ti < 1:
            # bottom edge: (-1,-1) → (1,-1)
            x = -1 + 2*ti
            y = -1
        elif ti < 2:
            # right edge: (1,-1) → (1,1)
            x = 1
            y = -1 + 2*(ti - 1)
        elif ti < 3:
            # top edge: (1,1) → (-1,1)
            x = 1 - 2*(ti - 2)
            y = 1
        else:
            # left edge: (-1,1) → (-1,-1)
            x = -1
            y = 1 - 2*(ti - 3)

        points[i] = x + 1j*y

    return points


if __name__ == "__main__":
    N = 4096
    n_circles = 31
    route = sample_square(N)
    fft_plotter = FftPlotter(route, n_circles)

    coefficients = fft_plotter.coefficients
    freqs = fft_plotter.freqs

    plt.stem(freqs, np.log10(np.abs(coefficients)))
    plt.show()