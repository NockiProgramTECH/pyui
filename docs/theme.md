# Thème (Design System)

## Utilisation

```python
from pyui import Theme

# Modes
Theme.light()
Theme.dark()
Theme.set_mode("dark")
Theme.mode()  # → "light" ou "dark"

# Jetons
primary = Theme.get("primary")
Theme.configure(primary="#2563EB", secondary="#64748B")

# Police
font = Theme.font("base", "bold")  # → ("Segoe UI", 11, "bold")
```

## Palette de couleurs

| Jeton | Light | Dark |
|-------|-------|------|
| `primary` | `#2563EB` | `#3B82F6` |
| `on_primary` | `#FFFFFF` | `#FFFFFF` |
| `primary_hover` | `#1D4ED8` | `#2563EB` |
| `secondary` | `#64748B` | `#64748B` |
| `background` | `#F8FAFC` | `#0F172A` |
| `surface` | `#FFFFFF` | `#1E293B` |
| `surface_hover` | `#F1F5F9` | `#334155` |
| `text` | `#1E293B` | `#F1F5F9` |
| `muted` | `#64748B` | `#94A3B8` |
| `border` | `#E2E8F0` | `#334155` |
| `success` | `#16A34A` | `#22C55E` |
| `danger` | `#DC2626` | `#EF4444` |
| `warning` | `#D97706` | `#F59E0B` |

## Typographie

Tailles : `xs` (9), `sm` (10), `base` (11), `lg` (13), `xl` (16), `2xl` (20), `3xl` (26)

Poids : `normal`, `bold`

Police par défaut : `Segoe UI`

## Réactivité au thème

Tous les composants s'abonnent automatiquement au thème et se mettent à jour lors de `Theme.dark()` / `Theme.light()` / `Theme.configure()`.