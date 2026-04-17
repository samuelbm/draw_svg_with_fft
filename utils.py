import numpy as np

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