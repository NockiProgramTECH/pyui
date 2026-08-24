# Changelog

Toutes les modifications notables de PyUI seront documentées dans ce fichier.

## [Unreleased]

- Aucune modification en attente.

## [0.1.0] — 2026-08-24

Version 0.1.0 — **PREMIÈRE VERSION STABLE**.

Conforme à la roadmap : Core, Widgets, Layouts, Sidebar/Navbar, Theme, Forms,
DataTable, Navigation avancée, Dashboard, État réactif, Packaging,
Documentation complète et API de placement explicite.

### Phase 1-3 — Core, widgets de base, layouts
- Structure src-layout du projet (pyproject.toml, src/pyui, tests, examples, docs)
- `Component` : cycle de vie `create → render → update → destroy`, API commune `show/hide/configure/pack/grid/place/bind`, enfants, abonnement faible au thème
- `App` : fenêtre Tk, routes, navigation, EventBus, State, Theme, fermeture propre
- `Page` : conteneur plein écran pour les routes
- Widgets : `Button` (7 variantes + hover), `Label`, `Input` (placeholder), `Text`, `CheckBox`, `RadioButton` (groupes), `Select`, `ListBox`, `ProgressBar`, `Separator`, `Frame`, `Card`
- Layouts : `Container`, `Row`, `Column`, `Stack`, `Grid`

### Phase 4 — Sidebar + Navbar + Navigation
- `Sidebar` : titre, logo, icônes, items, sous-menus repliables, élément actif, routes, collapse/expand, abonnement `navigate`
- `Navbar` : titre + actions (boutons), `set_title()`
- `Footer` : texte centré
- `App.set_content()` : conteneur personnalisé pour les pages
- `App.navigate()` émet l'événement `"navigate"`
- `IconManager.glyph()` + ~40 glyphes Unicode + `icon=` sur `Button`
- `StatCard` : carte statistique avec valeur, delta coloré

### Phase 5 — Theme
- `Theme.light()/dark()/set_mode()/get()/font()/configure()`
- Palettes light/dark complètes (20 jetons)
- Styles ttk pour Combobox, Progressbar, Treeview, Scrollbar
- Composants réactifs au thème (abonnement faible)

### Phase 6 — Formulaires
- `Form` : rendu (label + widget + erreur), `values()`, `set_values()`, `validate()`, `submit()`, `clear()`, boutons
- `TextField`, `PasswordField`, `EmailField`, `NumberField` (min/max, conversion int/float), `SelectField`, `CheckboxField`, `DateField`, `FileField` (bouton Parcourir)
- Validation : `required`, `min_length`, `max_length`, `pattern`, `validator`, email, nombre, date

### Phase 7 — DataTable
- `DataTable` : Treeview avec colonnes, données, tri par en-tête (▲/▼), recherche instantanée, pagination (Précédent/Suivant), sélection, double-clic, menu contextuel (Modifier/Supprimer/actions), export CSV (UTF-8 BOM)
- `TableColumn` : largeur, alignement, triable
- Styles Treeview intégrés au thème
- `Button.enable()/disable()`, `Card.set_title()/set_subtitle()`

### Phase 8 — Navigation avancée
- `Router` amélioré : historique, `back()`, `forward()`, `push()`, `reset()`, `Route` (path, title, name)
- `App.back()`, `App.forward()`, `App.current_path`, `App.can_back`, `App.can_forward`
- Hooks : `App.before_navigate()`, `App.after_navigate()`
- `Page.on_show()`, `Page.on_hide()` (cycle de vie de la page)

### Niveau 2 — Widgets avancés
- `Badge` : étiquette colorée (6 variantes)
- `Alert` : message coloré avec fermeture optionnelle (info/success/warning/danger)
- `Tooltip` : infobulle au survol (délai configurable)
- `Spinner` : animation de chargement Canvas (démarrage/arrêt)
- `Loading` : surcouche avec spinner + message (open/close)
- `Tabs` : onglets avec zone de contenu (callable ou sous-classe)
- `Accordion` : sections repliables (toggle)
- `Modal` : fenêtre modale avec titre, contenu personnalisé, close

### Phase 9 — Dashboard
- `Chart` : graphique barres/courbes sur Canvas (données labels/values, redimensionnement, theme)
- `StatCard` : carte statistique avec icône, valeur, delta coloré
- `Activity` : flux d'activités (icône, texte, temps)
- `Timeline` : chronologie verticale (titre, temps, description)
- `QuickAction` : bouton d'action rapide (outline + icône)
- `Metric` : grande valeur + étiquette
- `Dashboard` : composition prête à l'emploi (stats grid + chart + activity + timeline + actions)
- `_parent_tk()` accepte les widgets Tkinter bruts comme parent

### Phase 10 — État réactif
- `State` amélioré : abonnement par clé ou global, callbacks `(key, value, old)`, no-op si valeur inchangée
- `State.update()`, `State.snapshot()`, `State.reset()`, `State.replace()`, `State.has()`
- `State.bind(component, key, target)` : liaison d'une clé à une propriété ou un callable (weakref)
- `Component.bind_state(state, key, target)` : liaison avec désabonnement automatique à la destruction

### Dialogues et notifications
- `Dialog.confirm()` : Toplevel modal avec callbacks Oui/Non
- `Dialog.error()`, `Dialog.warning()`, `Dialog.success()`, `Dialog.info()` (messagebox)
- `Toast` : fenêtre éphémère (3,5s) en bas à droite, succès/erreur/avertissement/info

### Documentation
- 15 fichiers de documentation structurée (docs/)
- Tutoriel pas à pas : `docs/tutorial.md`
- 6 exemples d'application (01 à 06)
- README.md complet avec liens vers la doc

### Phase 11 — Packaging et tests
- Version centralisée 0.1.0 (pyproject.toml + pyui.__version__)
- pyproject : optional-dependencies dev (pytest, pytest-cov, build), configuration coverage
- Marqueur `py.typed` (typing)
- Tests de packaging : version, exports publics (`__all__`), imports des exemples
- CI GitHub Actions : tests sous Xvfb (Python 3.10/3.12) + build du package
- Build vérifié : wheel + sdist (`pyui-0.1.0-py3-none-any.whl`), installation dans un venv propre

### Amélioration finale — Placement et API explicite
- Modèle de placement : `Pack`, `GridPlacement`, `Place` (`pyui.core.placement`)
- `Component.pack()/grid()/place()` : paramètres nommés explicites (plus aucun `**kwargs`), validation avec messages clairs
- `Component.layout(placement)` + `Component.placement` : placement réutilisable, restauration exacte par `show()/hide()`
- `pack/grid` acceptent les tuples de marge `padx=(gauche, droite)`, `pady=(haut, bas)`
- Suppression de `**kwargs` dans toutes les signatures publiques (widgets, layouts, Form, DataTable, champs, routes)
- `Input(show=...)` : masquage de la saisie (mot de passe)
- Documentation : `docs/placement.md` — tous les paramètres de pack/grid/place listés
- 110 tests unitaires (dont 14 dédiés au placement)
