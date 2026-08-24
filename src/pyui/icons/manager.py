"""Système d'icônes unifié (Niveau 9).

Fonctionne par glyphes Unicode (pas d'images externes).
"""

GLYPHS = {
    "home": "\u2302",
    "dashboard": "\u25A6",
    "users": "\U0001F465",
    "user": "\U0001F464",
    "settings": "\u2699",
    "search": "\u2315",
    "edit": "\u270E",
    "delete": "\u2716",
    "plus": "\u271A",
    "minus": "\u2212",
    "save": "\U0001F4BE",
    "download": "\u21E9",
    "upload": "\u21E7",
    "menu": "\u2630",
    "arrow-left": "\u2190",
    "arrow-right": "\u2192",
    "money": "\U0001F4B0",
    "chart": "\U0001F4C8",
    "bell": "\U0001F514",
    "logout": "\u23FB",
    "folder": "\U0001F4C1",
    "file": "\U0001F4C4",
    "clock": "\U0001F552",
    "check": "\u2714",
    "warning": "\u26A0",
    "info": "\u2139",
    "refresh": "\u21BB",
    "lock": "\U0001F512",
    "box": "\U0001F4E6",
    "cart": "\U0001F6D2",
    "tag": "\U0001F3F7",
    "chevron-right": "\u25B8",
    "chevron-down": "\u25BE",
    "eye": "\U0001F441",
    "calendar": "\U0001F4C5",
    "print": "\U0001F5A8",
    "mail": "\u2709",
    "phone": "\u2706",
    "plus_circle": "\u2795",
}


class IconManager:
    """Résout un nom d'icône en glyphe Unicode."""

    _cache = {}

    @classmethod
    def glyph(cls, name):
        """Renvoie le glyphe associé à un nom (ou '' si inconnu)."""
        if name not in cls._cache:
            cls._cache[name] = GLYPHS.get(name, "")
        return cls._cache[name]

    @classmethod
    def get(cls, name, size=16):
        return cls.glyph(name)