# 01_GLOBAL — Vue d'ensemble des classes

Ce dossier contient deux livrables complémentaires pour la vue globale du
système **CLÉOPÂTRE** :

| Fichier | Rôle | Format |
|---------|------|--------|
| `01_classes_global.png` | **Diagramme de classes global, version design system premium** | 2800 × 1575 px (16:9), PNG |
| `01_classes_global.svg` | Master vectoriel du précédent (source du PNG) | SVG 2400 × 1350 |
| `diagramme_classes_global.png` / `.svg` / `.puml` | Même vue, rendu PlantUML d'origine | 4K |

## Contenu du diagramme `01_classes_global.*`

- **5 packages** clairement regroupés :
  1. *Utilisateurs & Auth* — `User`, `Session`, `Address`, `AuthLib`, `AuthActions`
  2. *Catalogue* — `Product`, `Brand`, `Concern`, `StockMovement`, `CatalogLib`
  3. *Expérience client* — `Wishlist`, `WishlistItem`, `WishlistShare`,
     `GiftCard`, `LoyaltyTransaction`
  4. *Commandes* — `Order`, `OrderItem`, `OrderEvent`, `CartLib`, `OrdersLib`
  5. *Persistance* — `Schema`, `PostgreSQL` `«singleton»`, `Migrations`,
     `OrderEvent`, `OrderItem`
- **Zone « Services Applicatifs »** : `src/lib/auth.ts`, `src/lib/catalog.ts`,
  `src/lib/orders.ts`, `src/actions/auth.ts`, `src/actions/admin.ts`,
  reliés aux packages du domaine par des connecteurs orthogonaux fléchés.
- Les stéréotypes `«module»` (couche `src/lib`) et `«actions»`
  (Server Actions `src/actions`) distinguent les modules des entités du
  schéma Drizzle ; `PostgreSQL` porte l'étiquette `«singleton»`.

## Design system

| Élément | Valeur |
|---------|--------|
| Fond | `#FAFAF9` |
| Texte | `#111827` |
| Accent primaire | `#1E3A5F` (indigo profond) |
| Accent secondaire | `#B45309` (or sourd, parcimonieux) |
| Bordures de cartes | `#E5E7EB`, rayon 10–12 px, ombre douce |
| Packages chauds / acteurs | `#FFFBF5` |
| Base de données | `#F0F7F4` |
| Typographie | Inter (400/500/600) · JetBrains Mono pour les chemins de fichiers |
| Marge extérieure | 40 px |

## Régénération

```bash
cd source
python3 -m pip install fonttools          # pour le calcul des chasses de caractères

# 1. master SVG (écrit ../01_classes_global.svg)
python3 gen_01_classes_global.py

# 2. PNG haute résolution
npm i @resvg/resvg-js
node render_png.js ../01_classes_global.svg ../01_classes_global.png 2800
```

Les polices nécessaires sont embarquées dans `source/fonts/`
(Inter et JetBrains Mono, licence SIL Open Font License) afin que le rendu
soit reproductible à l'identique sur n'importe quelle machine.
