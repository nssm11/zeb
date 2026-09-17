# CLÉOPÂTRE — Diagrammes de séquence (PFE)

## Objectif

Package de diagrammes de séquence UML 2.x destinés à la section
**Diagrammes de séquence** du rapport de Projet de Fin d’Études.

Les diagrammes documentent le comportement **réel** de la plateforme CLÉOPÂTRE
(Next.js 16, Server Actions, Drizzle ORM, PostgreSQL).

## Principe de lecture

| Niveau | Rôle |
|--------|------|
| **01 – Vue globale** | Tous les flux majeurs sur un seul diagramme, en 5 scénarios numérotés (01 Consultation · 02 Authentification · 03 Commande · 04 Administration · 05 Déconnexion). Messages de niveau élevé uniquement — aucun SQL, aucune route HTTP. |
| **02 → 10 – Détaillés** | Un workflow réel par diagramme, chronologique, avec les conditions du code (`alt` / `opt`) et les noms d’actions réels (`saveProductAction`, `placeOrderAction`, …). |

## Contenu

| Dossier | Diagramme | Workflow réel |
|---------|-----------|---------------|
| 01_GLOBAL | `sequence_global` | Tous les flux majeurs ensemble |
| 02_AUTHENTIFICATION | `sequence_authentification` | `loginAction` → session (cookie httpOnly) |
| 03_GESTION_PRODUITS | `sequence_gestion_produits` | Vue d’ensemble du cycle CRUD produits |
| 04_AJOUT_PRODUIT | `sequence_ajout_produit` | `saveProductAction` (création, transaction, stock, concerns) |
| 05_MODIFICATION_PRODUIT | `sequence_modification_produit` | `saveProductAction` (édition) |
| 06_ARCHIVAGE_PRODUIT | `sequence_archivage_produit` | `status = « archived »` (pas de suppression physique) |
| 07_CONSULTATION | `sequence_consultation` | Server Components + lecture catalogue |
| 08_DECONNEXION | `sequence_deconnexion` | `logoutAction` → `destroySession` |
| 09_ADMINISTRATION | `sequence_administration` | Back-office, `requireAdmin` / `requireStaff` |
| 10_COMMANDE | `sequence_commande` | `placeOrderAction` (checkout complet) |

Chaque dossier contient :

- `sequence_*.puml` — source PlantUML (thème inclus, autonome)
- `sequence_*.svg` — vectoriel, **titré** (titre centré + sous-titre projet)
- `sequence_*.png` — haute résolution (≈ 192 dpi), rendu fidèle du SVG

## Design

- Fond blanc pur, typographie **Inter**
- Palette sobre (ivoire / charbon / champagne, accent bleu discret)
- Titres centrés, sobres et identiques d’un diagramme à l’autre
- Lifelines fines, fragments `alt` / `opt` discrets, activations subtiles
- Lisibles en noir et blanc (la sémantique ne repose pas sur la couleur)

## Correspondance code source

**Authentification / Déconnexion**
`src/actions/auth.ts` → `loginAction`, `logoutAction`
`src/lib/auth.ts` → `createSession`, `destroySession`, `verifyPassword`, `getCurrentUser`

**Produits**
`src/actions/admin.ts` → `saveProductAction` (création, modification, archivage)

**Consultation**
`src/app/(site)/boutique/page.tsx` · `src/app/(site)/produit/[slug]/page.tsx`
`src/lib/catalog.ts`

**Commande**
`src/actions/checkout.ts` → `placeOrderAction` · `src/lib/orders.ts`

**Administration**
`src/actions/admin.ts` + `src/actions/admin-os.ts` · `requireAdmin` / `requireStaff`

## Choix de modélisation

Le projet utilise des **Server Actions** et des modules fonctionnels (pas de
couches Controller/Service/Repository classiques). Les lifelines représentent
donc les modules logiques réels :

- **Utilisateur / Administrateur** — acteurs
- **Interface (Next.js)** — boundary (pages App Router)
- **Server Actions** — control (`src/actions/*`)
- **lib/auth, lib/orders, lib/catalog** — modules métier (`src/lib/*`)
- **PostgreSQL** — entity (via Drizzle ORM)

Ceci reste conforme à UML 2.x.

## Reproduction

Les `.puml` sont autonomes (thème inclus) :

```bash
# PlantUML standard (Java)
java -jar plantuml.jar -tsvg -tpng sequence_authentification.puml
```

Ou avec le moteur PlantUML JavaScript (sans Java) : `npm install @plantuml/core`
puis `renderToString(lines, onSuccess, onError)`.

Le bandeau de titre centré est ajouté au SVG en post-traitement lors de la
génération du présent package ; le `.puml` contient uniquement le diagramme.

## Limitations

- Les e-mails asynchrones (Brevo/Resend) ne sont pas représentés comme
  participants principaux.
- Le panier côté client n’apparaît qu’au moment du checkout.
- L’archivage produit se fait par statut (`archived`) ; il n’existe pas de
  DELETE physique dans le code.

---

*Généré à partir de l’analyse du code source du projet CLÉOPÂTRE — Espace
Santé Beauté. PlantUML 1.2026.8 (moteur JS `@plantuml/core`) · septembre 2026.*
