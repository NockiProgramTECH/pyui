# Icônes

## Utilisation

```python
from pyui import IconManager, GLYPHS

glyphe = IconManager.glyph("home")  # → "⌂"
```

Les icônes sont des glyphes Unicode. Aucune image externe n'est nécessaire.

## Icônes disponibles

| Nom | Glyphe | Nom | Glyphe |
|-----|--------|-----|--------|
| `home` | ⌂ | `dashboard` | ▦ |
| `users` | 👥 | `user` | 👤 |
| `settings` | ⚙ | `search` | ⌕ |
| `edit` | ✎ | `delete` | ✖ |
| `plus` | ✚ | `minus` | − |
| `save` | 💾 | `download` | ⇩ |
| `upload` | ⇧ | `menu` | ☰ |
| `arrow-left` | ← | `arrow-right` | → |
| `money` | 💰 | `chart` | 📈 |
| `bell` | 🔔 | `logout` | ⏻ |
| `folder` | 📁 | `file` | 📄 |
| `clock` | 🕐 | `check` | ✔ |
| `warning` | ⚠ | `info` | ℹ |
| `refresh` | ↻ | `lock` | 🔒 |
| `box` | 📦 | `cart` | 🛒 |
| `tag` | 🏷 | `chevron-right` | ▸ |
| `chevron-down` | ▾ | `eye` | 👁 |
| `calendar` | 📅 | `mail` | ✉ |
| `phone` | ✆ | `plus_circle` | ➕ |

## Icônes dans les composants

```python
Button(parent, text="Clients", icon="users")
Button(parent, icon="search")  # icône seule
```