"""Utilitaires internes partagés."""


def clamp(value, low, high):
    return max(low, min(high, value))


def hex_to_rgb(color):
    """Convertit '#RRGGBB' en tuple (r, g, b)."""
    color = color.lstrip("#")
    if len(color) == 3:
        color = "".join(c * 2 for c in color)
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


def shade(color, factor):
    """Éclaircit (factor > 0) ou assombrit (factor < 0) une couleur hexadécimale."""
    r, g, b = hex_to_rgb(color)
    if factor >= 0:
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
    else:
        factor = -factor
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
    return rgb_to_hex((clamp(r, 0, 255), clamp(g, 0, 255), clamp(b, 0, 255)))
