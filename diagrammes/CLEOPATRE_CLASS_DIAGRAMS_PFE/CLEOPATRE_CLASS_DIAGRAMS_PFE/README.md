# Diagrammes de classes UML — Projet CLÉOPÂTRE (PFE)

## Objectif

Ce dossier contient l’ensemble des **diagrammes de classes UML** du système
CLÉOPÂTRE, réalisés pour le rapport de Projet de Fin d’Études (PFE).

Les diagrammes documentent **le système réellement implémenté**
(Next.js 16 + Server Actions + Drizzle ORM + PostgreSQL), et non un modèle
théorique d’e-commerce.

Ils sont conçus pour être :

- techniquement exacts (source = code source + schéma Drizzle)
- lisibles en impression A4/A3 (couleur ou noir et blanc)
- cohérents entre eux (même design system, même palette, même typographie)
- utilisables directement dans le rapport PDF
- reproductibles à partir des sources `.puml` fournies

## Structure des diagrammes

| N° | Dossier | Contenu |
|----|---------|---------|
| 01 | `01_GLOBAL` | Vue d’ensemble — 6 domaines fonctionnels, classes nommées uniquement |
| 02 | `02_AUTHENTIFICATION_UTILISATEURS` | Utilisateurs, sessions, adresses, resets, authentification |
| 03 | `03_ADMINISTRATION` | Back-office, rôles, commandes, catalogue, support |
| 04 | `04_GESTION_PRODUITS` | Catalogue, merchandising, associations, stock, avis |
| 05 | `05_ACCES_DONNEES` | Couche Drizzle, PostgreSQL / PGlite, seed, patterns CRUD |
| 06 | `06_ARCHITECTURE` | Organisation applicative (Interface → Actions → Domaine → Persistance) |
| 07 | `07_COMMANDES_CHECKOUT` | Commandes, lignes, événements, promotions, panier |
| 08 | `08_FIDELITE_WISHLIST_GIFTCARDS` | Fidélité, wishlist & partage, cartes cadeaux |

Chaque dossier contient :

- `diagramme_classes_*.puml` — source PlantUML (thème inclus, autonome)
- `diagramme_classes_*.svg` — vectoriel, **titré** (titre centré + sous-titre)
- `diagramme_classes_*.png` — haute résolution (≈ 192 dpi), rendu fidèle du SVG

Le bandeau de titre est ajouté en post-traitement du SVG ; les `.puml`
contiennent uniquement le diagramme (reproductibles avec PlantUML standard).

## Correspondance avec le code source

### Authentification & Utilisateurs
- `src/db/schema.ts` → tables `users`, `sessions`, `password_resets`, `addresses`
- `src/lib/auth.ts` → `hashPassword`, `verifyPassword`, `createSession`,
  `destroySession`, `getCurrentUser`, `pruneExpiredSessions`
- `src/actions/auth.ts` → `loginAction`, `registerAction`, `logoutAction`,
  `saveAddressAction`, `changePasswordAction`, …

### Administration
- `src/actions/admin.ts` → gestion produits, commandes, rôles, promotions,
  gift cards, retours, avis
- `src/actions/admin-os.ts` → métriques, insights, diagnostics, automations
- `src/lib/admin/*` → métriques, diagnostics, attention, période

### Gestion des produits
- `src/db/schema.ts` → `products`, `brands`, `categories`, `concerns`,
  `reviews`, `shelves`, `duos`, `product_substitutes`, `product_pairs`,
  `inventory_movements`
- `src/actions/admin.ts` → `saveProductAction`, `adjustStockAction`,
  `saveShelfAction`, `saveDuoAction`, …
- `src/lib/catalog.ts` → lecture catalogue / recherche

### Accès aux données
- `src/db/index.ts` → singleton `db` + `pool` (PostgreSQL ou PGlite)
- `src/db/schema.ts` → schéma complet + relations déclaratives
- `src/db/seed.ts` → peuplement initial

