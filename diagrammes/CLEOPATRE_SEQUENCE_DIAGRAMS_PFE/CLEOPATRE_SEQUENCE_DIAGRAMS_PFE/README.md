# CLÉOPÂTRE — Diagrammes de Séquence (PFE)

## Objectif

Package de diagrammes de séquence UML 2.x destinés à la section **I. Diagramme de Séquence** du rapport de Projet de Fin d’Études.

Les diagrammes documentent le comportement **réel** de la plateforme Cléopâtre (Next.js 16, Server Actions, Drizzle ORM, PostgreSQL).

---

## Principe de lecture

| Niveau | Rôle |
|--------|------|
| **01 – Global** | Vue d’ensemble pure. Tous les flux majeurs apparaissent ensemble sur un seul diagramme. Aucune explication à l’intérieur de l’image. |
| **02 à 10 – Détaillés** | Un workflow réel par diagramme, expliqué chronologiquement avec les conditions du code (`alt` / `opt`). |

---

## Design

- Fond blanc pur
- Typographie Inter
- Palette sobre (ivoire / charbon / champagne)
- Aucun titre, aucun numéro de figure, aucune note décorative à l’intérieur des images
- Export haute résolution PNG + SVG vectoriel

---

## Contenu

| Dossier | Diagramme | Workflow réel |
|---------|-----------|---------------|
| 01_GLOBAL | sequence_global | Tous les flux majeurs ensemble |
| 02_AUTHENTIFICATION | sequence_authentification | loginAction → session |
| 03_GESTION_PRODUITS | sequence_gestion_produits | Vue d’ensemble CRUD produits |
| 04_AJOUT_PRODUIT | sequence_ajout_produit | saveProductAction (INSERT) |
| 05_MODIFICATION_PRODUIT | sequence_modification_produit | saveProductAction (UPDATE) |
| 06_ARCHIVAGE_PRODUIT | sequence_archivage_produit | status = archived |
| 07_CONSULTATION | sequence_consultation | Server Components + SELECT |
| 08_DECONNEXION | sequence_deconnexion | logoutAction → destroySession |
| 09_ADMINISTRATION | sequence_administration | Back-office (admin / support) |
| 10_COMMANDE | sequence_commande | placeOrderAction (checkout) |

---

## Correspondance code source

**Authentification**  
`src/actions/auth.ts` → `loginAction`, `logoutAction`  
`src/lib/auth.ts` → `createSession`, `destroySession`, `verifyPassword`, `getCurrentUser`

**Produits**  
`src/actions/admin.ts` → `saveProductAction` (création, modification et archivage)

**Consultation**  
`src/app/(site)/boutique/page.tsx`  
`src/app/(site)/produit/[slug]/page.tsx`

**Commande**  
`src/actions/checkout.ts` → `placeOrderAction`  
`src/lib/orders.ts`

**Administration**  
`src/actions/admin.ts` + `src/actions/admin-os.ts`  
`requireAdmin` / `requireStaff`

---

## Choix de modélisation

Le projet utilise des **Server Actions** et des modules fonctionnels (pas de couches Controller/Service/Repository classiques).  
Les lifelines représentent donc les modules logiques réels :

- Pages (boundary)
- Server Actions (control)
- `lib/auth` (session)
- PostgreSQL (entity)

Ceci reste conforme à UML 2.x.

---

## Reproduction

```bash
java -jar plantuml.jar -tsvg -tpng *.puml
```

Les fichiers `.puml` fournis correspondent exactement aux images livrées.

### StarUML
Chaque diagramme peut être reconstruit manuellement :
1. Sequence Diagram
2. Actors + Lifelines listés
3. Messages dans l’ordre chronologique
4. Fragments `alt` / `opt` là où indiqués
5. Style : fond blanc, police lisible, pas de titre interne

---

## Limitations

- Les e-mails asynchrones (Brevo/Resend) ne sont pas représentés comme participants principaux.
- Le panier côté client n’apparaît qu’au moment du checkout.
- L’archivage produit se fait par statut (`archived`) ; il n’existe pas de DELETE physique dans le code.

---

*Généré à partir de l’analyse du code source du projet Cléopâtre — Espace Santé Beauté.*
