from itertools import islice, cycle
import time

import neopixel

from .get_pin import get_pin
from .audio_processing import audio_processing
from .wheel import wheel
from .generate_colors import generate_rgb


class StripManager:
    def __init__(self, pin_nr, npixels, order=neopixel.GRB):
        pixel_pin = get_pin(pin_nr)
        self.npixels = npixels
        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.npixels, brightness=0.2, auto_write=False, pixel_order=order
        )
        self.rainbow_cycle(1)

    def set_color(self, index, red, green, blue):
        self.pixels[index] = (red, green, blue)

    def set_all(self, table):
        [self.pixels.__setitem__(index, rgb) for index, rgb in enumerate(table)]

    def set_repeating(self, table):
        [
            self.pixels.__setitem__(index, rgb)
            for index, rgb in enumerate(islice(cycle(table), self.npixels))
        ]

    def rainbow_cycle(self, duration, cycles=1):
        for _ in range(cycles):
            for j in range(255):
                for i in range(self.npixels):
                    pixel_index = (i * 256 // self.npixels) + j
                    self.pixels[i] = wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(duration / 255)

    def visualize_audio(self, stream, chunk_size, rate, channels):
        notes_generator = audio_processing(stream, chunk_size, rate, channels, 5)
        rgb_generator = generate_rgb(5, normalize=True)
        for notes, rgb in zip(notes_generator, rgb_generator):
            rgb = rgb * notes[:, None]
            rgb = rgb.round().astype(int)
            self.set_repeating(rgb)
            self.pixels.show()
