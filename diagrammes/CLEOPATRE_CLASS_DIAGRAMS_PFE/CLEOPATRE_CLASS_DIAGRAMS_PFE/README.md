# Diagrammes de classes UML — Projet CLÉOPÂTRE (PFE)

## Objectif

Ce dossier contient l’ensemble des **diagrammes de classes UML** du système CLÉOPÂTRE, réalisés pour le rapport de Projet de Fin d’Études (PFE).

Les diagrammes documentent **le système réellement implémenté** (Next.js 16 + Drizzle ORM + PostgreSQL), et non un modèle théorique d’e-commerce.

Ils sont conçus pour être :
- techniquement exacts (source = code source + schéma Drizzle)
- lisibles en impression A4/A3
- cohérents entre eux
- utilisables directement dans le rapport PDF
- reproductibles dans StarUML / PlantUML

## Méthodologie

1. **Analyse exhaustive du code source**  
   - Schéma Drizzle (`src/db/schema.ts`) — source de vérité des entités et relations  
   - Server Actions (`src/actions/*.ts`)  
   - Bibliothèques métier (`src/lib/*.ts`)  
   - Routes App Router et API  
   - Migrations SQL (`drizzle/*.sql`)

2. **Modélisation UML 2.x**  
   - Classes = tables Drizzle + modules TypeScript cohérents  
   - Attributs = colonnes réelles (types, contraintes, valeurs par défaut)  
   - Méthodes = fonctions exportées réellement présentes  
   - Relations = clés étrangères + relations Drizzle déclarées

3. **Principe Global → Détaillé**  
   Le diagramme global donne la carte complète.  
   Chaque diagramme détaillé zoome sur une zone sans contredire le modèle global.

## Structure des diagrammes

| N° | Dossier | Contenu |
|----|---------|---------|
| 01 | `01_GLOBAL` | Diagramme de classes global — vue d’ensemble du système |
| 02 | `02_AUTHENTIFICATION_UTILISATEURS` | Utilisateurs, sessions, adresses, authentification |
| 03 | `03_ADMINISTRATION` | Back-office, rôles, gestion commandes/produits/clients |
| 04 | `04_GESTION_PRODUITS` | Catalogue, marques, catégories, merchandising, stock |
| 05 | `05_ACCES_DONNEES` | Couche Drizzle, PostgreSQL / PGlite, patterns CRUD |
| 06 | `06_ARCHITECTURE` | Organisation applicative (UI → Actions → Domaine → DB) |
| 07 | `07_COMMANDES_CHECKOUT` | Commandes, panier, checkout, promotions, événements |
| 08 | `08_FIDELITE_WISHLIST_GIFTCARDS` | Fidélité, wishlist, partage, cartes cadeaux |

Chaque dossier contient :
- `diagramme_classes_*.png` — version haute résolution (impression)
- `diagramme_classes_*.svg` — version vectorielle (redimensionnable)

## Correspondance avec le code source

### Authentification & Utilisateurs
- `src/db/schema.ts` → tables `users`, `sessions`, `password_resets`, `addresses`
- `src/lib/auth.ts` → `hashPassword`, `verifyPassword`, `createSession`, `getCurrentUser`
- `src/actions/auth.ts` → `loginAction`, `registerAction`, `logoutAction`, `saveAddressAction`, etc.

### Administration
- `src/actions/admin.ts` → gestion produits, commandes, rôles, promotions, gift cards, retours
- `src/actions/admin-os.ts` → métriques, insights, automations
- `src/lib/admin/*` → métriques, diagnostics, attention, period

### Gestion des produits
- `src/db/schema.ts` → `products`, `brands`, `categories`, `concerns`, `reviews`, `shelves`, `duos`, `product_substitutes`, `product_pairs`, `inventory_movements`
- `src/actions/admin.ts` → `saveProductAction`, `adjustStockAction`, `saveShelfAction`, `saveDuoAction`, …
- `src/lib/catalog.ts` → lecture catalogue / recherche

