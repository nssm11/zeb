# CLÉOPÂTRE — Espace Santé Beauté · Diagrammes UML (PFE)

Package complet de diagrammes UML 2.x du système **CLÉOPÂTRE** (plateforme de
e-commerce / parapharmacie), réalisé pour le rapport de **Projet de Fin d’Études**.

> **18 diagrammes** : 8 diagrammes de classes + 10 diagrammes de séquence,
> générés à partir des sources PlantUML, avec un **design system unique**
> (Inter, palette ivoire / charbon / champagne, accents bleu discret) pour
> une insertion directe dans le rapport PDF (A4 / A3, couleur ou noir et blanc).

## Contenus

| Dossier | Diagrammes |
|---------|-----------|
| `CLEOPATRE_CLASS_DIAGRAMS_PFE/` | 8 diagrammes de classes (vue globale + 7 vues détaillées) |
| `CLEOPATRE_SEQUENCE_DIAGRAMS_PFE/` | 10 diagrammes de séquence (vue globale + 9 workflows) |

Chaque sous-dossier (`01_GLOBAL`, `02_AUTHENTIFICATION_UTILISATEURS`, …) contient :

| Fichier | Rôle |
|---------|------|
| `*.puml` | Source PlantUML (reproductible, thème inclus) |
| `*.svg` | Vectoriel **4K 16:9** (viewBox 3840 × 2160) — master sans titre, contenu maximisé |
| `*.png` | **4K UHD (3840 × 2160, 16:9)** — rendu fidèle du SVG master |

### Format des maîtres 4K

Tous les diagrammes sont livrés **plein cadre 16:9** (3840 × 2160 px), prêts à
être insérés dans Word ou un diaporama :

- **aucun titre à l'intérieur de l'image** — le fond est blanc, sans bandeau,
  sans pied de page, sans panneau latéral ; le titre se place dans la légende
  du document ;
- **contenu maximisé et centré** : chaque diagramme est élargi (ou allongé)
  vectoriellement — l'espacement entre les colonnes de classes ou entre les
  lignes de vie est dilaté, sans déformer aucun texte ni rectangle — jusqu'à
  occuper la quasi-totalité du cadre, avec une fine marge uniforme ;
- aucun texte étiré ou déformé : seuls les espacements vides sont dilatés ;
- calibré pour rester **lisible inséré à 15 cm de large** dans Word.

## Principe « Global → Détaillé »

- Les **vue globale** (01) donnent la carte d’ensemble : domaines, flux majeurs,
  classes nommées (sans attributs pour le diagramme de classes global).
- Les **vues détaillées** (02 → 08 / 02 → 10) zooment sur un sous-système :
  attributs, méthodes, multiplicités, conditions (`alt` / `opt`).
- Les deux niveaux décrivent le **même système** ; aucune architecture fictive
  (pas de controllers, repositories ou services inventés).

## Fidélité au code source

Les diagrammes documentent l’implémentation réelle :

```
Interface (Next.js 16 App Router)
   → Server Actions (src/actions/*)
   → Modules métier (src/lib/*)
   → Drizzle ORM (src/db/*)
   → PostgreSQL 17 / PGlite
```

- Classes = tables du schéma Drizzle (`src/db/schema.ts`) + modules TypeScript
  stéréotypés `«module»`, `«singleton»`, `«type»`.
- Méthodes = fonctions exportées réellement présentes.
- Relations = clés étrangères et relations Drizzle.
- Messages de séquence = français naturel, sans SQL ni bruit d’implémentation
  dans les vues globales ; les noms d’actions réels apparaissent dans les vues
  détaillées (`saveProductAction`, `placeOrderAction`, …).

## Regeneration des diagrammes

Les sources `.puml` sont autonomes (theme inclus) et compatibles **PlantUML ≥ 1.2025**.

### Option 1 — PlantUML standard (Java)

```bash
java -jar plantuml.jar -tsvg -tpng diagramme_classes_global.puml
```

> Le `.puml` contient uniquement le diagramme. La mise en plein cadre 4K
> 16:9 (dilatation des espacements + centrage) est appliquée en
> post-traitement du SVG par le pipeline de génération ; un rendu PlantUML
> direct donne le diagramme à son format naturel.

### Option 2 — Moteur PlantUML JavaScript (sans Java)

```bash
npm install @plantuml/core
node -e "
import('@plantuml/core/plantuml.js').then(({ renderToString }) => {
  renderToString(require('fs').readFileSync('diagramme_classes_global.puml','utf8').split('\n'),
    svg => require('fs').writeFileSync('out.svg', svg),
    err => console.error(err));
});"
```

## Contraintes graphiques respectées

- Fond blanc, police **Inter**, typographie hiérarchisée (titres semibold,
  corps regular, annotations grises).
- Palettes sobres : charbon `#2C2A26`, grès `#A89B85`, ivoire `#FAF7F1`,
  champagne `#DCCFBA`, accent bleu discret `#5B7C99`.
- Packages = conteneurs arrondis à bordure fine (pas d’onglets UML classiques).
- Flèches fines, associations pleines, dépendances en pointillés,
  multiplicités minimales, pas de « spaghetti » relationnel.
- Lisibles en **noir et blanc** (la sémantique ne repose jamais sur la couleur seule).

---

**Stack technique du système documenté**
Next.js 16 (App Router) · React 19 · TypeScript · Drizzle ORM · PostgreSQL 17 ·
Zod · Tailwind CSS v4 · Framer Motion · GSAP · Server Actions
