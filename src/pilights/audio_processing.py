import numpy as np


def human_hearing_multiplier(freq):
    points = {
        0: -10,
        50: -8,
        100: -4,
        200: 0,
        500: 2,
        1000: 0,
        2000: 2,
        5000: 4,
        10000: -4,
        15000: 0,
        20000: -4,
    }

    xs = list(points.keys())

    for index, x in enumerate(xs[:-1]):
        if x <= freq < xs[index + 1]:
            x0 = x
            x1 = xs[index + 1]
            break

    y0, y1 = points[x0], points[x1]
    decibels = ((x1 - freq) * y0 + (freq - x0) * y1) / (x1 - x0)
    return 10 ** (decibels / 10)


def real_fft(im):
    im = np.abs(np.fft.fft(im))
    re = im[: len(im) // 2]
    re[1:] += im[len(im) // 2 + 1 :][::-1]
    return re


def audio_processing(
    audio_stream,
    chunk_size: int,
    rate: int,
    channels: int,
    num_notes: int,
    peak_falloff: float = 0.9,
    smooth_falloff: float = 0.9,
):
    freqs = [(rate * i) / chunk_size for i in range(num_notes)]
    human_ear_multipliers = np.array([human_hearing_multiplier(f) for f in freqs])

    avg_peak = 0.0
    smooth = None

    for data in audio_stream:
        samples = np.fromstring(data, dtype=np.int16)
        left = samples[::2]
        right = samples[1::2]

        # apply real fft
        notes = real_fft(left) + real_fft(right)

        # cut off at num_notes
        notes = notes[:num_notes]

        notes = notes * human_ear_multipliers

        peak = np.max(notes)
        if peak > avg_peak:
            avg_peak = peak
        else:
            avg_peak = avg_peak * peak_falloff + (1 - peak_falloff) * peak

        if avg_peak > 0:
            notes = notes / avg_peak

        notes = notes**2

        if smooth is None:
            smooth = notes
        else:
            smooth = smooth * smooth_falloff + notes * (1 - smooth_falloff)

        yield smooth