### Architecture
- App Router Next.js 16 (`src/app/(site)/*`, `src/app/admin/*`, `src/app/api/*`)
- Server Actions (`src/actions/*`) + libs métier (`src/lib/*`)
- Domaine = tables Drizzle
- Persistance = PostgreSQL 17 (ou PGlite embarqué)

### Commandes & Checkout
- `src/db/schema.ts` → `orders`, `order_items`, `order_events`, `promotions`
- `src/actions/checkout.ts` → `placeOrderAction`, `cancelOrderAction`
- `src/lib/cart.ts` → panier client (`CartState`, `CartLine`, `duoSavings`…)
- `src/lib/orders.ts` → réservation de numéro, promotions, fidélité
- `src/actions/shop.ts` → `validatePromoAction`
- `src/actions/admin.ts` → statut / paiement / notes de commande

### Fidélité / Wishlist / Cartes cadeaux
- `src/db/schema.ts` → `loyalty_transactions`, `wishlist_items`,
  `wishlist_shares`, `gift_cards`, `gift_card_transactions`
- `src/actions/shop.ts` → `toggleWishlistAction`
- `src/actions/admin.ts` → `issueGiftCardAction`, `cancelGiftCardAction`
- Solde points stocké sur `users.loyaltyPoints`

## Choix de modélisation

Le projet est **orienté modules TypeScript + Drizzle**, et non un monolithe
procédural classique.

- Les **tables** du schéma Drizzle sont modélisées comme des **classes UML**
  (entités de domaine).
- Les **modules** (`src/lib/*`, `src/actions/*`) sont modélisés comme des
  classes stéréotypées `«module»` regroupant des responsabilités cohérentes.
- Les **enums** PostgreSQL sont représentés comme des enums UML.
- Les attributs JSONB complexes (`shippingAddress`, `tolerances`, `images`…)
  sont indiqués avec leur type sémantique.
- Les **relations inutiles à la compréhension** sont retirées (pas de
  spaghetti) ; les types d’attributs (ex. `status : order_status`) portent
  alors la référence aux enums.
- Aucune classe inventée (pas de `ProductRepository`, `OrderService` fictif,
  etc.).

## Limites assumées

- Le diagramme global (01) ne reprend **pas toutes les 50+ tables**
  (`email_outbox`, `analytics_events`, `rate_limits`,
  `newsletter_subscribers`, …) pour rester lisible. Ces tables existent,
  sont utilisées, mais sont secondaires pour la compréhension architecturale.
- Les attributs JSONB détaillés (structure exacte des objets) sont simplifiés ;
  le schéma source reste la référence.
- Les multiplicités sont déduites des clés étrangères et des contraintes
  d’unicité réellement présentes.
- Les méthodes listées sont les principales responsabilités exportées ;
  les helpers internes non exportés ne sont pas tous représentés.

## Reproduction

Les `.puml` sont autonomes (thème inclus) :

```bash
# PlantUML standard (Java)
java -jar plantuml.jar -tsvg -tpng diagramme_classes_global.puml
```

Ou avec le moteur PlantUML JavaScript (sans Java) :

```bash
npm install @plantuml/core
# puis renderToString(lines, onSuccess, onError) sur le contenu du .puml
```

Le rendu PlantUML brut correspond au diagramme ; le bandeau de titre centré
(« Diagramme de classes – … » + sous-titre CLÉOPÂTRE) est ajouté au SVG en
post-traitement lors de la génération du présent package.

---

**Stack technique du projet analysé**
Next.js 16 (App Router) · React 19 · TypeScript · Drizzle ORM · PostgreSQL 17 ·
Zod · Server Actions · Tailwind CSS v4 · Framer Motion · GSAP

**Génération** : PlantUML 1.2026.8 (moteur JS `@plantuml/core`) · septembre 2026
**Projet** : CLÉOPÂTRE — Espace Santé Beauté (parapharmacie Ezzahra / Hammam-Lif)
