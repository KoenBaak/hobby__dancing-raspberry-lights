import time
import numpy as np
from colorsys import hsv_to_rgb


def generate_rgb(n, normalize=False):
    while True:
        t = time.time()
        waveforms = np.array(
            [
                np.sin(0.1 * i + np.sin(t * 0.27) * 4)
                + np.sin(0.3 * i + np.sin(t * 0.17) * 3)
                for i in range(n)
            ]
        )
        waveforms = ((waveforms / 2) + 1) / 2
        colors = np.array([hsv_to_rgb(v, 1, 1) for v in waveforms])

        if normalize:
            colors = colors / np.sum(colors, axis=1)[:, None]

        yield colors * 220
