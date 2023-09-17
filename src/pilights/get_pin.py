import board


def get_pin(nr):
    if nr == 10:
        return board.D10
    if nr == 12:
        return board.D12
    if nr == 18:
        return board.D18
    if nr == 21:
        return board.D21
    raise ValueError(f"Leds must be connected to one of the pins D10, D12, D18 or D21")