### Accès aux données
- `src/db/index.ts` → singleton `db` + `pool` (PostgreSQL ou PGlite)
- `src/db/schema.ts` → schéma complet + relations
- `src/db/seed.ts` → peuplement initial

### Architecture
- App Router Next.js 16 (`src/app/(site)/*`, `src/app/admin/*`)
- Server Actions + libs métier
- Domaine = tables Drizzle
- Persistance = PostgreSQL 17 (ou PGlite embarqué)

### Commandes & Checkout
- `src/db/schema.ts` → `orders`, `order_items`, `order_events`, `promotions`
- `src/actions/checkout.ts` → `placeOrderAction`, `cancelOrderAction`
- `src/lib/cart.ts` → panier client (CartLine, addLine, duoSavings…)
- `src/actions/shop.ts` → `validatePromoAction`
- `src/actions/admin.ts` → mise à jour statut / paiement / notes de commande

### Fidélité / Wishlist / Cartes cadeaux
- `src/db/schema.ts` → `loyalty_transactions`, `wishlist_items`, `wishlist_shares`, `gift_cards`, `gift_card_transactions`
- `src/actions/shop.ts` → `toggleWishlistAction`
- `src/actions/admin.ts` → `issueGiftCardAction`, `cancelGiftCardAction`
- Solde points stocké sur `users.loyaltyPoints`

## Choix de modélisation

Le projet est **orienté objets TypeScript + Drizzle**, et non un monolithe PHP procédural.

- Les **tables** du schéma Drizzle sont modélisées comme des **classes UML** (entités de domaine).
- Les **modules** (`src/lib/*`, `src/actions/*`) sont modélisés comme des **classes stéréotypées `<<module>>`** qui regroupent des responsabilités cohérentes.
- Les **enums** PostgreSQL sont représentés comme des enums UML.
- Les attributs JSONB complexes (ex. `shippingAddress`, `tolerances`, `images`) sont indiqués avec leur type sémantique.
- Aucune classe inventée (pas de `ProductRepository`, `OrderService` fictif, etc.).

Cette approche respecte la réalité du code tout en restant lisible pour un rapport académique.

## Reproduction dans StarUML

1. Ouvrir StarUML.
2. Créer un nouveau projet UML 2.x.
3. Pour chaque diagramme :
   - Créer un Class Diagram.
   - Reprendre les classes, attributs, méthodes et relations à partir du fichier `.puml` correspondant.
4. Les packages PlantUML correspondent aux packages StarUML.
5. Les stéréotypes `<<module>>`, `<<singleton>>`, `<<Drizzle>>` peuvent être ajoutés via les propriétés de classe.

Les fichiers `.puml` sont la référence exacte du contenu des diagrammes.

## Limites

- Le diagramme global ne reprend **pas toutes les 50+ tables** (ex. `email_outbox`, `analytics_events`, `rate_limits`, `newsletter_subscribers`, etc.) pour rester lisible. Ces tables existent et sont utilisées, mais sont secondaires pour la compréhension architecturale.
- Les attributs JSONB détaillés (structure exacte des objets) sont simplifiés dans les diagrammes pour la lisibilité ; le schéma source reste la référence.
- Les multiplicités sont déduites des clés étrangères et des contraintes d’unicité réellement présentes.
- Les méthodes listées sont les principales responsabilités exportées ; les helpers internes non exportés ne sont pas tous représentés.

## Validation

Chaque classe et chaque relation a été confrontée au code source avant génération.  
Aucun concept purement théorique (panier serveur classique, repository pattern, API REST commerciale, etc.) n’a été ajouté s’il n’était pas réellement implémenté sous cette forme.

---

**Stack technique du projet analysé**  
Next.js 16 (App Router) · React 19 · TypeScript · Drizzle ORM 0.45 · PostgreSQL 17 · Zod · Server Actions · Tailwind CSS v4 · Framer Motion · GSAP

**Date d’analyse** : septembre 2026  
**Projet** : CLÉOPÂTRE — Espace Santé Beauté (parapharmacie Ezzahra / Hammam-Lif)
